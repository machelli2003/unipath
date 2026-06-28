"""
Interest fit helper for the recommendation engine.
"""
MAX_INTEREST_FIT_SCORE = 25.0


def calculate_interest_fit(student_interests: list[str], course_related_interests: list[str]) -> dict:
    if not course_related_interests:
        return {"score": MAX_INTEREST_FIT_SCORE * 0.5, "matched_interests": [], "data_complete": False}

    student_set = {i.strip().lower() for i in student_interests}
    course_set = {i.strip().lower() for i in course_related_interests}
    matched = student_set & course_set
    score = round((len(matched) / len(course_set)) * MAX_INTEREST_FIT_SCORE, 2) if course_set else 0.0
    matched_original = [i for i in course_related_interests if i.strip().lower() in matched]
    return {"score": score, "matched_interests": matched_original, "data_complete": True}
