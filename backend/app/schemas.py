from typing import Literal

from pydantic import BaseModel, Field, HttpUrl, model_validator

from app.models import EvidenceStance, InvestigationStatus, Verdict


class InvestigationCreate(BaseModel):
    text: str = Field(min_length=20, max_length=30_000)
    language: Literal["auto", "en", "hi", "mr"] = "auto"
    caption: str | None = Field(default=None, max_length=1_000)

    @model_validator(mode="after")
    def reject_blank_text(self) -> "InvestigationCreate":
        self.text = self.text.strip()
        if len(self.text) < 20:
            raise ValueError("Text must contain at least 20 non-space characters")
        return self


class InvestigationRename(BaseModel):
    title: str = Field(min_length=2, max_length=160)


class InvestigationSummary(BaseModel):
    id: str
    title: str
    input_type: str
    language: str
    status: InvestigationStatus
    overall_conclusion: str | None
    bait_score: int | None
    failure_code: str | None
    failure_message: str | None
    created_at: str
    updated_at: str


class ClaimExtraction(BaseModel):
    exact_text: str
    normalized_text: str
    category: str
    start_offset: int | None = None
    end_offset: int | None = None
    entities: list[str] = Field(default_factory=list)
    ambiguity: str | None = None
    checkable: bool = True


BaitTechnique = Literal[
    "artificial urgency",
    "authority appeal",
    "forwarding pressure",
    "emotional pressure",
    "scarcity/fear",
]


class BaitSpanExtraction(BaseModel):
    technique: BaitTechnique
    matched_text: str
    start_offset: int
    end_offset: int
    severity: Literal["low", "medium", "high"]
    explanation: str


class ExtractionResult(BaseModel):
    title: str = Field(max_length=160)
    detected_language: Literal["en", "hi", "mr", "other"]
    claims: list[ClaimExtraction]
    bait_spans: list[BaitSpanExtraction]


class SearchResult(BaseModel):
    url: HttpUrl
    title: str
    description: str = ""
    published_at: str | None = None


class EvidenceForVerification(BaseModel):
    evidence_id: str
    source_id: str
    url: str
    title: str
    passage: str


class EvidenceAssessment(BaseModel):
    evidence_id: str
    stance: EvidenceStance
    explanation: str


class VerificationResult(BaseModel):
    verdict: Verdict
    explanation: str
    evidence_assessments: list[EvidenceAssessment]
    missing_context: list[str] = Field(default_factory=list)


class ReportEvidence(BaseModel):
    id: str
    passage: str
    locator: str
    stance: EvidenceStance
    explanation: str | None
    source_id: str
    source_title: str
    source_url: str
    publisher: str | None
    publication_date: str | None
    retrieval_date: str


class ReportClaim(BaseModel):
    id: str
    exact_text: str
    normalized_text: str
    category: str
    verdict: Verdict | None
    explanation: str | None
    evidence: list[ReportEvidence]


class BaitTagView(BaseModel):
    id: str
    technique: str
    matched_text: str
    start_offset: int
    end_offset: int
    severity: str
    rubric_points: int
    explanation: str


class InvestigationReport(BaseModel):
    investigation: InvestigationSummary
    original_text: str
    claims: list[ReportClaim]
    bait_tags: list[BaitTagView]
    methodology_note: str


class GraphNode(BaseModel):
    id: str
    type: Literal["original", "claim", "source", "evidence", "verdict", "bait"]
    label: str
    record_id: str
    metadata: dict[str, str | int | None] = Field(default_factory=dict)


class GraphEdge(BaseModel):
    id: str
    source: str
    target: str
    relationship: str
    record_id: str


class InvestigationGraph(BaseModel):
    nodes: list[GraphNode]
    edges: list[GraphEdge]
