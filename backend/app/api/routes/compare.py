from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from bson import ObjectId

from ...db.mongodb import get_db
from ...models.course import serialize_course
from ...models.university import serialize_university

compare_bp = Blueprint("compare", __name__)


@compare_bp.post("/courses")
@jwt_required()
def compare_courses():
    data = request.get_json() or {}
    course_ids = data.get("course_ids", [])

    if len(course_ids) < 2:
        return jsonify({"error": "Provide at least 2 course_ids."}), 400
    if len(course_ids) > 4:
        return jsonify({"error": "Maximum 4 courses can be compared at once."}), 400

    db = get_db()
    user_id = get_jwt_identity()
    profile = db.student_profiles.find_one({"user_id": user_id})
    aggregate = None
    if profile:
        from ...services.recommendation.grade_converter import GradeConverter
        aggregate = GradeConverter.compute_aggregate(profile.get("wassce_subjects", {}))

    courses = []
    for cid in course_ids:
        try:
            course = db.courses.find_one({"_id": ObjectId(cid)})
            if course:
                serialised = serialize_course(course)
                if aggregate is not None:
                    from ...services.admission.cut_off_analyzer import CutOffAnalyzer
                    analyzer = CutOffAnalyzer()
                    serialised["admission"] = analyzer.analyze(course, aggregate)
                courses.append(serialised)
        except Exception:
            pass

    return jsonify({"courses": courses, "student_aggregate": aggregate}), 200


@compare_bp.post("/universities")
@jwt_required()
def compare_universities():
    data = request.get_json() or {}
    short_names = data.get("short_names", [])

    if len(short_names) < 2:
        return jsonify({"error": "Provide at least 2 university short names."}), 400

    db = get_db()
    unis = []
    for name in short_names:
        uni = db.universities.find_one({"short_name": name.upper()})
        if uni:
            unis.append(serialize_university(uni))

    return jsonify({"universities": unis}), 200
