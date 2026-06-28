from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from bson import ObjectId

from ...db.mongodb import get_db
from ...models.course import serialize_course

courses_bp = Blueprint("courses", __name__)


@courses_bp.get("")
@jwt_required()
def get_courses():
    db = get_db()
    query = {}

    uni = request.args.get("university")
    category = request.args.get("category")
    max_co = request.args.get("max_cut_off", type=int)

    if uni:
        query["university_short"] = uni.upper()
    if category:
        query["category"] = category
    if max_co is not None:
        query["cut_off_2025"] = {"$lte": max_co}

    courses = [serialize_course(c) for c in db.courses.find(query)]
    return jsonify({"courses": courses, "total": len(courses)}), 200


@courses_bp.get("/<course_id>")
@jwt_required()
def get_course(course_id: str):
    db = get_db()
    try:
        course = db.courses.find_one({"_id": ObjectId(course_id)})
    except Exception:
        return jsonify({"error": "Invalid course ID."}), 400

    if not course:
        return jsonify({"error": "Course not found."}), 404

    cut_offs = list(
        db.cut_off_points.find({"course_id": course_id}, sort=[("year", -1)])
    )
    history = [{"year": c["year"], "aggregate": c["aggregate"]} for c in cut_offs]

    return jsonify(
        {
            "course": serialize_course(course),
            "cut_off_history": history,
        }
    ), 200
