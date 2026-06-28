"""
reports collection

Tracks PDF reports generated for a student (premium feature). Stores
metadata + a reference/URL to the generated file rather than the binary
itself (binary lives in object storage / local file system, not MongoDB).
"""

from datetime import datetime
from mongoengine import Document, StringField, ReferenceField, DateTimeField

from app.models.user import User
from app.models.recommendation import Recommendation


class Report(Document):
    user = ReferenceField(User, required=True)
    recommendation = ReferenceField(Recommendation, required=True)

    report_type = StringField(
        choices=["recommendation_summary", "career_roadmap", "full_report"],
        default="recommendation_summary",
    )
    file_path = StringField()  # path/URL to the generated PDF

    created_at = DateTimeField(default=datetime.utcnow)

    meta = {
        "collection": "reports",
        "indexes": ["user", "-created_at"],
    }
