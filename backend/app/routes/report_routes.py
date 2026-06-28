"""
app/routes/report_routes.py

POST /api/report
Generates a PDF report (recommendation summary / career roadmap) from an
existing Recommendation document. Premium feature. PDF rendering itself is
handled by app/services/report_service (not shown here in route logic to
keep this file thin) — see services layer for the actual reportlab/
WeasyPrint implementation.
"""

from flask import Blueprint, request, jsonify, send_file
from flask_jwt_extended import get_jwt_identity

from app.models.recommendation import Recommendation
from app.models.report import Report
from app.middleware.rbac import premium_required

report_bp = Blueprint("report", __name__)


@report_bp.post("")
@premium_required
def generate_report():
    user_id = get_jwt_identity()
    payload = request.get_json(silent=True) or {}
    recommendation_id = payload.get("recommendation_id")
    report_type = payload.get("report_type", "recommendation_summary")

    recommendation = Recommendation.objects(id=recommendation_id, user=user_id).first()
    if not recommendation:
        return jsonify({"error": "Recommendation not found."}), 404

    # NOTE: actual PDF generation is implemented in
    # app/services/report_service.py (reportlab/WeasyPrint) — wire it in
    # here once that service module is built out.
    file_path = f"/tmp/reports/{recommendation_id}_{report_type}.pdf"

    report = Report(
        user=user_id,
        recommendation=recommendation.id,
        report_type=report_type,
        file_path=file_path,
    )
    report.save()

    return jsonify({"report_id": str(report.id), "file_path": file_path}), 201


@report_bp.get("/<report_id>/download")
@premium_required
def download_report(report_id):
    user_id = get_jwt_identity()
    report = Report.objects(id=report_id, user=user_id).first()
    if not report:
        return jsonify({"error": "Report not found."}), 404
    return send_file(report.file_path, as_attachment=True)
