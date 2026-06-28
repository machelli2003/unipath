"""
recommendation_engine/grade_converter.py

STEP 1 of the recommendation flow: Grade Conversion System.

Purely deterministic lookup table. No AI, no estimation. This module is the
ONLY place in the codebase that should define the WASSCE grade -> numeric
mapping, so it stays single-sourced.
"""

GRADE_TO_NUMERIC = {
    "A1": 1,
    "B2": 2,
    "B3": 3,
    "C4": 4,
    "C5": 5,
    "C6": 6,
    "D7": 7,
    "E8": 8,
    "F9": 9,
}

# Inverse lookup, useful for displaying "numeric -> nearest grade" in the
# What-If Simulator UI.
NUMERIC_TO_GRADE = {v: k for k, v in GRADE_TO_NUMERIC.items()}


def grade_to_numeric(grade: str) -> int:
    """Convert a single WASSCE letter grade to its numeric value (1=best, 9=worst)."""
    grade = grade.strip().upper()
    if grade not in GRADE_TO_NUMERIC:
        raise ValueError(
            f"Invalid WASSCE grade '{grade}'. Must be one of: "
            f"{', '.join(GRADE_TO_NUMERIC.keys())}"
        )
    return GRADE_TO_NUMERIC[grade]


def convert_subjects(subjects: list[dict]) -> list[dict]:
    """
    Convert a list of {subject_name, grade} dicts into
    {subject_name, original_grade, numeric_value} dicts.
    """
    converted = []
    for subj in subjects:
        converted.append(
            {
                "subject_name": subj["subject_name"],
                "original_grade": subj["grade"],
                "numeric_value": grade_to_numeric(subj["grade"]),
            }
        )
    return converted


def calculate_aggregate(converted_subjects: list[dict], best_n: int = 6) -> float:
    """
    WASSCE-style aggregate: sum of the numeric values of the student's best
    `best_n` subjects (lower aggregate = stronger academic performance).
    """
    values = sorted(s["numeric_value"] for s in converted_subjects)
    best = values[:best_n] if len(values) >= best_n else values
    return float(sum(best))
