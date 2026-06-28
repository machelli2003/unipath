"""
admission_engine/trend_analyzer.py

Historical trend analysis across multiple years of cut-off data for a
(university, course) pair. Pure arithmetic on DB-sourced numbers — no
forecasting model, no AI. Trend direction is informational context for the
student, not a prediction engine.
"""


def analyze_trend(historical_cutoffs: list[dict]) -> dict:
    """
    historical_cutoffs: list of {year, cut_off_aggregate}, any order.

    Returns direction ("rising_competition" means cut-off aggregate is
    DROPPING year over year, i.e. getting harder to meet, since lower
    aggregate = better in the WASSCE scale) and the simple year-over-year
    deltas, with no assumptions made beyond the recorded data points.
    """
    if len(historical_cutoffs) < 2:
        return {
            "direction": "insufficient_data",
            "deltas": [],
            "note": "Need at least 2 years of cut-off data for trend analysis.",
        }

    sorted_data = sorted(historical_cutoffs, key=lambda d: d["year"])
    deltas = []
    for prev, curr in zip(sorted_data, sorted_data[1:]):
        deltas.append(
            {
                "from_year": prev["year"],
                "to_year": curr["year"],
                "change": curr["cut_off_aggregate"] - prev["cut_off_aggregate"],
            }
        )

    avg_change = sum(d["change"] for d in deltas) / len(deltas)

    if avg_change < -0.5:
        direction = "rising_competition"  # cutoff aggregate falling = harder
    elif avg_change > 0.5:
        direction = "easing_competition"  # cutoff aggregate rising = easier
    else:
        direction = "stable"

    return {"direction": direction, "deltas": deltas, "average_yearly_change": round(avg_change, 2)}
