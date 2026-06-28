"""
Looks up the latest cut-off for a course at a university
and compares it against the student's aggregate.
"""
from mongoengine import ConnectionFailure

from ...db.mongodb import get_db
from .classifier import classify_admission, admission_probability


class CutOffAnalyzer:

    def get_latest_cut_off(self, course_id: str) -> dict | None:
        """
        Returns the most recent cut-off record for a course.
        """
        try:
            db = get_db()
        except ConnectionFailure:
            return None

        record = db.cut_off_points.find_one(
            {"course_id": course_id},
            sort=[("year", -1)],
        )
        return record

    def analyze(self, course: dict, student_aggregate: int) -> dict:
        """
        Returns full admission analysis for one course.
        """
        course_id = str(course["_id"])
        cut_off_rec = self.get_latest_cut_off(course_id)

        # Fall back to the embedded cut_off_2025 if no record found
        if cut_off_rec:
            cut_off_agg = cut_off_rec["aggregate"]
            cut_off_year = cut_off_rec["year"]
        else:
            cut_off_agg = course.get("cut_off_2025", 24)
            cut_off_year = 2025

        category = classify_admission(student_aggregate, cut_off_agg)
        probability = admission_probability(student_aggregate, cut_off_agg)
        gap = student_aggregate - cut_off_agg

        return {
            "cut_off_aggregate": cut_off_agg,
            "cut_off_year": cut_off_year,
            "student_aggregate": student_aggregate,
            "gap": gap,
            "admission_category": category,
            "admission_probability": probability,
        }
