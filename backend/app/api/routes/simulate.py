from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from bson import ObjectId

from ...db.mongodb import get_db
from ...services.recommendation.engine import RecommendationEngine

simulate_bp = Blueprint("simulate", __name__)
engine = RecommendationEngine()


@simulate_bp.post("")
@jwt_required()
def simulate():
    user_id = get_jwt_identity()
    db = get_db()

    profile = db.student_profiles.find_one({"user_id": user_id})
    if not profile:
        return jsonify({"error": "Profile not found."}), 404

    data = request.get_json() or {}
    grade_overrides = data.get("grade_overrides", {})
    if not grade_overrides:
        return jsonify({"error": "Provide grade_overrides in request body."}), 400

    simulated_profile = dict(profile)
    simulated_subjects = {**profile.get("wassce_subjects", {}), **grade_overrides}
    simulated_profile["wassce_subjects"] = simulated_subjects
    simulated_profile["user_id"] = user_id

    result = engine.run(simulated_profile, save=False)
    result["simulated"] = True
    result["grade_overrides"] = grade_overrides

    return jsonify(result), 200
