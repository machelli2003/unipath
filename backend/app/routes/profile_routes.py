"""
app/routes/profile_routes.py

GET  /api/profile        -> fetch the logged-in student's profile
PUT  /api/profile        -> create/update the logged-in student's profile
"""

from flask import Blueprint, request, jsonify
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
    if not profile:
        return jsonify({"error": "Profile not found. Complete onboarding first."}), 404
    return jsonify(profile.to_mongo().to_dict() | {"_id": str(profile.id)}), 200


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
        # Return validation details to the client so frontend can show actionable errors
        return jsonify({"error": "Validation error saving profile.", "details": str(e)}), 400
    except Exception as e:
        # Unexpected server error
        return jsonify({"error": "Internal server error.", "details": str(e)}), 500

    return jsonify({"message": "Profile saved.", "profile_id": str(profile.id)}), 200
