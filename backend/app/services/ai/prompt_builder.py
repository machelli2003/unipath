"""
Builds prompts for Claude that inject the deterministic results.
Claude is ONLY allowed to explain/narrate — never score or decide.
"""

SYSTEM_PROMPT = """You are UniPath AI, an academic guidance advisor for SHS students in Ghana.

STRICT RULES — you must follow these without exception:
1. You NEVER calculate or change scores — all scores were pre-calculated by the system.
2. You NEVER invent or estimate cut-off points — only use values provided to you.
3. You NEVER override the recommendation ranking — only explain it.
4. You ONLY explain, compare, and guide based on the data given to you.
5. Keep language simple, warm, and encouraging — you are talking to a student.
6. Always be honest about reach choices — do not give false hope.
7. If asked something outside academic guidance, politely redirect.

Your role: explain WHY courses were recommended, compare options, and help the student understand their choices."""


def build_summary_prompt(result: dict) -> tuple[str, str]:
    top = result.get("top_courses", [])[:5]
    aggregate = result.get("student_aggregate", "unknown")
    shs_prog = result.get("shs_program", "unknown")

    courses_text = "\n".join([
        f"- {i+1}. {c['course_name']} at {c['university']} (Match: {round(c['match_score'])}%, Admission: {c['admission_category'].upper()}, Cut-off: {c['cut_off_aggregate']})"
        for i, c in enumerate(top)
    ])

    user_prompt = f"""A student with the following profile just received their recommendations:

SHS Programme: {shs_prog}
WASSCE Aggregate: {aggregate}

Top 5 recommended courses:
{courses_text}

Write a short, encouraging 3-4 sentence summary for this student explaining:
1. What their top match is and why it suits them
2. Which choice looks most achievable given their aggregate
3. One piece of actionable advice

Keep it warm, direct, and specific. Do not use bullet points."""

    return SYSTEM_PROMPT, user_prompt


def build_course_explanation_prompt(course_result: dict, profile: dict) -> tuple[str, str]:
    user_prompt = f"""Explain this course recommendation to the student:

Course: {course_result['course_name']} at {course_result['university']}
Match Score: {round(course_result['match_score'])}%
Admission Category: {course_result['admission_category'].upper()}
Student Aggregate: {course_result['student_aggregate']}
Cut-off Aggregate: {course_result['cut_off_aggregate']}
Career Paths: {', '.join(course_result.get('career_paths', []))}
Why Points: {'; '.join(course_result.get('why_points', []))}

Student Profile:
- SHS Programme: {profile.get('shs_program')}
- Interests: {', '.join(profile.get('interests', []))}
- Career Goals: {', '.join(profile.get('career_goals', []))}

Write 2-3 paragraphs explaining this match clearly to the student.
Be specific about why it suits them and what to expect from the programme."""

    return SYSTEM_PROMPT, user_prompt


def build_chat_system_prompt(context: dict) -> str:
    top = context.get("top_courses", [])[:3]
    courses_text = ", ".join([
        f"{c['course_name']} at {c['university']} ({round(c['match_score'])}%)"
        for c in top
    ])

    return f"""{SYSTEM_PROMPT}

STUDENT CONTEXT (use this to personalise your responses):
- SHS Programme: {context.get('shs_program', 'Unknown')}
- WASSCE Aggregate: {context.get('student_aggregate', 'Unknown')}
- Top Matches: {courses_text}
- Interests: {', '.join(context.get('interests', []))}
- Career Goals: {', '.join(context.get('career_goals', []))}

Use this context to give personalised, relevant advice."""
