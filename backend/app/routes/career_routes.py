"""
app/routes/career_routes.py

GET /api/careers                 -> list all careers
GET /api/careers/<name>          -> single career detail with related_courses
                                     (the "Career Explorer" feature: start
                                     from a career, work backwards to courses)
"""

from flask import Blueprint, jsonify

from app.models.career import Career
from app.models.course import Course

career_bp = Blueprint("career", __name__)


@career_bp.get("")
def list_careers():
    careers = Career.objects()
    return jsonify([c.to_mongo().to_dict() | {"_id": str(c.id)} for c in careers]), 200


@career_bp.get("/<name>")
def get_career(name):
    career = Career.objects(name=name).first()
    if not career:
        return jsonify({"error": "Career not found."}), 404

    related_courses = [
        c.to_mongo().to_dict() | {"_id": str(c.id)}
        for c in Course.objects(name__in=career.related_courses)
    ]

    data = career.to_mongo().to_dict()
    data["_id"] = str(career.id)
    data["related_courses_detail"] = related_courses
    return jsonify(data), 200
