from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required

from ...db.mongodb import get_db
from ...models.university import serialize_university

universities_bp = Blueprint("universities", __name__)


@universities_bp.get("")
@jwt_required()
def get_universities():
    db = get_db()
    unis = [serialize_university(u) for u in db.universities.find({})]
    return jsonify({"universities": unis, "total": len(unis)}), 200


@universities_bp.get("/<short_name>")
@jwt_required()
def get_university(short_name: str):
    db = get_db()
    uni = db.universities.find_one({"short_name": short_name.upper()})
    if not uni:
        return jsonify({"error": "University not found."}), 404
    from ...models.course import serialize_course
    courses = list(db.courses.find({"university_short": short_name.upper()}))
    return jsonify(
        {
            "university": serialize_university(uni),
            "courses": [serialize_course(c) for c in courses],
            "total_courses": len(courses),
        }
    ), 200
