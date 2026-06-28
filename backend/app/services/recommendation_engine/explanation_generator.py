"""
recommendation_engine/explanation_generator.py

Generates plain-language explanation bullet points FROM THE SCORING DATA
ITSELF using simple rules/templates. This runs BEFORE the AI layer.

Why this matters for the "no AI hallucination" guarantee: the facts in
explanation_points are derived directly from numbers the engine already
computed. The AI layer (see ai_layer/explainer.py) is only ever allowed to
rephrase/expand THESE pre-computed facts into friendlier prose — it never
generates new factual claims from scratch.
"""


def generate_explanation_points(
    course_name: str,
    academic_result: dict,
    interest_result: dict,
    skills_result: dict,
    career_result: dict,
) -> list[str]:
    points = []

    # ----- Academic strengths -----
    for subj in academic_result.get("subject_breakdown", []):
        if subj["met"] and subj["raw_score"] >= 0.85:
            core_tag = " (core subject)" if subj["is_core"] else ""
            points.append(f"Strong performance in {subj['subject_name']}{core_tag}")

    weak_core_subjects = [
        s["subject_name"]
        for s in academic_result.get("subject_breakdown", [])
        if s["is_core"] and not s["met"]
    ]
    if weak_core_subjects:
        points.append(
            f"Grade below requirement in core subject(s): {', '.join(weak_core_subjects)}"
        )

    # ----- Interests -----
    if interest_result.get("matched_interests"):
        points.append(
            f"Interest in {', '.join(interest_result['matched_interests'])} aligns with this course"
        )

    # ----- Skills -----
    strong_skills = [
        s["skill_name"]
        for s in skills_result.get("skill_breakdown", [])
        if s["rating"] >= 4
    ]
    if strong_skills:
        points.append(f"High self-rated {', '.join(strong_skills)}")

    # ----- Career -----
    if career_result.get("matched_goals"):
        points.append(
            f"Matches stated career goal: {', '.join(career_result['matched_goals'])}"
        )

    if not points:
        points.append(
            "Limited overlap found between your profile and this course's typical requirements"
        )

    return points
