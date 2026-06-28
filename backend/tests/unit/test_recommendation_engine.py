"""
tests/unit/test_recommendation_engine.py
"""

from app.services.recommendation_engine.engine import score_single_course


SAMPLE_COURSE = {
    "name": "Computer Science",
    "required_subjects": [
        {"subject_name": "Mathematics", "minimum_grade": "B3", "is_core": "yes"},
        {"subject_name": "English Language", "minimum_grade": "C6", "is_core": "yes"},
    ],
    "required_skills": ["Analytical Thinking", "Problem Solving"],
    "related_interests": ["Tech & Computing"],
    "related_career_goals": ["Software Engineer"],
}


def test_strong_student_scores_high():
    result = score_single_course(
        course=SAMPLE_COURSE,
        student_subjects=[
            {"subject_name": "Mathematics", "numeric_value": 1},
            {"subject_name": "English Language", "numeric_value": 2},
        ],
        student_interests=["Tech & Computing"],
        student_skills=[
            {"skill_name": "Analytical Thinking", "rating": 5},
            {"skill_name": "Problem Solving", "rating": 5},
        ],
        student_career_goals=["Software Engineer"],
    )
    assert result["match_score"] > 80
    assert "course_name" in result
    assert len(result["explanation_points"]) > 0


def test_weak_student_scores_low():
    result = score_single_course(
        course=SAMPLE_COURSE,
        student_subjects=[
            {"subject_name": "Mathematics", "numeric_value": 9},
            {"subject_name": "English Language", "numeric_value": 9},
        ],
        student_interests=["Arts"],
        student_skills=[
            {"skill_name": "Analytical Thinking", "rating": 1},
            {"skill_name": "Problem Solving", "rating": 1},
        ],
        student_career_goals=["Lawyer"],
    )
    assert result["match_score"] < 40


def test_score_breakdown_sums_to_match_score():
    result = score_single_course(
        course=SAMPLE_COURSE,
        student_subjects=[{"subject_name": "Mathematics", "numeric_value": 3}],
        student_interests=["Tech & Computing"],
        student_skills=[{"skill_name": "Analytical Thinking", "rating": 3}],
        student_career_goals=["Software Engineer"],
    )
    breakdown = result["score_breakdown"]
    total = (
        breakdown["academic_fit"]
        + breakdown["interest_fit"]
        + breakdown["skills_fit"]
        + breakdown["career_fit"]
    )
    assert round(total, 2) == result["match_score"]
