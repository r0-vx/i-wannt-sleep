from app.models import BaitTag, Claim, Evidence, Investigation, Source, Verdict
from app.services.graph import build_graph
from app.services.providers import UnsafeUrlError, _assert_public_host


def test_localhost_is_rejected_before_source_fetch() -> None:
    try:
        _assert_public_host("localhost")
    except UnsafeUrlError as exc:
        assert "Local addresses" in str(exc)
    else:
        raise AssertionError("localhost must never pass the SSRF address check")


def test_graph_edges_reference_real_persistent_nodes(database) -> None:
    from app.db import SessionLocal

    with SessionLocal() as db:
        investigation = Investigation(owner_id="owner", original_text="A sufficiently long claim")
        db.add(investigation)
        db.flush()
        claim = Claim(
            investigation_id=investigation.id,
            exact_text="A sufficiently long claim",
            normalized_text="A sufficiently long claim",
            verdict=Verdict.verified,
        )
        source = Source(
            canonical_url="https://example.com/source",
            title="Example source",
            content_hash="a" * 64,
        )
        db.add_all([claim, source])
        db.flush()
        evidence = Evidence(
            claim_id=claim.id,
            source_id=source.id,
            passage="This is the stored source passage supporting the example claim.",
        )
        tag = BaitTag(
            investigation_id=investigation.id,
            technique="artificial urgency",
            matched_text="urgent",
            start_offset=0,
            end_offset=6,
            severity="medium",
            rubric_points=8,
            explanation="Time pressure",
        )
        db.add_all([evidence, tag])
        db.commit()
        db.refresh(investigation)
        graph = build_graph(db, investigation)

    node_ids = {node.id for node in graph.nodes}
    record_ids = {node.record_id for node in graph.nodes}
    assert all(edge.source in node_ids and edge.target in node_ids for edge in graph.edges)
    assert all(edge.record_id in record_ids for edge in graph.edges)
