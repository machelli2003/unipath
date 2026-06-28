"""
Career fit helper for the recommendation engine.
"""
MAX_CAREER_FIT_SCORE = 15.0


def calculate_career_fit(student_career_goals: list[str], course_related_career_goals: list[str]) -> dict:
    if not course_related_career_goals:
        return {"score": MAX_CAREER_FIT_SCORE * 0.5, "matched_careers": [], "data_complete": False}

    student_set = {c.strip().lower() for c in student_career_goals}
    course_set = {c.strip().lower() for c in course_related_career_goals}
    matched = student_set & course_set
    ratio = len(matched) / len(course_set) if course_set else 0.0
    score = round(ratio * MAX_CAREER_FIT_SCORE, 2)
    matched_original = [c for c in course_related_career_goals if c.strip().lower() in matched]
    return {"score": score, "matched_careers": matched_original, "data_complete": True}
