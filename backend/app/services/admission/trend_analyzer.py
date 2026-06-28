"""
Analyses historical cut-off trends for a course.
Tells the student whether competition is rising, stable, or easing.
"""
from mongoengine import ConnectionFailure

from ...db.mongodb import get_db


class TrendAnalyzer:

    def get_trend(self, course_id: str) -> dict:
        try:
            db = get_db()
        except ConnectionFailure:
            return {
                "trend": "stable",
                "trend_label": "Stable",
                "history": [],
                "description": "Not enough historical data to determine trend.",
            }

        records = list(
            db.cut_off_points.find(
                {"course_id": course_id},
                sort=[("year", 1)],
            )
        )

        if len(records) < 2:
            return {
                "trend": "stable",
                "trend_label": "Stable",
                "history": [],
                "description": "Not enough historical data to determine trend.",
            }

        history = [{"year": r["year"], "aggregate": r["aggregate"]} for r in records]
        first = records[0]["aggregate"]
        last = records[-1]["aggregate"]
        delta = last - first

        if delta >= 3:
            trend = "rising"
            trend_label = "Getting More Competitive"
            description = (
                f"Cut-off has risen by {delta} points over the last {len(records)} years. Competition is increasing."
            )
        elif delta <= -3:
            trend = "easing"
            trend_label = "Getting Easier to Enter"
            description = (
                f"Cut-off has dropped by {abs(delta)} points over the last {len(records)} years. Competition is easing."
            )
        else:
            trend = "stable"
            trend_label = "Stable"
            description = "Cut-off has remained fairly consistent over recent years."

        return {
            "trend": trend,
            "trend_label": trend_label,
            "history": history,
            "description": description,
            "delta": delta,
        }
