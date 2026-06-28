"""
cut_off_points collection

The single source of truth for admission cut-offs. ALL admission-likelihood
logic in the admission engine reads from here — the AI layer and
recommendation engine are NEVER allowed to invent or estimate a cut-off.

Supports yearly versioning: multiple documents can exist for the same
(university, course) across different years, enabling historical trend
analysis (see admission_engine/trend_analyzer.py).
"""

from datetime import datetime
from mongoengine import Document, StringField, IntField, FloatField, DateTimeField


class CutOffPoint(Document):
    university_name = StringField(required=True)
    course_name = StringField(required=True)
    year = IntField(required=True)

    cut_off_aggregate = IntField(required=True)  # lower = more competitive (WASSCE scale)

    # Optional competition signals used by the competition_factor calculation
    applicants_count = IntField()
    available_slots = IntField()

    source = StringField()  # e.g. "GTEC published list 2025", official source citation
    notes = StringField()

    created_at = DateTimeField(default=datetime.utcnow)

    meta = {
        "collection": "cut_off_points",
        "indexes": [
            {"fields": ["university_name", "course_name", "year"], "unique": True},
            "year",
        ],
        # newest year first by default — convenient for "latest cut-off" queries
        "ordering": ["-year"],
    }
