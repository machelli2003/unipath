from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from ...db.mongodb import get_db
from ...services.report_service import ReportService

report_bp = Blueprint("report", __name__)
report_service = ReportService()


@report_bp.get("")
@jwt_required()
def get_reports():
    user_id = get_jwt_identity()
    db = get_db()
    reports = list(db.reports.find({"user_id": user_id}, sort=[("created_at", -1)]))
    return jsonify(
        {
            "reports": [
                {
                    "id": str(r["_id"]),
                    "title": r.get("title", ""),
                    "created_at": r["created_at"].isoformat(),
                }
                for r in reports
            ]
        }
    ), 200


@report_bp.post("/generate")
@jwt_required()
def generate_report():
    user_id = get_jwt_identity()
    db = get_db()

    profile = db.student_profiles.find_one({"user_id": user_id})
    rec = db.recommendations.find_one({"student_id": user_id}, sort=[("generated_at", -1)])
    if not rec:
        return jsonify({"error": "No recommendation found. Run /recommend first."}), 404

    result = report_service.generate(user_id, profile, rec)
    return jsonify(result), 200
