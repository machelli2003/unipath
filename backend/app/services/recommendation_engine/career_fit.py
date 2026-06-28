"""
recommendation_engine/career_fit.py

Career Fit (15% of total score): does this course lead to one of the
student's stated career goals? Deterministic boolean/overlap check.
"""

MAX_CAREER_FIT_SCORE = 15.0


def calculate_career_fit(
    student_career_goals: list[str],
    course_related_career_goals: list[str],
) -> dict:
    """
    score = (matched career goals / total student career goals) * 15

    If the student listed no career goals, return neutral midpoint and flag
    incompleteness rather than guessing.
    """
    if not student_career_goals:
        return {"score": MAX_CAREER_FIT_SCORE * 0.5, "matched_goals": [], "data_complete": False}

    student_set = {g.strip().lower() for g in student_career_goals}
    course_set = {g.strip().lower() for g in course_related_career_goals}

    matched = student_set & course_set
    ratio = len(matched) / len(student_set) if student_set else 0.0
    score = round(ratio * MAX_CAREER_FIT_SCORE, 2)

    matched_original_case = [
        g for g in student_career_goals if g.strip().lower() in matched
    ]

    return {"score": score, "matched_goals": matched_original_case, "data_complete": True}
