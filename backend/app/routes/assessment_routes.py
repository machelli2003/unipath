"""
app/routes/assessment_routes.py

POST /api/assess
Takes raw WASSCE grades (or mock grades / strength ratings depending on
mode), runs them through the deterministic grade converter, and stores an
Assessment record. This is STEP 1 of the recommendation flow — scoring
against courses happens later via /api/recommend.
"""

from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.models.assessment import Assessment
from app.services.recommendation_engine.grade_converter import (
    convert_subjects,
    calculate_aggregate,
)
from app.schemas.assessment_schema import AssessmentSchema
from app.utils.validators import validate_with_schema

assessment_bp = Blueprint("assessment", __name__)


@assessment_bp.post("")
@jwt_required()
def submit_assessment():
    user_id = get_jwt_identity()
    data, errors = validate_with_schema(AssessmentSchema(), request.get_json(silent=True) or {})
    if errors:
        return jsonify({"errors": errors}), 400

    converted = convert_subjects(data["subjects"])
    aggregate = calculate_aggregate(converted)

    assessment = Assessment(
        user=user_id,
        mode=data["mode"],
        converted_subjects=converted,
        aggregate_score=aggregate,
        is_simulation=data.get("is_simulation", False),
    )
    try:
        assessment.save()
        assessment_id = str(assessment.id)
    except Exception as e:
        current_app.config["DB_AVAILABLE"] = False
        current_app.config["DB_ERROR"] = str(e)
        current_app.config.setdefault("fallback_assessments", {})[str(user_id)] = {
            "mode": data["mode"],
            "converted_subjects": converted,
            "aggregate_score": aggregate,
            "is_simulation": data.get("is_simulation", False),
        }
        assessment_id = f"fallback-{user_id}"

    return jsonify(
        {
            "assessment_id": assessment_id,
            "converted_subjects": converted,
            "aggregate_score": aggregate,
        }
    ), 201
