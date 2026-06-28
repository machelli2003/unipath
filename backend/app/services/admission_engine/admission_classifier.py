"""
admission_engine/admission_classifier.py

Final classification step of the Admission Intelligence System. Combines:
  - gap vs latest cut-off (cutoff_comparator.py)
  - historical trend (trend_analyzer.py)
  - competition factor (competition_factor.py)

...into one of three deterministic categories:
  🟢 Safe Choice
  🟡 Competitive Choice
  🔴 Reach Choice

Thresholds are explicit constants below — fully auditable, no AI judgment
call involved anywhere in this decision.
"""

from app.services.admission_engine.cutoff_comparator import compare_to_cutoff
from app.services.admission_engine.trend_analyzer import analyze_trend
from app.services.admission_engine.competition_factor import calculate_competition_factor

# Gap thresholds, in WASSCE aggregate points (lower aggregate = stronger).
SAFE_GAP_THRESHOLD = 3.0  # student beats cutoff by 3+ points -> Safe
REACH_GAP_THRESHOLD = -2.0  # student misses cutoff by 2+ points -> Reach


def classify_admission(
    student_aggregate: float,
    historical_cutoffs: list[dict],
) -> dict:
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

    # Base classification from the raw gap
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
