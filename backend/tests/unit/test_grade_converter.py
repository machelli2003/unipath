"""
tests/unit/test_grade_converter.py
"""

import pytest
from app.services.recommendation_engine.grade_converter import (
    grade_to_numeric,
    convert_subjects,
    calculate_aggregate,
)


def test_grade_to_numeric_valid():
    assert grade_to_numeric("A1") == 1
    assert grade_to_numeric("f9") == 9  # case-insensitive


def test_grade_to_numeric_invalid():
    with pytest.raises(ValueError):
        grade_to_numeric("Z9")


def test_convert_subjects():
    subjects = [{"subject_name": "Mathematics", "grade": "B2"}]
    converted = convert_subjects(subjects)
    assert converted[0]["numeric_value"] == 2
    assert converted[0]["original_grade"] == "B2"


def test_calculate_aggregate_best_six():
    converted = [
        {"subject_name": f"Subject{i}", "numeric_value": v}
        for i, v in enumerate([1, 2, 3, 4, 5, 6, 9, 9])
    ]
    # best 6 of [1,2,3,4,5,6,9,9] = [1,2,3,4,5,6] = sum 21
    assert calculate_aggregate(converted) == 21.0
