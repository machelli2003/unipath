from flask import Blueprint, request, jsonify, Response, stream_with_context
from flask_jwt_extended import jwt_required, get_jwt_identity

from ...db.mongodb import get_db
from ...services.ai.chat_handler import ChatHandler

chat_bp = Blueprint("chat", __name__)
chat_handler = ChatHandler()


def _get_context(user_id: str, db) -> dict:
    profile = db.student_profiles.find_one({"user_id": user_id}) or {}
    rec = db.recommendations.find_one({"student_id": user_id}, sort=[("generated_at", -1)]) or {}
    return {
        "shs_program": profile.get("shs_program", ""),
        "interests": profile.get("interests", []),
        "career_goals": profile.get("career_goals", []),
        "student_aggregate": rec.get("student_aggregate"),
        "top_courses": rec.get("top_courses", [])[:5],
    }


@chat_bp.post("")
@jwt_required()
def chat():
    user_id = get_jwt_identity()
    data = request.get_json() or {}
    message = data.get("message", "").strip()

    if not message:
        return jsonify({"error": "Message cannot be empty."}), 400

    db = get_db()
    context = _get_context(user_id, db)
    response = chat_handler.chat(user_id, message, context)
    return jsonify({"response": response}), 200


@chat_bp.post("/stream")
@jwt_required()
def chat_stream():
    user_id = get_jwt_identity()
    data = request.get_json() or {}
    message = data.get("message", "").strip()

    if not message:
        return jsonify({"error": "Message cannot be empty."}), 400

    db = get_db()
    context = _get_context(user_id, db)

    def generate():
        for chunk in chat_handler.stream_chat(user_id, message, context):
            yield f"data: {chunk}\n\n"
        yield "data: [DONE]\n\n"

    return Response(
        stream_with_context(generate()),
        mimetype="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "X-Accel-Buffering": "no",
            "Access-Control-Allow-Origin": "*",
        },
    )


@chat_bp.get("/history")
@jwt_required()
def get_history():
    user_id = get_jwt_identity()
    db = get_db()
    records = list(db.chat_history.find({"user_id": user_id}, sort=[("created_at", -1)]).limit(50))
    history = [
        {
            "user_message": r["user_message"],
            "ai_response": r["ai_response"],
            "created_at": r["created_at"].isoformat(),
        }
        for r in records
    ]
    history.reverse()
    return jsonify({"history": history}), 200


@chat_bp.delete("/history")
@jwt_required()
def clear_history():
    user_id = get_jwt_identity()
    db = get_db()
    db.chat_history.delete_many({"user_id": user_id})
    return jsonify({"message": "Chat history cleared."}), 200
