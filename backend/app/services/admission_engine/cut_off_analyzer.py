"""
admission_engine/cut_off_analyzer.py

Looks up the latest cut-off for a course and compares it against the
student's aggregate.
"""

from datetime import datetime
from app.models.cut_off_point import CutOffPoint
from .admission_classifier import classify_admission, admission_probability


class CutOffAnalyzer:

    def get_latest_cut_off(self, course_name: str) -> dict | None:
        """
        Returns the most recent cut-off record for a course.
        """
        record = CutOffPoint.objects(course_name=course_name).order_by('-year').first()
        return record

    def analyze(self, course: dict, student_aggregate: int) -> dict:
        """
        Returns full admission analysis for one course.
        """
        course_name = course.get("name")
        cut_off_rec = self.get_latest_cut_off(course_name)

        if cut_off_rec:
            cut_off_agg = cut_off_rec.cut_off_aggregate
            cut_off_year = cut_off_rec.year
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
