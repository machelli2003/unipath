"""
app/routes/simulation_routes.py

POST /api/simulate
The "What-If Simulator" advanced feature (Premium). Accepts a hypothetical
set of grades, runs them through the SAME deterministic engine as a normal
assessment, and returns results WITHOUT persisting them as the student's
real assessment history (is_simulation=True).
"""

from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.models.student_profile import StudentProfile
from app.models.course import Course
from app.services.recommendation_engine.grade_converter import convert_subjects, calculate_aggregate
from app.services.recommendation_engine.engine import generate_recommendations
from app.schemas.assessment_schema import AssessmentSchema
from app.utils.validators import validate_with_schema
from app.middleware.rbac import premium_required

simulation_bp = Blueprint("simulation", __name__)


@simulation_bp.post("")
@premium_required
def simulate():
    user_id = get_jwt_identity()
    data, errors = validate_with_schema(AssessmentSchema(), request.get_json(silent=True) or {})
    if errors:
        return jsonify({"errors": errors}), 400

    profile = StudentProfile.objects(user=user_id).first()
    if not profile:
        return jsonify({"error": "Complete your profile before running simulations."}), 400

    converted = convert_subjects(data["subjects"])
    aggregate = calculate_aggregate(converted)

    all_courses = [c.to_mongo().to_dict() for c in Course.objects()]
    student_subjects = [{"subject_name": s["subject_name"], "numeric_value": s["numeric_value"]} for s in converted]

    results = generate_recommendations(
        all_courses=all_courses,
        student_subjects=student_subjects,
        student_interests=profile.interests,
        student_skills=[{"skill_name": s.skill_name, "rating": s.rating} for s in profile.skills],
        student_career_goals=profile.career_goals,
        top_n=current_app.config.get("FREE_TIER_RECOMMENDATION_LIMIT", 10),
    )

    return jsonify(
        {
            "simulated_aggregate": aggregate,
            "converted_subjects": converted,
            "results": results,
            "note": "This is a hypothetical simulation and was not saved to your assessment history.",
        }
    ), 200
