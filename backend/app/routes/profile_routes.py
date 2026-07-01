"""
app/routes/profile_routes.py

GET  /api/profile        -> fetch the logged-in student's profile
PUT  /api/profile        -> create/update the logged-in student's profile
"""

from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.models.student_profile import StudentProfile
from mongoengine.errors import ValidationError as MongoValidationError
from app.utils.normalizers import normalize_profile_payload
from mongoengine.errors import ValidationError as MongoValidationError

profile_bp = Blueprint("profile", __name__)


@profile_bp.get("")
@jwt_required()
def get_profile():
    user_id = get_jwt_identity()
    profile = StudentProfile.objects(user=user_id).first()
    if profile:
        return jsonify(profile.to_mongo().to_dict() | {"_id": str(profile.id)}), 200

    fallback_profiles = current_app.config.setdefault("fallback_profiles", {})
    if user_id in fallback_profiles:
        return jsonify({**fallback_profiles[user_id], "_id": user_id}), 200

    return jsonify({"error": "Profile not found. Complete onboarding first."}), 404


@profile_bp.put("")
@jwt_required()
def upsert_profile():
    user_id = get_jwt_identity()
    payload = request.get_json(silent=True) or {}
    # Normalize common frontend variants into canonical model choices
    payload = normalize_profile_payload(payload)

    profile = StudentProfile.objects(user=user_id).first()
    if not profile:
        payload["user"] = user_id
        profile = StudentProfile(**payload)
    else:
        for key, value in payload.items():
            setattr(profile, key, value)

    try:
        profile.save()
    except MongoValidationError as e:
        return jsonify({"error": "Validation error saving profile.", "details": str(e)}), 400
    except Exception as e:
        current_app.config["DB_AVAILABLE"] = False
        current_app.config["DB_ERROR"] = str(e)
        current_app.config.setdefault("fallback_profiles", {})[user_id] = payload
        return jsonify({"message": "Profile saved locally.", "profile_id": user_id, "storage": "fallback"}), 200

    return jsonify({"message": "Profile saved.", "profile_id": str(profile.id)}), 200
