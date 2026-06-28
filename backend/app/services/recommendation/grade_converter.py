"""
Grade conversion utilities for the recommendation engine.
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

NUMERIC_TO_GRADE = {v: k for k, v in GRADE_TO_NUMERIC.items()}


def to_score(grade: str) -> int:
    grade = grade.strip().upper()
    if grade not in GRADE_TO_NUMERIC:
        raise ValueError(f"Invalid WASSCE grade '{grade}'")
    return GRADE_TO_NUMERIC[grade]


def compute_aggregate(grades: dict, best_n: int = 6) -> float:
    values = sorted([to_score(value) for value in grades.values()])
    best = values[:best_n] if len(values) >= best_n else values
    return float(sum(best))


class GradeConverter:
    @staticmethod
    def to_score(grade: str) -> int:
        return to_score(grade)

    @staticmethod
    def compute_aggregate(grades: dict, best_n: int = 6) -> float:
        return compute_aggregate(grades, best_n=best_n)
