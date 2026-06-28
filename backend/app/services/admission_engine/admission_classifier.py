"""
admission_engine/admission_classifier.py

Deterministic admission classification for UniPath.

The simple rule set used by the platform is based on the gap between the
student's aggregate and the cut-off aggregate (lower is better):
  - safe: student aggregate <= cut-off - 3
  - competitive: student aggregate <= cut-off + 2
  - reach: student aggregate > cut-off + 2

The module also preserves the richer historical-cutoff workflow used by the
admission engine when a list of historical cut-offs is supplied.
"""

from __future__ import annotations

from typing import Union

from app.services.admission_engine.cutoff_comparator import compare_to_cutoff
from app.services.admission_engine.trend_analyzer import analyze_trend
from app.services.admission_engine.competition_factor import calculate_competition_factor

# Gap thresholds, in WASSCE aggregate points (lower aggregate = stronger).
SAFE_THRESHOLD = -3
COMPETITIVE_THRESHOLD = 2

# Legacy threshold names retained for compatibility with the historical engine.
SAFE_GAP_THRESHOLD = 3.0
REACH_GAP_THRESHOLD = -2.0


def classify_admission(
    student_aggregate: float,
    cut_off_aggregate_or_history: Union[int, float, list[dict]],
) -> Union[str, dict]:
    """
    Supports both simple aggregate-gap classification and the richer engine
    workflow based on a historical cut-off list.
    """
    if isinstance(cut_off_aggregate_or_history, (list, tuple)):
        return classify_admission_with_history(student_aggregate, cut_off_aggregate_or_history)

    gap = float(student_aggregate) - float(cut_off_aggregate_or_history)

    if gap <= SAFE_THRESHOLD:
        return "safe"
    if gap <= COMPETITIVE_THRESHOLD:
        return "competitive"
    return "reach"


def admission_probability(student_aggregate: int | float, cut_off_aggregate: int | float) -> int:
    """
    Returns an estimated admission probability (0-100%).
    Based on the gap between the student's aggregate and the cut-off.
    """
    gap = float(student_aggregate) - float(cut_off_aggregate)

    if gap <= -5:
        return 95
    if gap <= -3:
        return 85
    if gap <= -1:
        return 70
    if gap == 0:
        return 55
    if gap <= 2:
        return 35
    if gap <= 4:
        return 15
    return 5


def classify_admission_with_history(student_aggregate: float, historical_cutoffs: list[dict]) -> dict:
    """
    historical_cutoffs: list of {year, cut_off_aggregate, applicants_count?,
                                  available_slots?}, at least 1 entry required.
    """
    if not historical_cutoffs:
        return {
            "category": None,
            "reason": "No cut-off data available for this university/course pairing.",
            "data_complete": False,
        }

    latest = max(historical_cutoffs, key=lambda d: d["year"])
    comparison = compare_to_cutoff(student_aggregate, latest["cut_off_aggregate"])
    trend = analyze_trend(historical_cutoffs)
    competition = calculate_competition_factor(
        latest.get("applicants_count"), latest.get("available_slots")
    )

    gap = comparison["gap"]

    # Base classification from the raw gap.
    if gap >= SAFE_GAP_THRESHOLD:
        category = "Safe Choice"
    elif gap <= REACH_GAP_THRESHOLD:
        category = "Reach Choice"
    else:
        category = "Competitive Choice"

    # Trend/competition can push a borderline case one notch, but never
    # override a clear Safe or clear Reach — keeps the rule auditable.
    is_borderline = REACH_GAP_THRESHOLD < gap < SAFE_GAP_THRESHOLD
    if is_borderline:
        if trend["direction"] == "rising_competition" or competition.get("level") in (
            "high",
            "very_high",
        ):
            category = "Reach Choice" if gap < 0 else "Competitive Choice"
        elif trend["direction"] == "easing_competition" and competition.get("level") in (
            "low",
            "moderate",
            "unknown",
        ):
            category = "Safe Choice" if gap >= 0 else "Competitive Choice"

    return {
        "category": category,
        "comparison": comparison,
        "trend": trend,
        "competition": competition,
        "latest_cutoff_year": latest["year"],
        "data_complete": True,
    }
