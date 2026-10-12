from __future__ import annotations

import asyncio
import json
from collections.abc import AsyncIterator

from fastapi import APIRouter, BackgroundTasks, Depends, Header, HTTPException, Query, status
from fastapi.responses import StreamingResponse
from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.db import SessionLocal, get_db
from app.models import Claim, Evidence, Investigation, InvestigationStatus, JobEvent
from app.schemas import (
    BaitTagView,
    InvestigationCreate,
    InvestigationGraph,
    InvestigationRename,
    InvestigationReport,
    InvestigationSummary,
    ReportClaim,
    ReportEvidence,
)
from app.services.graph import build_graph
from app.services.pipeline import emit, run_investigation

router = APIRouter(prefix="/api/v1/investigations", tags=["investigations"])


def owner_id(x_forwardcheck_session: str = Header(min_length=20, max_length=128)) -> str:
    return x_forwardcheck_session


def summary(item: Investigation) -> InvestigationSummary:
    return InvestigationSummary(
        id=item.id,
        title=item.title,
        input_type=item.input_type,
        language=item.language,
        status=item.status,
        overall_conclusion=item.overall_conclusion,
        bait_score=item.bait_score,
        failure_code=item.failure_code,
        failure_message=item.failure_message,
        created_at=item.created_at.isoformat(),
        updated_at=item.updated_at.isoformat(),
    )


def owned(db: Session, investigation_id: str, owner: str) -> Investigation:
    item = db.scalar(
        select(Investigation).where(
            Investigation.id == investigation_id, Investigation.owner_id == owner
        )
    )
    if not item:
        raise HTTPException(status_code=404, detail="Investigation not found")
    return item


@router.post("", response_model=InvestigationSummary, status_code=status.HTTP_201_CREATED)
def create_investigation(
    payload: InvestigationCreate,
    owner: str = Depends(owner_id),
    db: Session = Depends(get_db),
) -> InvestigationSummary:
    item = Investigation(
        owner_id=owner,
        original_text=payload.text,
        language=payload.language,
        caption=payload.caption,
        title=payload.text.splitlines()[0][:80],
    )
    db.add(item)
    db.commit()
    db.refresh(item)
    emit(db, item, "created", "Investigation saved. Verification has not started.")
    return summary(item)


@router.get("", response_model=list[InvestigationSummary])
def list_investigations(
    limit: int = Query(default=20, ge=1, le=100),
    owner: str = Depends(owner_id),
    db: Session = Depends(get_db),
) -> list[InvestigationSummary]:
    items = db.scalars(
        select(Investigation)
        .where(Investigation.owner_id == owner)
        .order_by(Investigation.created_at.desc())
        .limit(limit)
    ).all()
    return [summary(item) for item in items]


@router.post("/{investigation_id}/verify", response_model=InvestigationSummary)
def verify_investigation(
    investigation_id: str,
    background_tasks: BackgroundTasks,
    owner: str = Depends(owner_id),
    db: Session = Depends(get_db),
) -> InvestigationSummary:
    item = owned(db, investigation_id, owner)
    if item.status not in {InvestigationStatus.draft, InvestigationStatus.failed}:
        raise HTTPException(status_code=409, detail="Investigation is already running or complete")
    item.status = InvestigationStatus.queued
    item.failure_code = None
    item.failure_message = None
    emit(db, item, "queued", "Investigation queued for processing.")
    background_tasks.add_task(run_investigation, item.id)
    return summary(item)


@router.get("/{investigation_id}/status", response_model=InvestigationSummary)
def get_status(
    investigation_id: str,
    owner: str = Depends(owner_id),
    db: Session = Depends(get_db),
) -> InvestigationSummary:
    return summary(owned(db, investigation_id, owner))


@router.post("/{investigation_id}/cancel", response_model=InvestigationSummary)
def cancel_investigation(
    investigation_id: str,
    owner: str = Depends(owner_id),
    db: Session = Depends(get_db),
) -> InvestigationSummary:
    item = owned(db, investigation_id, owner)
    if item.status in {InvestigationStatus.complete, InvestigationStatus.failed}:
        raise HTTPException(status_code=409, detail="A finished investigation cannot be cancelled")
    item.status = InvestigationStatus.cancelled
    emit(db, item, "cancelled", "Cancellation requested by the user.")
    return summary(item)


@router.patch("/{investigation_id}", response_model=InvestigationSummary)
def rename_investigation(
    investigation_id: str,
    payload: InvestigationRename,
    owner: str = Depends(owner_id),
    db: Session = Depends(get_db),
) -> InvestigationSummary:
    item = owned(db, investigation_id, owner)
    item.title = payload.title.strip()
    db.commit()
    db.refresh(item)
    return summary(item)


