from typing import List, Dict, Any

from app.models.student_profile import (
    GRADE_CHOICES,
    INTEREST_CHOICES,
    SKILL_CHOICES,
    CAREER_GOAL_CHOICES,
)


def _canonical_map(choices: List[str]) -> Dict[str, str]:
    return {c.strip().lower(): c for c in choices}


GRADE_CANONICAL = {g.lower(): g for g in GRADE_CHOICES}
NUMERIC_TO_GRADE = {str(i + 1): g for i, g in enumerate(GRADE_CHOICES)}

INTEREST_MAP = _canonical_map(INTEREST_CHOICES)
SKILL_MAP = _canonical_map(SKILL_CHOICES)
CAREER_MAP = _canonical_map(CAREER_GOAL_CHOICES)


def normalize_mode(mode: str) -> str:
    if not mode:
        return mode
    m = mode.strip().lower()
    if m in ("official", "official_results"):
        return "official_results"
    if m in ("awaiting", "awaiting_results"):
        return "awaiting_results"
    if m in ("novdec", "nov_dec", "nov/dec"):
        return "nov_dec"
    return mode


def normalize_grade(g: Any) -> str:
    if g is None:
        return g
    if isinstance(g, int):
        return NUMERIC_TO_GRADE.get(str(g), None)
    s = str(g).strip().upper()
    if s.lower() in GRADE_CANONICAL:
        return GRADE_CANONICAL[s.lower()]
    # numeric string e.g. '1'
    if s.isdigit():
        return NUMERIC_TO_GRADE.get(s)
    return None


def normalize_subjects(subjects: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    out = []
    if not subjects:
        return out
    for s in subjects:
        if not isinstance(s, dict):
            continue
        name = s.get("subject_name") or s.get("name")
        if not name:
            continue
        grade = normalize_grade(s.get("grade") or s.get("numeric_value") or s.get("self_rated_strength"))
        entry = {"subject_name": str(name).strip(), "grade": grade}
        # preserve self_rated_strength if present and numeric
        if "self_rated_strength" in s:
            try:
                entry["self_rated_strength"] = int(s["self_rated_strength"])
            except Exception:
                pass
        out.append(entry)
    return out


def normalize_list_choices(values: List[str], mapping: Dict[str, str]) -> List[str]:
    if not values:
        return []
    out = []
    for v in values:
        if not v:
            continue
        key = str(v).strip().lower()
        if key in mapping:
            out.append(mapping[key])
    return out


def normalize_skills(skills: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    out = []
    if not skills:
        return out
    for s in skills:
        if not isinstance(s, dict):
            continue
        name = s.get("skill_name") or s.get("name")
        if not name:
            continue
        key = str(name).strip().lower()
        canon = SKILL_MAP.get(key)
        if not canon:
            continue
        try:
            rating = int(s.get("rating", s.get("value", 0)))
        except Exception:
            rating = 0
        out.append({"skill_name": canon, "rating": rating})
    return out


def normalize_profile_payload(payload: Dict[str, Any]) -> Dict[str, Any]:
    p = dict(payload) if payload else {}

    # Mode
    if "mode" in p:
        p["mode"] = normalize_mode(p.get("mode"))

    # SHS program - title case
    if "shs_program" in p and p.get("shs_program"):
        p["shs_program"] = str(p.get("shs_program")).strip().title()

    # Subjects and original_subjects
    if "subjects" in p:
        p["subjects"] = normalize_subjects(p.get("subjects", []))
    if "original_subjects" in p:
        p["original_subjects"] = normalize_subjects(p.get("original_subjects", []))

    # Interests
    if "interests" in p:
        p["interests"] = normalize_list_choices(p.get("interests", []), INTEREST_MAP)

    # Skills
    if "skills" in p:
        p["skills"] = normalize_skills(p.get("skills", []))

    # Career goals
    if "career_goals" in p:
        p["career_goals"] = normalize_list_choices(p.get("career_goals", []), CAREER_MAP)

    return p
