"""
app/routes/chat_routes.py

POST /api/chat                  -> send a message to the AI advisor (premium)
GET  /api/chat/history           -> list past chat sessions

The AI advisor here is bound by the same guardrails as the rest of the AI
layer (see ai_layer/guardrails.py): it explains, compares, and suggests
ONLY from facts it's given — it never decides admission or invents data.
For general open-ended questions we still inject relevant DB facts
(student's latest recommendation, if any) as context before calling the AI.
"""

from datetime import datetime
from flask import Blueprint, request, jsonify
from flask_jwt_extended import get_jwt_identity

from app.models.chat_history import ChatHistory
from app.models.recommendation import Recommendation
from app.services.ai_layer.guardrails import build_system_prompt
from app.services.ai_layer.client import call_ai
from app.middleware.rbac import premium_required

chat_bp = Blueprint("chat", __name__)


@chat_bp.post("")
@premium_required
def send_chat_message():
    user_id = get_jwt_identity()
    payload = request.get_json(silent=True) or {}
    message = payload.get("message", "").strip()
    session_id = payload.get("session_id")

    if not message:
        return jsonify({"error": "message is required."}), 400

    if session_id:
        session = ChatHistory.objects(id=session_id, user=user_id).first()
        if not session:
            return jsonify({"error": "Chat session not found."}), 404
    else:
        session = ChatHistory(user=user_id, session_title=message[:50])

    # Inject the student's latest recommendation as grounding context so
    # the AI references real, DB-sourced facts rather than guessing.
    latest_recommendation = (
        Recommendation.objects(user=user_id).order_by("-created_at").first()
    )
    context_data = (
        latest_recommendation.to_mongo().to_dict() if latest_recommendation else "No recommendation data available yet for this student."
    )

    system_prompt = build_system_prompt(str(context_data))
    ai_response = call_ai(system_prompt, message)

    session.messages.append({"role": "user", "content": message, "timestamp": datetime.utcnow()})
    session.messages.append({"role": "assistant", "content": ai_response, "timestamp": datetime.utcnow()})
    session.updated_at = datetime.utcnow()
    session.save()

    return jsonify({"session_id": str(session.id), "response": ai_response}), 200


@chat_bp.get("/history")
@premium_required
def get_chat_history():
    user_id = get_jwt_identity()
    sessions = ChatHistory.objects(user=user_id).order_by("-updated_at")
    return jsonify(
        [
            {
                "id": str(s.id),
                "session_title": s.session_title,
                "updated_at": s.updated_at.isoformat(),
                "message_count": len(s.messages),
            }
            for s in sessions
        ]
    ), 200
