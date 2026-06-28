"""
universities collection

Knowledge base entry for a single university. Programs reference course
names rather than embedding full course data — the canonical course record
lives in the courses collection.
"""

from datetime import datetime
from mongoengine import (
    Document,
    EmbeddedDocument,
    EmbeddedDocumentListField,
    StringField,
    ListField,
    DateTimeField,
)


class Department(EmbeddedDocument):
    name = StringField(required=True)
    programs = ListField(StringField())  # course names offered by this dept


class Faculty(EmbeddedDocument):
    name = StringField(required=True)
    departments = EmbeddedDocumentListField(Department)


class University(Document):
    name = StringField(required=True, unique=True)
    short_name = StringField()  # e.g. "KNUST", "UG", "UCC"
    location = StringField()
    overview = StringField()  # general description / history blurb

    faculties = EmbeddedDocumentListField(Faculty)

    # General admission requirements text (specific cut-offs live in
    # cut_off_points collection, NOT here — keeps numbers single-sourced)
    general_admission_requirements = StringField()

    website_url = StringField()
    logo_url = StringField()

    created_at = DateTimeField(default=datetime.utcnow)
    updated_at = DateTimeField(default=datetime.utcnow)

    meta = {
        "collection": "universities",
        "indexes": ["name", "short_name"],
    }


def serialize_university(university) -> dict:
    payload = university.to_mongo().to_dict() if hasattr(university, "to_mongo") else dict(university)
    return {
        "id": str(payload.get("_id") or payload.get("id") or ""),
        "short_name": payload.get("short_name", ""),
        "name": payload.get("name", ""),
        "location": payload.get("location", ""),
        "type": payload.get("type", ""),
        "established": payload.get("established"),
        "website": payload.get("website") or payload.get("website_url", ""),
        "overview": payload.get("overview", ""),
        "faculties": payload.get("faculties", []),
    }
