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
