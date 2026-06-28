from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from bson import ObjectId

from ...db.mongodb import get_db
from ...services.recommendation.engine import RecommendationEngine
from ...services.ai.explanation_generator import ExplanationGenerator

recommend_bp = Blueprint("recommend", __name__)
engine = RecommendationEngine()
ai = ExplanationGenerator()


@recommend_bp.post("")
@jwt_required()
def run_recommendation():
    user_id = get_jwt_identity()
    db = get_db()

    profile = db.student_profiles.find_one({"user_id": user_id})
    if not profile:
        return jsonify({"error": "Profile not found. Complete onboarding first."}), 404

    profile["user_id"] = user_id
    result = engine.run(profile, save=True)
    if "error" in result:
        return jsonify(result), 500

    include_ai = request.args.get("ai", "true").lower() == "true"
    if include_ai and result.get("top_courses"):
        result["ai_summary"] = ai.generate_summary(result)

    return jsonify(result), 200


@recommend_bp.get("/latest")
@jwt_required()
def get_latest():
    user_id = get_jwt_identity()
    db = get_db()

    rec = db.recommendations.find_one(
        {"student_id": user_id},
        sort=[("generated_at", -1)]
    )
    if not rec:
        return jsonify({"error": "No recommendations found. Run /recommend first."}), 404

    rec["_id"] = str(rec["_id"])
    rec["generated_at"] = rec["generated_at"].isoformat()
    return jsonify(rec), 200


@recommend_bp.get("/course/<course_id>")
@jwt_required()
def explain_course(course_id: str):
    user_id = get_jwt_identity()
    db = get_db()

    profile = db.student_profiles.find_one({"user_id": user_id})
    if not profile:
        return jsonify({"error": "Profile not found."}), 404

    rec = db.recommendations.find_one(
        {"student_id": user_id}, sort=[("generated_at", -1)]
    )
    if not rec:
        return jsonify({"error": "No recommendation found. Run /recommend first."}), 404

    course_result = next(
        (c for c in rec.get("top_courses", []) if c["course_id"] == course_id),
        None,
    )
    if not course_result:
        return jsonify({"error": "Course not found in your recommendations."}), 404

    explanation = ai.generate_course_explanation(course_result, profile)
    return jsonify({"course_id": course_id, "explanation": explanation}), 200
