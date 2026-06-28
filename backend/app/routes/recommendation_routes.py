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
from app.models.course import Course
from app.models.recommendation import Recommendation
from app.services.recommendation_engine.engine import generate_recommendations
from app.services.admission_engine.cut_off_analyzer import CutOffAnalyzer

recommendation_bp = Blueprint("recommendation", __name__)


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

    profile = StudentProfile.objects(user=user_id).first()
    if not profile:
        return jsonify({"error": "Complete your profile (interests/skills/goals) before requesting recommendations."}), 400

    all_courses = [c.to_mongo().to_dict() for c in Course.objects()]
    student_subjects = [
        {"subject_name": s.subject_name, "numeric_value": s.numeric_value}
        for s in assessment.converted_subjects
    ]

    top_results = generate_recommendations(
        all_courses=all_courses,
        student_subjects=student_subjects,
        student_interests=profile.interests,
        student_skills=[{"skill_name": s.skill_name, "rating": s.rating} for s in profile.skills],
        student_career_goals=profile.career_goals,
        top_n=current_app.config.get("FREE_TIER_RECOMMENDATION_LIMIT", 10),
    )

    # Attach admission category for each result, using ONLY DB cut-off data.
    analyzer = CutOffAnalyzer()
    for result in top_results:
        classification = analyzer.analyze(result, assessment.aggregate_score)
        result["admission"] = classification

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
            "results": top_results,
        }
    ), 200
