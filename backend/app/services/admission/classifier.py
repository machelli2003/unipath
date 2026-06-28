SAFE_THRESHOLD        = -3   # student is 3+ points better than cut-off
COMPETITIVE_THRESHOLD =  2   # student is within 2 points of cut-off


def classify_admission(student_aggregate: int, cut_off_aggregate: int) -> str:
    """
    Returns 'safe', 'competitive', or 'reach'.
    """
    gap = student_aggregate - cut_off_aggregate  # negative = student is better

    if gap <= SAFE_THRESHOLD:
        return "safe"
    elif gap <= COMPETITIVE_THRESHOLD:
        return "competitive"
    else:
        return "reach"


def admission_probability(student_aggregate: int, cut_off_aggregate: int) -> int:
    """
    Returns an estimated admission probability (0-100%).
    Based on gap between student aggregate and cut-off.
    """
    gap = student_aggregate - cut_off_aggregate

    if gap <= -5:
        return 95
    if gap <= -3:
        return 85
    if gap <= -1:
        return 70
    if gap == 0:
        return 55
    if gap <= 2:
        return 35
    if gap <= 4:
        return 15
    return 5
