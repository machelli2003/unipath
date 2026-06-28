"""Thin wrapper for comparison helpers used by the compare routes."""

from typing import Any, Dict, List, Optional


class ComparisonService:
    """Minimal compatibility service for the compare endpoints."""

    def compare_courses(self, courses: List[Dict[str, Any]], aggregate: Optional[float] = None) -> Dict[str, Any]:
        return {
            "courses": courses,
            "student_aggregate": aggregate,
        }

    def compare_universities(self, universities: List[Dict[str, Any]]) -> Dict[str, Any]:
        return {
            "universities": universities,
        }
