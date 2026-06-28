"""
users collection

Core account record. Authentication credentials and subscription tier live
here; academic/profile data lives in StudentProfile (one-to-one).
"""

from datetime import datetime
from mongoengine import (
    Document,
    StringField,
    EmailField,
    BooleanField,
    DateTimeField,
)


class User(Document):
    full_name = StringField(required=True, max_length=120)
    email = EmailField(required=True, unique=True)
    password_hash = StringField(required=True)

    role = StringField(choices=["student", "admin"], default="student")
    subscription_tier = StringField(choices=["free", "premium"], default="free")

    is_email_verified = BooleanField(default=False)
    is_active = BooleanField(default=True)

    created_at = DateTimeField(default=datetime.utcnow)
    updated_at = DateTimeField(default=datetime.utcnow)
    last_login_at = DateTimeField()

    meta = {
        "collection": "users",
        "indexes": ["email"],
    }

    def to_public_dict(self) -> dict:
        """Safe representation for API responses (never expose password_hash)."""
        return {
            "id": str(self.id),
            "full_name": self.full_name,
            "email": self.email,
            "role": self.role,
            "subscription_tier": self.subscription_tier,
            "is_email_verified": self.is_email_verified,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }
