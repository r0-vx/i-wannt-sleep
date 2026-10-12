from __future__ import annotations

import re
from collections import Counter

import httpx
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.db import SessionLocal
from app.models import (
    BaitTag,
    Claim,
    Evidence,
    Investigation,
    InvestigationStatus,
    JobEvent,
    Source,
    Verdict,
)
from app.schemas import EvidenceForVerification
from app.services.bait import score_bait_spans
from app.services.providers import (
    BraveSearchProvider,
    GeminiProvider,
    ProviderConfigurationError,
    ProviderResponseError,
    SafePageFetcher,
    UnsafeUrlError,
)


def emit(
    db: Session, investigation: Investigation, event_type: str, message: str, **payload: object
) -> None:
    db.add(
        JobEvent(
            investigation_id=investigation.id,
            event_type=event_type,
            stage=investigation.status.value,
            message=message,
            payload=payload,
        )
    )
    db.commit()


def _query_for_claim(claim: Claim) -> str:
    entities = " ".join(claim.entities[:4])
    return f'"{claim.normalized_text[:220]}" {entities}'.strip()


def _claim_terms(text: str) -> set[str]:
    words = re.findall(r"[\w\u0900-\u097F]{4,}", text.casefold())
    return {word for word, _ in Counter(words).most_common(16)}


def run_investigation(investigation_id: str) -> None:
    settings = get_settings()
    with SessionLocal() as db:
        investigation = db.get(Investigation, investigation_id)
        if not investigation or investigation.status == InvestigationStatus.cancelled:
            return
        try:
            gemini = GeminiProvider(settings)
            search = BraveSearchProvider(settings)
            fetcher = SafePageFetcher(settings)

            investigation.status = InvestigationStatus.extracting
            emit(db, investigation, "stage", "Extracting atomic claims and rhetoric spans.")
            extraction = gemini.extract(investigation.original_text, investigation.language)
            investigation.title = extraction.title
            investigation.language = extraction.detected_language
            for item in extraction.claims:
                db.add(
                    Claim(
                        investigation_id=investigation.id,
                        exact_text=item.exact_text,
                        normalized_text=item.normalized_text,
                        category=item.category,
                        start_offset=item.start_offset,
                        end_offset=item.end_offset,
                        entities=item.entities,
                        ambiguity=item.ambiguity,
                    )
                )
            bait_score, tag_points = score_bait_spans(extraction.bait_spans)
            investigation.bait_score = bait_score
            for span, points in zip(extraction.bait_spans, tag_points, strict=True):
                db.add(
                    BaitTag(
                        investigation_id=investigation.id,
                        technique=span.technique,
                        matched_text=span.matched_text,
                        start_offset=span.start_offset,
                        end_offset=span.end_offset,
                        severity=span.severity,
                        rubric_points=points,
                        explanation=span.explanation,
                    )
                )
            db.commit()
            emit(
                db,
                investigation,
                "claims",
                f"Found {len(extraction.claims)} checkable claim(s).",
                claim_count=len(extraction.claims),
            )

            investigation.status = InvestigationStatus.discovering
            emit(db, investigation, "stage", "Searching for independent public evidence.")
            claims = db.scalars(
                select(Claim).where(Claim.investigation_id == investigation.id)
            ).all()
            for claim in claims:
                if investigation.status == InvestigationStatus.cancelled:
                    return
                for search_result in search.search(_query_for_claim(claim)):
                    try:
                        page = fetcher.fetch(
                            str(search_result.url), _claim_terms(claim.normalized_text)
                        )
                    except (UnsafeUrlError, ProviderResponseError, httpx.HTTPError):
                        continue
                    source = db.scalar(
                        select(Source).where(Source.canonical_url == page.canonical_url)
                    )
                    if not source:
                        source = Source(
                            canonical_url=page.canonical_url,
                            title=page.title or search_result.title,
                            publisher=page.publisher,
                            publication_date=page.publication_date or search_result.published_at,
                            content_hash=page.content_hash,
                        )
                        db.add(source)
                        db.flush()
                    if db.scalar(
                        select(Evidence).where(
                            Evidence.claim_id == claim.id, Evidence.source_id == source.id
                        )
                    ):
                        continue
                    db.add(
                        Evidence(
                            claim_id=claim.id,
                            source_id=source.id,
                            passage=page.passage,
                            locator="extracted article passage",
                        )
                    )
                    db.commit()
                emit(
                    db,
                    investigation,
                    "source",
                    f"Processed sources for: {claim.normalized_text[:90]}",
                )

            investigation.status = InvestigationStatus.verifying
            emit(db, investigation, "stage", "Checking claims against retrieved passages.")
            verdicts: list[str] = []
            for claim in claims:
                db.refresh(claim)
                evidence_items = [
                    EvidenceForVerification(
                        evidence_id=item.id,
                        source_id=item.source.id,
                        url=item.source.canonical_url,
                        title=item.source.title,
                        passage=item.passage,
                    )
                    for item in claim.evidence
                ]
                if not evidence_items:
                    claim.verdict = Verdict.cannot_confirm
                    claim.explanation = "No retrievable evidence passage was found for this claim."
                    db.commit()
                    verdicts.append("Cannot Confirm")
                    continue
                verification = gemini.verify(claim.normalized_text, evidence_items)
                claim.verdict = verification.verdict
                claim.explanation = verification.explanation
                by_id = {item.id: item for item in claim.evidence}
                for assessment in verification.evidence_assessments:
                    evidence = by_id[assessment.evidence_id]
                    evidence.stance = assessment.stance
                    evidence.explanation = assessment.explanation
                db.commit()
                verdicts.append(verification.verdict.value)

            investigation.overall_conclusion = _overall_conclusion(verdicts)
            investigation.status = InvestigationStatus.complete
            emit(db, investigation, "complete", "Investigation completed with validated citations.")
        except ProviderConfigurationError as exc:
            investigation.status = InvestigationStatus.failed
            investigation.failure_code = "provider_not_configured"
            investigation.failure_message = str(exc)
            emit(db, investigation, "error", str(exc), code=investigation.failure_code)
        except Exception as exc:
            investigation.status = InvestigationStatus.failed
            investigation.failure_code = "pipeline_failed"
            investigation.failure_message = "The investigation could not be completed safely."
            emit(
                db, investigation, "error", investigation.failure_message, detail=type(exc).__name__
            )


def _overall_conclusion(verdicts: list[str]) -> str:
    if not verdicts:
        return "No checkable factual claims were identified."
    counts = Counter(verdicts)
    if len(counts) == 1:
        verdict = next(iter(counts))
        return f"All {len(verdicts)} assessed claim(s) were classified as {verdict}."
    summary = ", ".join(f"{count} {verdict}" for verdict, count in counts.items())
    return f"This forward contains mixed findings: {summary}. Review each claim and citation."
