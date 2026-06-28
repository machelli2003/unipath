"""
saved_items collection

Generic bookmark/favorites record so students can save courses,
universities, or careers for later (used in dashboard "Saved" tab).
"""

from datetime import datetime
from mongoengine import Document, StringField, ReferenceField, DateTimeField

from app.models.user import User


class SavedItem(Document):
    user = ReferenceField(User, required=True)
    item_type = StringField(choices=["course", "university", "career"], required=True)
    item_name = StringField(required=True)  # name of the saved entity

    created_at = DateTimeField(default=datetime.utcnow)

    meta = {
        "collection": "saved_items",
        "indexes": [
            {"fields": ["user", "item_type", "item_name"], "unique": True},
        ],
    }
