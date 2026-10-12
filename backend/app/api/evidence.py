from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.investigations import owner_id
from app.db import get_db
from app.models import Claim, Evidence, Investigation, Source

router = APIRouter(prefix="/api/v1/evidence", tags=["evidence"])


@router.get("")
def list_evidence(
    owner: str = Depends(owner_id),
    db: Session = Depends(get_db),
) -> list[dict[str, object]]:
    rows = db.execute(
        select(Evidence, Source, Claim, Investigation)
        .join(Source, Source.id == Evidence.source_id)
        .join(Claim, Claim.id == Evidence.claim_id)
        .join(Investigation, Investigation.id == Claim.investigation_id)
        .where(Investigation.owner_id == owner)
        .order_by(Source.retrieval_date.desc())
        .limit(200)
    ).all()
    return [
        {
            "id": evidence.id,
            "claimId": claim.id,
            "investigationId": investigation.id,
            "claim": claim.normalized_text,
            "passage": evidence.passage,
            "stance": evidence.stance.value,
            "sourceTitle": source.title,
            "sourceUrl": source.canonical_url,
            "publisher": source.publisher,
            "retrievedAt": source.retrieval_date.isoformat(),
        }
        for evidence, source, claim, investigation in rows
    ]
