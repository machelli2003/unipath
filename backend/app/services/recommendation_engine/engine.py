"""
recommendation_engine/engine.py

Main orchestrator for the recommendation engine. This is the ONLY function
the rest of the app (routes/services) should call to get course
recommendations — it composes the individual deterministic scorers and
guarantees the weighting from the spec:

    Academic Fit  -> 40%
    Interest Fit  -> 25%
    Skills Fit    -> 20%
    Career Fit    -> 15%
                     ----
                     100%

No AI calls happen in this file. AI is invoked separately, downstream, only
to rephrase the explanation_points this engine already produced.
"""

from app.services.recommendation_engine.academic_fit import calculate_academic_fit
from app.services.recommendation_engine.interest_fit import calculate_interest_fit
from app.services.recommendation_engine.skills_fit import calculate_skills_fit
from app.services.recommendation_engine.career_fit import calculate_career_fit
from app.services.recommendation_engine.explanation_generator import (
    generate_explanation_points,
)

TOP_N_RESULTS = 10


def score_single_course(
    course: dict,
    student_subjects: list[dict],
    student_interests: list[str],
    student_skills: list[dict],
    student_career_goals: list[str],
) -> dict:
    """
    Score one course against one student profile.

    course: a course document (dict) with required_subjects,
            required_skills, related_interests, related_career_goals
    """
    academic_result = calculate_academic_fit(
        student_subjects, course.get("required_subjects", [])
    )
    interest_result = calculate_interest_fit(
        student_interests, course.get("related_interests", [])
    )
    skills_result = calculate_skills_fit(
        student_skills, course.get("required_skills", [])
    )
    career_result = calculate_career_fit(
        student_career_goals, course.get("related_career_goals", [])
    )

    total_score = round(
        academic_result["score"]
        + interest_result["score"]
        + skills_result["score"]
        + career_result["score"],
        2,
    )

    explanation_points = generate_explanation_points(
        course["name"], academic_result, interest_result, skills_result, career_result
    )

    return {
        "course_name": course["name"],
        "match_score": total_score,
        "score_breakdown": {
            "academic_fit": academic_result["score"],
            "interest_fit": interest_result["score"],
            "skills_fit": skills_result["score"],
            "career_fit": career_result["score"],
        },
        "explanation_points": explanation_points,
        "data_completeness": {
            "academic": academic_result.get("data_complete", True),
            "interest": interest_result.get("data_complete", True),
            "skills": skills_result.get("data_complete", True),
            "career": career_result.get("data_complete", True),
        },
    }


def generate_recommendations(
    all_courses: list[dict],
    student_subjects: list[dict],
    student_interests: list[str],
    student_skills: list[dict],
    student_career_goals: list[str],
    top_n: int = TOP_N_RESULTS,
) -> list[dict]:
    """
    STEP 2-4 of the recommendation flow:
      - Evaluate all courses
      - Apply weighted scoring
      - Rank results
      - Return top N (default 10)

    NOTE: Cut-off comparison / admission category (Safe/Competitive/Reach)
    is intentionally NOT done here — that's the Admission Intelligence
    System's job (see admission_engine/). This function answers "which
    courses fit you," not "will you get in."
    """
    scored = [
        score_single_course(
            course,
            student_subjects,
            student_interests,
            student_skills,
            student_career_goals,
        )
        for course in all_courses
    ]

    scored.sort(key=lambda r: r["match_score"], reverse=True)
    return scored[:top_n]
