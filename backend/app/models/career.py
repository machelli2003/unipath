"""
careers collection

Knowledge base for the "Career Explorer" advanced feature — lets a student
start from a target career and work backwards to matching courses.
"""

from datetime import datetime
from mongoengine import Document, StringField, ListField, DateTimeField


class Career(Document):
    name = StringField(required=True, unique=True)  # references CAREER_GOAL_CHOICES
    description = StringField()

    related_courses = ListField(StringField())  # course names that lead here
    required_skills = ListField(StringField())
    typical_industries = ListField(StringField())
    growth_outlook = StringField(
        choices=["Declining", "Stable", "Growing", "High Growth"]
    )

    created_at = DateTimeField(default=datetime.utcnow)
    updated_at = DateTimeField(default=datetime.utcnow)

    meta = {
        "collection": "careers",
        "indexes": ["name"],
    }


def serialize_career(career) -> dict:
    payload = career.to_mongo().to_dict() if hasattr(career, "to_mongo") else dict(career)
    return {
        "id": str(payload.get("_id") or payload.get("id") or ""),
        "key": payload.get("key", payload.get("name", "")),
        "title": payload.get("title", payload.get("name", "")),
        "industry": payload.get("industry", ""),
        "description": payload.get("description", ""),
        "related_courses": payload.get("related_courses", []),
        "required_skills": payload.get("required_skills", []),
        "interest_tags": payload.get("interest_tags", []),
        "salary_range": payload.get("salary_range", {}),
        "employment_rate": payload.get("employment_rate", 0),
        "professional_body": payload.get("professional_body", ""),
    }
