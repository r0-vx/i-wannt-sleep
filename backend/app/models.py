from __future__ import annotations

import enum
import uuid
from datetime import UTC, datetime

from sqlalchemy import JSON, DateTime, Enum, ForeignKey, Integer, String, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db import Base


def utcnow() -> datetime:
    return datetime.now(UTC)


class InvestigationStatus(enum.StrEnum):
    draft = "draft"
    queued = "queued"
    extracting = "extracting"
    discovering = "discovering"
    verifying = "verifying"
    complete = "complete"
    failed = "failed"
    cancelled = "cancelled"


class Verdict(enum.StrEnum):
    verified = "Verified"
    false = "False"
    outdated = "Outdated"
    partially_supported = "Partially Supported"
    cannot_confirm = "Cannot Confirm"


class EvidenceStance(enum.StrEnum):
    supports = "supports"
    contradicts = "contradicts"
    qualifies = "qualifies"
    context = "context"
    insufficient = "insufficient"


class Investigation(Base):
    __tablename__ = "investigations"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    owner_id: Mapped[str] = mapped_column(String(128), index=True)
    title: Mapped[str] = mapped_column(String(160), default="Untitled investigation")
    input_type: Mapped[str] = mapped_column(String(24), default="text")
    language: Mapped[str] = mapped_column(String(16), default="auto")
    original_text: Mapped[str] = mapped_column(Text)
    caption: Mapped[str | None] = mapped_column(Text, nullable=True)
    status: Mapped[InvestigationStatus] = mapped_column(
        Enum(InvestigationStatus), default=InvestigationStatus.draft, index=True
    )
    overall_conclusion: Mapped[str | None] = mapped_column(Text, nullable=True)
    bait_score: Mapped[int | None] = mapped_column(Integer, nullable=True)
    failure_code: Mapped[str | None] = mapped_column(String(80), nullable=True)
    failure_message: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utcnow, onupdate=utcnow
    )

    claims: Mapped[list[Claim]] = relationship(
        cascade="all, delete-orphan", back_populates="investigation"
    )
    bait_tags: Mapped[list[BaitTag]] = relationship(
        cascade="all, delete-orphan", back_populates="investigation"
    )
    events: Mapped[list[JobEvent]] = relationship(
        cascade="all, delete-orphan", back_populates="investigation"
    )


class Claim(Base):
    __tablename__ = "claims"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    investigation_id: Mapped[str] = mapped_column(
        ForeignKey("investigations.id", ondelete="CASCADE"), index=True
    )
    exact_text: Mapped[str] = mapped_column(Text)
    normalized_text: Mapped[str] = mapped_column(Text)
    category: Mapped[str] = mapped_column(String(80), default="general")
    start_offset: Mapped[int | None] = mapped_column(Integer, nullable=True)
    end_offset: Mapped[int | None] = mapped_column(Integer, nullable=True)
    entities: Mapped[list[str]] = mapped_column(JSON, default=list)
    ambiguity: Mapped[str | None] = mapped_column(Text, nullable=True)
    verdict: Mapped[Verdict | None] = mapped_column(Enum(Verdict), nullable=True)
    explanation: Mapped[str | None] = mapped_column(Text, nullable=True)

    investigation: Mapped[Investigation] = relationship(back_populates="claims")
    evidence: Mapped[list[Evidence]] = relationship(
        cascade="all, delete-orphan", back_populates="claim"
    )


class Source(Base):
    __tablename__ = "sources"
    __table_args__ = (UniqueConstraint("canonical_url", name="uq_source_canonical_url"),)

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    canonical_url: Mapped[str] = mapped_column(Text)
    title: Mapped[str] = mapped_column(Text)
    publisher: Mapped[str | None] = mapped_column(String(255), nullable=True)
    publication_date: Mapped[str | None] = mapped_column(String(40), nullable=True)
    retrieval_date: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)
    extraction_status: Mapped[str] = mapped_column(String(40), default="retrieved")
    content_hash: Mapped[str] = mapped_column(String(64), index=True)

    evidence: Mapped[list[Evidence]] = relationship(back_populates="source")


class Evidence(Base):
    __tablename__ = "evidence"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    claim_id: Mapped[str] = mapped_column(ForeignKey("claims.id", ondelete="CASCADE"), index=True)
    source_id: Mapped[str] = mapped_column(ForeignKey("sources.id", ondelete="CASCADE"), index=True)
    passage: Mapped[str] = mapped_column(Text)
    locator: Mapped[str] = mapped_column(String(255), default="page text")
    stance: Mapped[EvidenceStance] = mapped_column(
        Enum(EvidenceStance), default=EvidenceStance.context
    )
    relevance: Mapped[int] = mapped_column(Integer, default=0)
    explanation: Mapped[str | None] = mapped_column(Text, nullable=True)

    claim: Mapped[Claim] = relationship(back_populates="evidence")
    source: Mapped[Source] = relationship(back_populates="evidence")


class BaitTag(Base):
    __tablename__ = "bait_tags"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    investigation_id: Mapped[str] = mapped_column(
        ForeignKey("investigations.id", ondelete="CASCADE"), index=True
    )
    technique: Mapped[str] = mapped_column(String(60))
    matched_text: Mapped[str] = mapped_column(Text)
    start_offset: Mapped[int] = mapped_column(Integer)
    end_offset: Mapped[int] = mapped_column(Integer)
    severity: Mapped[str] = mapped_column(String(12))
    rubric_points: Mapped[int] = mapped_column(Integer)
    explanation: Mapped[str] = mapped_column(Text)

    investigation: Mapped[Investigation] = relationship(back_populates="bait_tags")


class JobEvent(Base):
    __tablename__ = "job_events"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    investigation_id: Mapped[str] = mapped_column(
        ForeignKey("investigations.id", ondelete="CASCADE"), index=True
    )
    event_type: Mapped[str] = mapped_column(String(40))
    stage: Mapped[str] = mapped_column(String(40))
    message: Mapped[str] = mapped_column(Text)
    payload: Mapped[dict[str, object]] = mapped_column(JSON, default=dict)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)

    investigation: Mapped[Investigation] = relationship(back_populates="events")
