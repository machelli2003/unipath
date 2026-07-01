"""
app/routes/recommendation_routes.py

POST /api/recommend
The main pipeline endpoint: pulls the student's profile + a given
assessment, runs the deterministic recommendation engine against all
courses in the DB, attaches admission categories via the admission engine,
optionally enriches with AI-generated prose explanations, and persists the
result as a Recommendation document.

Free tier students get up to FREE_TIER_RECOMMENDATION_LIMIT results;
premium unlocks AI chat-style elaboration (handled by /api/chat instead).
"""

from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.models.assessment import Assessment
from app.models.student_profile import StudentProfile
from app.models.recommendation import Recommendation
from app.services.recommendation_engine.engine import generate_recommendations
from app.services.admission_engine.cut_off_analyzer import CutOffAnalyzer
from app.db.mongodb import get_db


def _get_profile_payload(user_id: str) -> dict | None:
    profile = StudentProfile.objects(user=user_id).first()
    if profile:
        data = profile.to_mongo().to_dict()
        if isinstance(data.get("skills"), list):
            data["skills"] = [
                {"skill_name": item.get("skill_name"), "rating": item.get("rating")}
                for item in data.get("skills", [])
                if isinstance(item, dict)
            ]
        return data

    fallback_profiles = current_app.config.setdefault("fallback_profiles", {})
    if user_id in fallback_profiles:
        return dict(fallback_profiles[user_id])

    return None


def _normalize_course_payload(course: dict) -> dict:
    if not isinstance(course, dict):
        return {}

    normalized = dict(course)

    def _as_list(value):
        if isinstance(value, list):
            return value
        if isinstance(value, tuple):
            return list(value)
        if value is None:
            return []
        return [value]

    required_subjects = normalized.get("required_subjects", [])
    if isinstance(required_subjects, list):
        normalized["required_subjects"] = [
            item if isinstance(item, dict) else {"subject_name": str(item), "minimum_grade": "C6", "is_core": "no"}
            for item in required_subjects
        ]
    else:
        normalized["required_subjects"] = [
            {"subject_name": str(required_subjects), "minimum_grade": "C6", "is_core": "no"}
        ]

    normalized["required_skills"] = _as_list(normalized.get("required_skills", []))
    normalized["related_interests"] = _as_list(normalized.get("related_interests", []))
    normalized["related_career_goals"] = _as_list(normalized.get("related_career_goals", []))
    normalized["career_paths"] = _as_list(normalized.get("career_paths", []))

    return normalized

recommendation_bp = Blueprint("recommendation", __name__)


def _serialize_results(results: list[dict]) -> list[dict]:
    return [
        {
            "course_name": item.get("course_name"),
            "match_score": item.get("match_score"),
            "score_breakdown": item.get("score_breakdown", {}),
            "explanation_points": item.get("explanation_points", []),
            "admission_category": item.get("admission_category") or (item.get("admission") or {}).get("category"),
            "why_points": item.get("explanation_points", []),
        }
        for item in results
    ]


@recommendation_bp.post("")
@jwt_required()
def get_recommendations():
    user_id = get_jwt_identity()
    payload = request.get_json(silent=True) or {}
    assessment_id = payload.get("assessment_id")

    if not assessment_id:
        return jsonify({"error": "assessment_id is required."}), 400

    assessment = Assessment.objects(id=assessment_id, user=user_id).first()
    if not assessment:
        return jsonify({"error": "Assessment not found."}), 404

    profile = _get_profile_payload(user_id)
    if not profile:
        return jsonify({"error": "Complete your profile (interests/skills/goals) before requesting recommendations."}), 400

    missing = []
    if not profile.get("interests"):
        missing.append("interests")
    if not profile.get("skills"):
        missing.append("skills")
    if not profile.get("career_goals"):
        missing.append("career goals")

    if missing:
        return jsonify({
            "error": f"Complete your profile. Missing: {', '.join(missing)}.",
            "missing_fields": missing
        }), 400

    db = get_db()
    raw_courses = list(db.courses.find({})) if db else []
    all_courses = [_normalize_course_payload(c) for c in raw_courses]
    student_subjects = [
        {"subject_name": s.subject_name, "numeric_value": s.numeric_value}
        for s in assessment.converted_subjects
    ]

    top_results = generate_recommendations(
        all_courses=all_courses,
        student_subjects=student_subjects,
        student_interests=profile.get("interests", []),
        student_skills=profile.get("skills", []),
        student_career_goals=profile.get("career_goals", []),
        top_n=current_app.config.get("FREE_TIER_RECOMMENDATION_LIMIT", 10),
    )

    # Attach admission category for each result, using ONLY DB cut-off data.
    analyzer = CutOffAnalyzer()
    for result in top_results:
        classification = analyzer.analyze(result, assessment.aggregate_score)
        result["admission"] = classification

    serialized_results = _serialize_results(top_results)
    recommendation = Recommendation(
        user=user_id,
        assessment=assessment.id,
        results=[
            {
                "course_name": r["course_name"],
                "match_score": r["match_score"],
                "score_breakdown": r["score_breakdown"],
                "explanation_points": r["explanation_points"],
                "admission_category": (r["admission"] or {}).get("category") if r.get("admission") else None,
            }
            for r in top_results
        ],
    )
    recommendation.save()

    return jsonify(
        {
            "recommendation_id": str(recommendation.id),
            "top_courses": serialized_results,
            "results": serialized_results,
        }
    ), 200


@recommendation_bp.get("/latest")
@jwt_required()
def get_latest_recommendations():
    user_id = get_jwt_identity()
    recommendation = Recommendation.objects(user=user_id).order_by("-created_at").first()
    if not recommendation:
        return jsonify({"error": "No recommendations found. Run /recommend first."}), 404

    return jsonify(
        {
            "recommendation_id": str(recommendation.id),
            "top_courses": [
                {
                    "course_name": item.course_name,
                    "match_score": item.match_score,
                    "score_breakdown": item.score_breakdown.to_mongo().to_dict() if hasattr(item.score_breakdown, "to_mongo") else {},
                    "explanation_points": list(item.explanation_points or []),
                    "admission_category": item.admission_category,
                    "why_points": list(item.explanation_points or []),
                }
                for item in recommendation.results or []
            ],
        }
    ), 200
