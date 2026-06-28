"""
app/routes/course_routes.py

GET /api/courses              -> list all courses (paginated)
GET /api/courses/<name>       -> single course detail, with offering
                                  universities and historical cut-offs
"""

from flask import Blueprint, request, jsonify

from app.models.course import Course
from app.models.cut_off_point import CutOffPoint

course_bp = Blueprint("course", __name__)


@course_bp.get("")
def list_courses():
    page = int(request.args.get("page", 1))
    per_page = int(request.args.get("per_page", 20))
    courses = Course.objects().skip((page - 1) * per_page).limit(per_page)
    return jsonify(
        {
            "page": page,
            "per_page": per_page,
            "total": Course.objects().count(),
            "items": [c.to_mongo().to_dict() | {"_id": str(c.id)} for c in courses],
        }
    ), 200


@course_bp.get("/<name>")
def get_course(name):
    course = Course.objects(name=name).first()
    if not course:
        return jsonify({"error": "Course not found."}), 404

    historical_cutoffs = [
        {
            "university_name": c.university_name,
            "year": c.year,
            "cut_off_aggregate": c.cut_off_aggregate,
        }
        for c in CutOffPoint.objects(course_name=name)
    ]

    data = course.to_mongo().to_dict()
    data["_id"] = str(course.id)
    data["historical_cutoffs"] = historical_cutoffs
    return jsonify(data), 200
