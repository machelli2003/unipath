"""
Academic fit helper for the recommendation engine.
"""
from app.services.recommendation_engine.grade_converter import to_score

MAX_ACADEMIC_FIT_SCORE = 40.0
CORE_SUBJECT_BONUS_MULTIPLIER = 1.5
ALWAYS_CORE_SUBJECTS = {"mathematics", "english language", "integrated science"}


def _subject_grade_score(numeric_grade: int, minimum_grade_numeric: int) -> float:
    if numeric_grade <= minimum_grade_numeric:
        improvement = minimum_grade_numeric - numeric_grade
        return min(1.0, 0.7 + (improvement * 0.05))
    gap = numeric_grade - minimum_grade_numeric
    return max(0.1, 0.7 - (gap * 0.15))


def calculate_academic_fit(student_subjects: list[dict], required_subjects: list[dict]) -> dict:
    if not required_subjects:
        return {"score": MAX_ACADEMIC_FIT_SCORE * 0.5, "subject_breakdown": [], "data_complete": False}

    student_lookup = {
        s["subject_name"].strip().lower(): s["numeric_value"] for s in student_subjects
    }
    total_weight = 0.0
    weighted_score_sum = 0.0
    breakdown = []

    for req in required_subjects:
        # Handle both string and dict representations of requirements
        if isinstance(req, str):
            continue  # Skip string-only entries, can't score
        subject_key = req["subject_name"].strip().lower()
        is_core = req.get("is_core") == "yes" or subject_key in ALWAYS_CORE_SUBJECTS
        weight = CORE_SUBJECT_BONUS_MULTIPLIER if is_core else 1.0
        min_grade_numeric = to_score(req["minimum_grade"])
        student_numeric = student_lookup.get(subject_key)

        if student_numeric is None:
            raw_score = 0.0
            met = False
        else:
            raw_score = _subject_grade_score(student_numeric, min_grade_numeric)
            met = student_numeric <= min_grade_numeric

        total_weight += weight
        weighted_score_sum += raw_score * weight
        breakdown.append(
            {
                "subject_name": req["subject_name"],
                "met": met,
                "is_core": is_core,
                "raw_score": round(raw_score, 3),
            }
        )

    fit_ratio = (weighted_score_sum / total_weight) if total_weight > 0 else 0.0
    return {"score": round(fit_ratio * MAX_ACADEMIC_FIT_SCORE, 2), "subject_breakdown": breakdown, "data_complete": True}
