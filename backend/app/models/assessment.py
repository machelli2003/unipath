"""
assessments collection

A snapshot of a student's academic input at a point in time, AFTER grade
conversion (see recommendation_engine/grade_converter.py) but BEFORE
scoring. Kept separate from StudentProfile so a student can re-run
assessments (e.g. "What-If Simulator") without overwriting their base
profile, and so we retain a history of past assessments.
"""

from datetime import datetime
from mongoengine import (
    Document,
    EmbeddedDocument,
    EmbeddedDocumentListField,
    StringField,
    FloatField,
    ReferenceField,
    DateTimeField,
    BooleanField,
)

from app.models.user import User


class ConvertedSubject(EmbeddedDocument):
    subject_name = StringField(required=True)
    original_grade = StringField(required=True)  # e.g. "B2"
    numeric_value = FloatField(required=True)  # e.g. 2 (A1=1 ... F9=9)


class Assessment(Document):
    user = ReferenceField(User, required=True)

    mode = StringField(
        choices=["official_results", "awaiting_results", "nov_dec"], required=True
    )
    converted_subjects = EmbeddedDocumentListField(ConvertedSubject)
    aggregate_score = FloatField()  # sum/avg of best 6 subjects, per WASSCE convention

    # Flags whether this assessment came from the "What-If Simulator"
    # (hypothetical, not saved as the student's official profile state)
    is_simulation = BooleanField(default=False)

    created_at = DateTimeField(default=datetime.utcnow)

    meta = {
        "collection": "assessments",
        "indexes": ["user", "-created_at"],
    }
