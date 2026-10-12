from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.models import Claim, Evidence, Investigation
from app.schemas import GraphEdge, GraphNode, InvestigationGraph


def build_graph(db: Session, investigation: Investigation) -> InvestigationGraph:
    claims = db.scalars(
        select(Claim)
        .where(Claim.investigation_id == investigation.id)
        .options(selectinload(Claim.evidence).selectinload(Evidence.source))
    ).all()
    nodes = [
        GraphNode(
            id=f"investigation:{investigation.id}",
            type="original",
            label=investigation.title,
            record_id=investigation.id,
        )
    ]
    edges: list[GraphEdge] = []
    seen_sources: set[str] = set()
    for claim in claims:
        claim_node = f"claim:{claim.id}"
        nodes.append(
            GraphNode(id=claim_node, type="claim", label=claim.normalized_text, record_id=claim.id)
        )
        edges.append(
            GraphEdge(
                id=f"contains:{claim.id}",
                source=f"investigation:{investigation.id}",
                target=claim_node,
                relationship="Contains Claim",
                record_id=claim.id,
            )
        )
        if claim.verdict:
            verdict_node = f"verdict:{claim.id}"
            nodes.append(
                GraphNode(
                    id=verdict_node,
                    type="verdict",
                    label=claim.verdict.value,
                    record_id=claim.id,
                )
            )
            edges.append(
                GraphEdge(
                    id=f"verdict-edge:{claim.id}",
                    source=claim_node,
                    target=verdict_node,
                    relationship="Has Verdict",
                    record_id=claim.id,
                )
            )
        for evidence in claim.evidence:
            evidence_node = f"evidence:{evidence.id}"
            source_node = f"source:{evidence.source.id}"
            nodes.append(
                GraphNode(
                    id=evidence_node,
                    type="evidence",
                    label=evidence.passage[:120],
                    record_id=evidence.id,
                    metadata={"stance": evidence.stance.value},
                )
            )
            if evidence.source.id not in seen_sources:
                seen_sources.add(evidence.source.id)
                nodes.append(
                    GraphNode(
                        id=source_node,
                        type="source",
                        label=evidence.source.title,
                        record_id=evidence.source.id,
                        metadata={"url": evidence.source.canonical_url},
                    )
                )
            edges.extend(
                [
                    GraphEdge(
                        id=f"claim-evidence:{evidence.id}",
                        source=claim_node,
                        target=evidence_node,
                        relationship={
                            "supports": "Supported By",
                            "contradicts": "Contradicted By",
                            "qualifies": "Qualified By",
                        }.get(evidence.stance.value, "Context From"),
                        record_id=evidence.id,
                    ),
                    GraphEdge(
                        id=f"evidence-source:{evidence.id}",
                        source=evidence_node,
                        target=source_node,
                        relationship="Extracted From",
                        record_id=evidence.id,
                    ),
                ]
            )
    for tag in investigation.bait_tags:
        tag_node = f"bait:{tag.id}"
        nodes.append(
            GraphNode(
                id=tag_node,
                type="bait",
                label=tag.technique,
                record_id=tag.id,
                metadata={"points": tag.rubric_points},
            )
        )
        edges.append(
            GraphEdge(
                id=f"bait-edge:{tag.id}",
                source=f"investigation:{investigation.id}",
                target=tag_node,
                relationship="Contains Bait Technique",
                record_id=tag.id,
            )
        )
    return InvestigationGraph(nodes=nodes, edges=edges)
