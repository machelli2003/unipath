"""
course_requirements collection

Normalized table linking (university, course) -> specific admission
requirement details for that pairing. Separate from `courses.required_subjects`
(which is the GENERAL subject requirement for the course everywhere) because
the same course can have slightly different requirements at different
universities (e.g. KNUST Computer Science vs UG Computer Science).
"""

from datetime import datetime
from mongoengine import (
    Document,
    EmbeddedDocument,
    EmbeddedDocumentListField,
    StringField,
    DateTimeField,
)
from app.models.course import RequiredSubject


class CourseRequirement(Document):
    university_name = StringField(required=True)
    course_name = StringField(required=True)

    specific_subjects = EmbeddedDocumentListField(RequiredSubject)
    additional_notes = StringField()  # e.g. "Interview required", "SHS Science track only"

    created_at = DateTimeField(default=datetime.utcnow)
    updated_at = DateTimeField(default=datetime.utcnow)

    meta = {
        "collection": "course_requirements",
        "indexes": [
            {"fields": ["university_name", "course_name"], "unique": True},
        ],
    }
