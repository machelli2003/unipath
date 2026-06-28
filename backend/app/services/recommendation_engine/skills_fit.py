"""
recommendation_engine/skills_fit.py

Skills Fit (20% of total score): compares the student's self-rated skills
(1-5 scale) against a course's required_skills list. Deterministic average
of normalized ratings — no AI involved.
"""

MAX_SKILLS_FIT_SCORE = 20.0
MAX_SELF_RATING = 5.0


def calculate_skills_fit(
    student_skills: list[dict],
    course_required_skills: list[str],
) -> dict:
    """
    student_skills: [{skill_name, rating (1-5)}]
    course_required_skills: [skill_name, ...]

    score = average(normalized rating for each required skill) * 20

    A skill the student didn't rate is treated as rating=1 (weakest), not
    skipped — silently ignoring missing skills would let omissions inflate
    scores.
    """
    if not course_required_skills:
        return {"score": MAX_SKILLS_FIT_SCORE * 0.5, "skill_breakdown": [], "data_complete": False}

    student_lookup = {s["skill_name"].strip().lower(): s["rating"] for s in student_skills}

    breakdown = []
    normalized_sum = 0.0

    for skill in course_required_skills:
        key = skill.strip().lower()
        rating = student_lookup.get(key, 1)  # default to weakest if unrated
        normalized = rating / MAX_SELF_RATING
        normalized_sum += normalized
        breakdown.append({"skill_name": skill, "rating": rating, "normalized": round(normalized, 3)})

    avg_normalized = normalized_sum / len(course_required_skills)
    score = round(avg_normalized * MAX_SKILLS_FIT_SCORE, 2)

    return {"score": score, "skill_breakdown": breakdown, "data_complete": True}
