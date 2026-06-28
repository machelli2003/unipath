"""
Scoring engine for the recommendation pipeline.
"""
from .grade_converter import compute_aggregate, to_score
from .academic_fit import calculate_academic_fit
from .interest_fit import calculate_interest_fit
from .skills_fit import calculate_skills_fit
from .career_fit import calculate_career_fit


class ScoringEngine:

    def score_course(self, profile: dict, course: dict) -> dict:
        student_subjects = [
            {"subject_name": k, "numeric_value": to_score(v) if isinstance(v, str) else v}
            for k, v in profile.get("wassce_subjects", {}).items()
        ]
        academic_result = calculate_academic_fit(student_subjects, course.get("required_subjects", []))
        interest_result = calculate_interest_fit(profile.get("interests", []), course.get("interest_tags", []))
        skills_result = calculate_skills_fit(profile.get("skills", []), course.get("required_skills", []))
        career_result = calculate_career_fit(profile.get("career_goals", []), course.get("career_paths", []))

        total_score = round(
            academic_result["score"]
            + interest_result["score"]
            + skills_result["score"]
            + career_result["score"],
            2,
        )

        return {
            "total": total_score,
            "academic_fit": academic_result,
            "interest_fit": interest_result,
            "skills_fit": skills_result,
            "career_fit": career_result,
        }
