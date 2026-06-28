"""
recommendation_engine/academic_fit.py

STEP 3 of the recommendation flow: Academic Fit Logic (40% of total score).

Rules (per spec):
  - Match required subjects for the course
  - Penalize weak grades in core subjects
  - Strong weighting for Mathematics, English, and Science

Fully deterministic: every number produced here can be traced back to a
simple, auditable rule. No ML, no AI guessing.
"""

CORE_SUBJECT_BONUS_MULTIPLIER = 1.5  # core subjects count 1.5x in fit calc
MAX_ACADEMIC_FIT_SCORE = 40.0

# Subjects that always count as "core" regardless of course, per spec.
ALWAYS_CORE_SUBJECTS = {"mathematics", "english language", "integrated science"}


def _subject_grade_score(numeric_grade: int, minimum_grade_numeric: int) -> float:
    """
    Score a single subject 0.0-1.0 based on how the student's grade compares
    to the course's minimum required grade.

    - Meets or beats requirement -> scaled score based on how much it beats it
    - Fails requirement -> steep penalty (not zero, to avoid cliff-edge harshness,
      but still clearly worse)
    """
    if numeric_grade <= minimum_grade_numeric:
        # At or better than required. Reward strength beyond the minimum,
        # capped at 1.0 (e.g. requiring C6 but scoring A1 = full marks).
        improvement = minimum_grade_numeric - numeric_grade
        return min(1.0, 0.7 + (improvement * 0.05))
    else:
        # Did not meet requirement: linear penalty, floor at 0.1 so it's
        # never "as if the subject didn't exist."
        gap = numeric_grade - minimum_grade_numeric
        return max(0.1, 0.7 - (gap * 0.15))


def calculate_academic_fit(
    student_subjects: list[dict],
    required_subjects: list[dict],
) -> dict:
    """
    student_subjects: [{subject_name, numeric_value}]
    required_subjects: [{subject_name, minimum_grade (letter), is_core}]

    Returns:
        {
            "score": float (0-40),
            "subject_breakdown": [
                {"subject_name", "met": bool, "weight", "raw_score"}
            ]
        }
    """
    from app.services.recommendation_engine.grade_converter import grade_to_numeric

    if not required_subjects:
        # No specific requirements on record -> neutral mid-score, never
        # invented/guessed. Flagged explicitly so the UI can show
        # "general requirement data unavailable" rather than a fake number.
        return {"score": MAX_ACADEMIC_FIT_SCORE * 0.5, "subject_breakdown": [], "data_complete": False}

    student_lookup = {
        s["subject_name"].strip().lower(): s["numeric_value"] for s in student_subjects
    }

    total_weight = 0.0
    weighted_score_sum = 0.0
    breakdown = []

    for req in required_subjects:
        subject_key = req["subject_name"].strip().lower()
        is_core = req.get("is_core") == "yes" or subject_key in ALWAYS_CORE_SUBJECTS
        weight = CORE_SUBJECT_BONUS_MULTIPLIER if is_core else 1.0

        min_grade_numeric = grade_to_numeric(req["minimum_grade"])
        student_numeric = student_lookup.get(subject_key)

        if student_numeric is None:
            # Student didn't take this subject at all -> heaviest penalty
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
    score = round(fit_ratio * MAX_ACADEMIC_FIT_SCORE, 2)

    return {"score": score, "subject_breakdown": breakdown, "data_complete": True}
