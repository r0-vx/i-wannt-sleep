from collections import defaultdict

from app.schemas import BaitSpanExtraction

POINTS_BY_SEVERITY = {"low": 4, "medium": 8, "high": 12}
CATEGORY_CAP = 20


def score_bait_spans(spans: list[BaitSpanExtraction]) -> tuple[int, list[int]]:
    """Score model-selected exact spans deterministically, capping each category at 20."""
    totals: dict[str, int] = defaultdict(int)
    points: list[int] = []
    seen: set[tuple[str, int, int]] = set()
    for span in spans:
        key = (span.technique, span.start_offset, span.end_offset)
        if key in seen:
            points.append(0)
            continue
        seen.add(key)
        available = CATEGORY_CAP - totals[span.technique]
        awarded = max(0, min(POINTS_BY_SEVERITY[span.severity], available))
        totals[span.technique] += awarded
        points.append(awarded)
    return min(100, sum(totals.values())), points
