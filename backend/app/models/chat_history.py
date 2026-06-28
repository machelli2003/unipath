"""
chat_history collection

Stores AI advisor conversation turns (premium feature). The AI layer used
in chat follows the same strict rules as elsewhere: it explains, compares,
and suggests — it never invents cut-offs or overrides the recommendation
engine's output. See app/services/ai_layer/guardrails.py.
"""

from datetime import datetime
from mongoengine import Document, EmbeddedDocument, EmbeddedDocumentListField, StringField, ReferenceField, DateTimeField

from app.models.user import User


class ChatMessage(EmbeddedDocument):
    role = StringField(choices=["user", "assistant"], required=True)
    content = StringField(required=True)
    timestamp = DateTimeField(default=datetime.utcnow)


class ChatHistory(Document):
    user = ReferenceField(User, required=True)
    session_title = StringField(default="New Conversation")
    messages = EmbeddedDocumentListField(ChatMessage)

    created_at = DateTimeField(default=datetime.utcnow)
    updated_at = DateTimeField(default=datetime.utcnow)

    meta = {
        "collection": "chat_history",
        "indexes": ["user", "-updated_at"],
    }
