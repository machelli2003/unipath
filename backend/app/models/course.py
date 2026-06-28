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
    name = StringField(required=True, unique=True)
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
