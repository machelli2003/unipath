"""
recommendation_engine/interest_fit.py

Interest Fit (25% of total score): how well a course's related_interests
overlap with the student's selected interests. Deterministic set-overlap
calculation — no AI involved.
"""

MAX_INTEREST_FIT_SCORE = 25.0


def calculate_interest_fit(
    student_interests: list[str],
    course_related_interests: list[str],
) -> dict:
    """
    Simple, explainable overlap scoring:
        score = (matched interests / total course-related interests) * 25

    If the course has no related_interests on record, return a neutral
    midpoint rather than 0 (an empty requirement isn't the student's fault)
    and flag data_complete = False so the UI/explanation layer is honest
    about it.
    """
    if not course_related_interests:
        return {"score": MAX_INTEREST_FIT_SCORE * 0.5, "matched_interests": [], "data_complete": False}

    student_set = {i.strip().lower() for i in student_interests}
    course_set = {i.strip().lower() for i in course_related_interests}

    matched = student_set & course_set
    ratio = len(matched) / len(course_set) if course_set else 0.0
    score = round(ratio * MAX_INTEREST_FIT_SCORE, 2)

    # Recover original-cased names for matched interests (for nicer explanations)
    matched_original_case = [
        i for i in course_related_interests if i.strip().lower() in matched
    ]

    return {"score": score, "matched_interests": matched_original_case, "data_complete": True}