@router.delete("/{investigation_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_investigation(
    investigation_id: str,
    owner: str = Depends(owner_id),
    db: Session = Depends(get_db),
) -> None:
    item = owned(db, investigation_id, owner)
    if item.status in {
        InvestigationStatus.queued,
        InvestigationStatus.extracting,
        InvestigationStatus.discovering,
        InvestigationStatus.verifying,
    }:
        raise HTTPException(
            status_code=409, detail="Cancel the active investigation before deletion"
        )
    db.delete(item)
    db.commit()


@router.get("/{investigation_id}/events")
async def events(
    investigation_id: str,
    owner: str = Depends(owner_id),
    after: int = Query(default=0, ge=0),
) -> StreamingResponse:
    with SessionLocal() as db:
        owned(db, investigation_id, owner)

    async def stream() -> AsyncIterator[str]:
        last_id = after
        idle_ticks = 0
        while True:
            with SessionLocal() as session:
                event_items = session.scalars(
                    select(JobEvent)
                    .where(
                        JobEvent.investigation_id == investigation_id,
                        JobEvent.id > last_id,
                    )
                    .order_by(JobEvent.id)
                ).all()
                item = session.get(Investigation, investigation_id)
            if event_items:
                idle_ticks = 0
                for event in event_items:
                    last_id = event.id
                    body = {
                        "id": event.id,
                        "type": event.event_type,
                        "stage": event.stage,
                        "message": event.message,
                        "payload": event.payload,
                        "createdAt": event.created_at.isoformat(),
                    }
                    yield f"id: {event.id}\nevent: progress\ndata: {json.dumps(body)}\n\n"
            else:
                idle_ticks += 1
            if (
                item
                and item.status
                in {
                    InvestigationStatus.complete,
                    InvestigationStatus.failed,
                    InvestigationStatus.cancelled,
                }
                and not event_items
            ):
                break
            if idle_ticks >= 20:
                yield ": keep-alive\n\n"
                idle_ticks = 0
            await asyncio.sleep(0.75)

    return StreamingResponse(
        stream(),
        media_type="text/event-stream",
        headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"},
    )


@router.get("/{investigation_id}/report", response_model=InvestigationReport)
def report(
    investigation_id: str,
    owner: str = Depends(owner_id),
    db: Session = Depends(get_db),
) -> InvestigationReport:
    item = db.scalar(
        select(Investigation)
        .where(Investigation.id == investigation_id, Investigation.owner_id == owner)
        .options(
            selectinload(Investigation.claims)
            .selectinload(Claim.evidence)
            .selectinload(Evidence.source),
            selectinload(Investigation.bait_tags),
        )
    )
    if not item:
        raise HTTPException(status_code=404, detail="Investigation not found")
    return InvestigationReport(
        investigation=summary(item),
        original_text=item.original_text,
        claims=[
            ReportClaim(
                id=claim.id,
                exact_text=claim.exact_text,
                normalized_text=claim.normalized_text,
                category=claim.category,
                verdict=claim.verdict,
                explanation=claim.explanation,
                evidence=[
                    ReportEvidence(
                        id=evidence.id,
                        passage=evidence.passage,
                        locator=evidence.locator,
                        stance=evidence.stance,
                        explanation=evidence.explanation,
                        source_id=evidence.source.id,
                        source_title=evidence.source.title,
                        source_url=evidence.source.canonical_url,
                        publisher=evidence.source.publisher,
                        publication_date=evidence.source.publication_date,
                        retrieval_date=evidence.source.retrieval_date.isoformat(),
                    )
                    for evidence in claim.evidence
                ],
            )
            for claim in item.claims
        ],
        bait_tags=[
            BaitTagView(
                id=tag.id,
                technique=tag.technique,
                matched_text=tag.matched_text,
                start_offset=tag.start_offset,
                end_offset=tag.end_offset,
                severity=tag.severity,
                rubric_points=tag.rubric_points,
                explanation=tag.explanation,
            )
            for tag in item.bait_tags
        ],
        methodology_note=(
            "Verdicts are generated only from stored passages retrieved from public sources. "
            "The Bait Index is a rhetoric heuristic, not a probability that content is false."
        ),
    )


@router.get("/{investigation_id}/graph")
def graph(
    investigation_id: str,
    owner: str = Depends(owner_id),
    db: Session = Depends(get_db),
) -> InvestigationGraph:
    item = db.scalar(
        select(Investigation)
        .where(Investigation.id == investigation_id, Investigation.owner_id == owner)
        .options(selectinload(Investigation.bait_tags))
    )
    if not item:
        raise HTTPException(status_code=404, detail="Investigation not found")
    return build_graph(db, item)
