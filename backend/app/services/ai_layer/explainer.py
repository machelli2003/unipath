"""
ai_layer/explainer.py

Takes the deterministic engine's explanation_points and rephrases them into
warmer, more conversational prose for the student. The AI NEVER sees raw DB
write access and is only given the specific facts relevant to this call.
"""

import json

from app.services.ai_layer.guardrails import build_system_prompt
from app.services.ai_layer.client import call_ai


def explain_recommendation(course_name: str, match_score: float, score_breakdown: dict, explanation_points: list[str]) -> str:
    context_data = json.dumps(
        {
            "course_name": course_name,
            "match_score": match_score,
            "score_breakdown": score_breakdown,
            "explanation_points": explanation_points,
        },
        indent=2,
    )

    system_prompt = build_system_prompt(context_data)
    user_message = (
        f"Explain why {course_name} is a {match_score}% match for this student, "
        "in 2-4 friendly sentences, using only the facts provided above."
    )

    return call_ai(system_prompt, user_message)


def compare_courses(courses_data: list[dict]) -> str:
    """
    courses_data: list of dicts, each with course_name, match_score,
    score_breakdown, explanation_points — i.e. only data the engine already
    produced. The AI compares using these facts only.
    """
    context_data = json.dumps(courses_data, indent=2)
    system_prompt = build_system_prompt(context_data)
    course_names = ", ".join(c["course_name"] for c in courses_data)
    user_message = (
        f"Compare these courses for the student: {course_names}. "
        "Highlight key differences using only the facts provided above."
    )
    return call_ai(system_prompt, user_message)


def explain_career_path(career_data: dict) -> str:
    context_data = json.dumps(career_data, indent=2)
    system_prompt = build_system_prompt(context_data)
    user_message = (
        f"Explain the career path for {career_data.get('name')} using only the "
        "facts provided above, in a way that's encouraging and clear for an "
        "SHS student."
    )
    return call_ai(system_prompt, user_message)


def suggest_alternatives(low_match_course: dict, alternative_candidates: list[dict]) -> str:
    """
    alternative_candidates MUST be a pre-filtered list the recommendation
    engine already scored — the AI selects/explains from this list, it
    never invents new course names.
    """
    context_data = json.dumps(
        {"original_course": low_match_course, "alternatives": alternative_candidates},
        indent=2,
    )
    system_prompt = build_system_prompt(context_data)
    user_message = (
        "The student's match for the original course is lower than ideal. "
        "Using ONLY the alternatives list provided above, suggest 1-3 better-fitting "
        "options and briefly explain why."
    )
    return call_ai(system_prompt, user_message)
