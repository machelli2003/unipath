"""
Handles the AI advisor chat session.
Maintains conversation history and streams responses.
"""
from datetime import datetime
from mongoengine import ConnectionFailure
from bson import ObjectId
from ...db.mongodb import get_db
from .claude_client import ClaudeClient
from .prompt_builder import build_chat_system_prompt


class ChatHandler:

    def __init__(self):
        self.client = ClaudeClient()

    def get_history(self, user_id: str, limit: int = 20) -> list:
        try:
            db = get_db()
        except ConnectionFailure:
            return []

        records = list(
            db.chat_history.find(
                {"user_id": user_id},
                sort=[("created_at", -1)],
            ).limit(limit)
        )
        records.reverse()
        messages = []
        for r in records:
            messages.append({"role": "user", "content": r["user_message"]})
            messages.append({"role": "assistant", "content": r["ai_response"]})
        return messages

    def save_turn(self, user_id: str, user_msg: str, ai_response: str):
        try:
            db = get_db()
        except ConnectionFailure:
            return

        db.chat_history.insert_one({
            "_id": ObjectId(),
            "user_id": user_id,
            "user_message": user_msg,
            "ai_response": ai_response,
            "created_at": datetime.utcnow(),
        })

    def chat(self, user_id: str, user_message: str, context: dict) -> str:
        system = build_chat_system_prompt(context)
        history = self.get_history(user_id)
        try:
            response = self.client.complete(system, user_message, max_tokens=600)
        except Exception as e:
            response = "I'm sorry, I'm having trouble responding right now. Please try again."
            print(f"[Chat] Error: {e}")

        self.save_turn(user_id, user_message, response)
        return response

    def stream_chat(self, user_id: str, user_message: str, context: dict):
        system = build_chat_system_prompt(context)
        history = self.get_history(user_id)
        full_response = ""
        try:
            for chunk in self.client.stream(system, history + [{"role": "user", "content": user_message}], max_tokens=600):
                full_response += chunk
                yield chunk
        except Exception as e:
            yield "I'm having trouble responding right now."
            print(f"[Chat Stream] Error: {e}")
            return

        self.save_turn(user_id, user_message, full_response)
