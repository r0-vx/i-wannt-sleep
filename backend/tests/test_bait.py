from app.schemas import BaitSpanExtraction
from app.services.bait import score_bait_spans


def span(technique: str, start: int, severity: str = "high") -> BaitSpanExtraction:
    return BaitSpanExtraction(
        technique=technique,
        matched_text="urgent",
        start_offset=start,
        end_offset=start + 6,
        severity=severity,
        explanation="Test fixture",
    )


def test_true_urgent_message_can_score_high_without_becoming_a_verdict() -> None:
    score, points = score_bait_spans(
        [
            span("artificial urgency", 0),
            span("artificial urgency", 10),
            span("emotional pressure", 20),
            span("forwarding pressure", 30),
        ]
    )
    assert score == 44
    assert points == [12, 8, 12, 12]


def test_duplicate_span_is_not_double_counted() -> None:
    duplicate = span("scarcity/fear", 0)
    score, points = score_bait_spans([duplicate, duplicate])
    assert score == 12
    assert points == [12, 0]


def test_calm_falsehood_can_score_zero() -> None:
    score, points = score_bait_spans([])
    assert score == 0
    assert points == []
