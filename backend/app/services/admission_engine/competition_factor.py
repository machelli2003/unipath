"""
admission_engine/competition_factor.py

Adds a "competition factor" to the admission picture using
applicants_count / available_slots when that data exists in
cut_off_points. Deterministic ratio math — never estimated when data is
missing (returns None instead of guessing).
"""


def calculate_competition_factor(applicants_count: int | None, available_slots: int | None) -> dict:
    if not applicants_count or not available_slots or available_slots <= 0:
        return {"ratio": None, "level": "unknown", "data_complete": False}

    ratio = round(applicants_count / available_slots, 2)

    if ratio < 1.5:
        level = "low"
    elif ratio < 3:
        level = "moderate"
    elif ratio < 6:
        level = "high"
    else:
        level = "very_high"

    return {"ratio": ratio, "level": level, "data_complete": True}
