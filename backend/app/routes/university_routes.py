"""
app/routes/university_routes.py

GET /api/universities            -> list all universities (paginated)
GET /api/universities/<name>     -> single university detail with faculties/programs
"""

from flask import Blueprint, request, jsonify

from app.models.university import University

university_bp = Blueprint("university", __name__)


@university_bp.get("")
def list_universities():
    page = int(request.args.get("page", 1))
    per_page = int(request.args.get("per_page", 20))
    universities = University.objects().skip((page - 1) * per_page).limit(per_page)
    return jsonify(
        {
            "page": page,
            "per_page": per_page,
            "total": University.objects().count(),
            "items": [u.to_mongo().to_dict() | {"_id": str(u.id)} for u in universities],
        }
    ), 200


@university_bp.get("/<name>")
def get_university(name):
    university = University.objects(name=name).first()
    if not university:
        return jsonify({"error": "University not found."}), 404
    data = university.to_mongo().to_dict()
    data["_id"] = str(university.id)
    return jsonify(data), 200
