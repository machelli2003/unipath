"""
Recommendation Engine — orchestrates the full pipeline.
"""
from datetime import datetime
from bson import ObjectId

from ...db.mongodb import get_db
from .grade_converter import GradeConverter
from .scoring import ScoringEngine
from .explainer import Explainer
from .ranker import Ranker
from ..admission.cut_off_analyzer import CutOffAnalyzer
from ..admission.trend_analyzer import TrendAnalyzer


class RecommendationEngine:

    def __init__(self):
        self.scorer = ScoringEngine()
        self.explainer = Explainer()
        self.ranker = Ranker()
        self.cut_off = CutOffAnalyzer()
        self.trend = TrendAnalyzer()

    def run(self, profile: dict, save: bool = True) -> dict:
        db = get_db()

        grades = profile.get("wassce_subjects", {})
        aggregate = GradeConverter.compute_aggregate(grades)
        shs_prog = profile.get("shs_program", "Science")

        courses = list(db.courses.find({}))
        if not courses:
            return {"error": "No courses found in database. Run seed scripts first."}

        scored = []
        for course in courses:
            profile_for_scoring = {**profile, "grades": grades}
            scores = self.scorer.score_course(profile_for_scoring, course)
            admission = self.cut_off.analyze(course, aggregate)
            why = self.explainer.build_why_points(profile, course, scores, admission)
            summary = self.explainer.build_summary(course, scores, admission)

            scored.append(
                {
                    "course": course,
                    "scores": scores,
                    "admission": admission,
                    "why_points": why,
                    "summary": summary,
                }
            )

        top_results = self.ranker.rank_with_filter(scored, shs_prog, top_n=10)

        serialised = []
        for item in top_results:
            c = item["course"]
            serialised.append(
                {
                    "course_id": str(c["_id"]),
                    "course_name": c["name"],
                    "university": c.get("university_short", ""),
                    "category": c.get("category", ""),
                    "duration_years": c.get("duration_years", 4),
                    "difficulty": c.get("difficulty", "medium"),
                    "match_score": item["scores"]["total"],
                    "score_breakdown": item["scores"],
                    "admission_category": item["admission"]["admission_category"],
                    "admission_probability": item["admission"]["admission_probability"],
                    "cut_off_aggregate": item["admission"]["cut_off_aggregate"],
                    "student_aggregate": aggregate,
                    "gap": item["admission"]["gap"],
                    "why_points": item["why_points"],
                    "summary": item["summary"],
                    "career_paths": c.get("career_paths", []),
                    "professional_body": c.get("professional_body", ""),
                }
            )

        result = {
            "student_aggregate": aggregate,
            "shs_program": shs_prog,
            "mode": profile.get("mode", "official"),
            "top_courses": serialised,
            "generated_at": datetime.utcnow().isoformat(),
            "ai_summary": None,
        }

        if save:
            user_id = profile.get("user_id")
            if user_id:
                doc = {
                    "_id": ObjectId(),
                    "student_id": user_id,
                    "student_aggregate": aggregate,
                    "top_courses": serialised,
                    "generated_at": datetime.utcnow(),
                    "ai_summary": None,
                }
                db.recommendations.insert_one(doc)
                result["recommendation_id"] = str(doc["_id"])

        return result
