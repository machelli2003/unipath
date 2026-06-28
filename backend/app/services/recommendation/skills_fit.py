"""
Skills fit helper for the recommendation engine.
"""
MAX_SKILLS_FIT_SCORE = 20.0
MAX_SELF_RATING = 5.0


def calculate_skills_fit(student_skills: list[dict], course_required_skills: list[str]) -> dict:
    if not course_required_skills:
        return {"score": MAX_SKILLS_FIT_SCORE * 0.5, "skill_breakdown": [], "data_complete": False}

    student_lookup = {s["skill_name"].strip().lower(): s["rating"] for s in student_skills}
    breakdown = []
    normalized_sum = 0.0

    for skill in course_required_skills:
        key = skill.strip().lower()
        rating = student_lookup.get(key, 1)
        normalized = rating / MAX_SELF_RATING
        normalized_sum += normalized
        breakdown.append({"skill_name": skill, "rating": rating, "normalized": round(normalized, 3)})

    avg_normalized = normalized_sum / len(course_required_skills)
    return {"score": round(avg_normalized * MAX_SKILLS_FIT_SCORE, 2), "skill_breakdown": breakdown, "data_complete": True}
