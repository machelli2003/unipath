from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required

from ...db.mongodb import get_db
from ...models.career import serialize_career
from ...models.course import serialize_course

careers_bp = Blueprint("careers", __name__)


@careers_bp.get("")
@jwt_required()
def get_careers():
    db = get_db()
    careers = [serialize_career(c) for c in db.careers.find({})]
    return jsonify({"careers": careers, "total": len(careers)}), 200


@careers_bp.get("/<career_key>")
@jwt_required()
def get_career(career_key: str):
    db = get_db()
    career = db.careers.find_one({"key": career_key})
    if not career:
        return jsonify({"error": "Career not found."}), 404

    courses = list(db.courses.find({"career_paths": career_key}))
    return jsonify(
        {
            "career": serialize_career(career),
            "matching_courses": [serialize_course(c) for c in courses[:20]],
        }
    ), 200
