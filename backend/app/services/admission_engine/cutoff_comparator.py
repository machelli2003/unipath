"""
admission_engine/cutoff_comparator.py

Compares a student's aggregate score against the LATEST cut-off on record
for a (university, course) pair. The cut-off number ALWAYS comes from the
cut_off_points collection (queried by routes/services and passed in here) —
this module never invents, estimates, or interpolates a cut-off value.

WASSCE aggregate convention: LOWER is better (A1=1 ... F9=9, so a lower sum
across best subjects = stronger performance).
"""


def compare_to_cutoff(student_aggregate: float, latest_cutoff_aggregate: int) -> dict:
    """
    Returns the raw gap and a simple deterministic flag. Categorization
    into Safe/Competitive/Reach happens in admission_classifier.py, which
    also factors in the competition_factor.
    """
    gap = latest_cutoff_aggregate - student_aggregate  # positive = student beats cutoff

    return {
        "student_aggregate": student_aggregate,
        "cutoff_aggregate": latest_cutoff_aggregate,
        "gap": round(gap, 2),
        "meets_cutoff": gap >= 0,
    }
