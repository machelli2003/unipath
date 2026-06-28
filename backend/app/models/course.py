"""
courses collection

Canonical knowledge base entry for a course (e.g. "Computer Science").
This is the single source of truth the recommendation engine scores against
— required_subjects and required_skills drive Academic Fit / Skills Fit.
"""

from datetime import datetime
from mongoengine import (
    Document,
    EmbeddedDocument,
    EmbeddedDocumentField,
    EmbeddedDocumentListField,
    StringField,
    ListField,
    IntField,
    DateTimeField,
)


class RequiredSubject(EmbeddedDocument):
    subject_name = StringField(required=True)
    # Best grade considered "fully met" for this subject (e.g. "B3")
    minimum_grade = StringField(required=True)
    # core subjects (Math/English/core science) get higher weight in scoring
    is_core = StringField(choices=["yes", "no"], default="no")


class Course(Document):
    name = StringField(required=True)
    description = StringField()

    required_subjects = EmbeddedDocumentListField(RequiredSubject)
    required_skills = ListField(StringField())  # references SKILL_CHOICES
    related_interests = ListField(StringField())  # references INTEREST_CHOICES
    related_career_goals = ListField(StringField())  # references CAREER_GOAL_CHOICES

    career_paths = ListField(StringField())
    difficulty_level = StringField(
        choices=["Low", "Moderate", "High", "Very High"], default="Moderate"
    )

    # Names of universities offering this course — full details/cut-offs are
    # resolved via the universities and cut_off_points collections.
    offered_at_universities = ListField(StringField())

    created_at = DateTimeField(default=datetime.utcnow)
    updated_at = DateTimeField(default=datetime.utcnow)

    meta = {
        "collection": "courses",
        "indexes": ["name"],
    }


def serialize_course(course) -> dict:
    payload = course.to_mongo().to_dict() if hasattr(course, "to_mongo") else dict(course)
    return {
        "id": str(payload.get("_id") or payload.get("id") or ""),
        "name": payload.get("name", ""),
        "university_short": payload.get("university_short", ""),
        "university_id": payload.get("university_id", ""),
        "category": payload.get("category", ""),
        "faculty": payload.get("faculty", ""),
        "duration_years": payload.get("duration_years", 0),
        "cut_off_2025": payload.get("cut_off_2025", 0),
        "competitiveness": payload.get("competitiveness", ""),
        "difficulty": payload.get("difficulty", payload.get("difficulty_level", "")),
        "required_subjects": payload.get("required_subjects", []),
        "core_subjects": payload.get("core_subjects", []),
        "elective_subjects": payload.get("elective_subjects", []),
        "eligible_shs_programmes": payload.get("eligible_shs_programmes", []),
        "interest_tags": payload.get("interest_tags", payload.get("related_interests", [])),
        "required_skills": payload.get("required_skills", []),
        "career_paths": payload.get("career_paths", payload.get("related_career_goals", [])),
        "description": payload.get("description", ""),
        "national_service": payload.get("national_service", True),
        "internship_required": payload.get("internship_required", False),
        "professional_body": payload.get("professional_body", ""),
        "average_cut_off": payload.get("average_cut_off", payload.get("cut_off_2025", 0)),
    }
