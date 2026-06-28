"""
app/routes/profile_routes.py

GET  /api/profile        -> fetch the logged-in student's profile
PUT  /api/profile        -> create/update the logged-in student's profile
"""

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.models.student_profile import StudentProfile

profile_bp = Blueprint("profile", __name__)


@profile_bp.get("")
@jwt_required()
def get_profile():
    user_id = get_jwt_identity()
    profile = StudentProfile.objects(user=user_id).first()
    if not profile:
        return jsonify({"error": "Profile not found. Complete onboarding first."}), 404
    return jsonify(profile.to_mongo().to_dict() | {"_id": str(profile.id)}), 200


@profile_bp.put("")
@jwt_required()
def upsert_profile():
    user_id = get_jwt_identity()
    payload = request.get_json(silent=True) or {}

    profile = StudentProfile.objects(user=user_id).first()
    if not profile:
        payload["user"] = user_id
        profile = StudentProfile(**payload)
    else:
        for key, value in payload.items():
            setattr(profile, key, value)

    profile.save()
    return jsonify({"message": "Profile saved.", "profile_id": str(profile.id)}), 200
