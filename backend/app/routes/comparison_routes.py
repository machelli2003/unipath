"""
app/routes/comparison_routes.py

POST /api/compare
Compares 2+ courses (skills vs careers vs difficulty) or universities,
side by side. Comparison data itself is pulled straight from the DB
(courses/universities collections) — deterministic. The AI layer is only
invoked to add prose-level commentary on top of the already-fetched facts.

Free tier limited to FREE_TIER_COMPARISON_LIMIT items per comparison.
"""

from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.models.user import User
from app.models.course import Course
from app.models.university import University

comparison_bp = Blueprint("comparison", __name__)


@comparison_bp.post("")
@jwt_required()
def compare_items():
    user_id = get_jwt_identity()
    payload = request.get_json(silent=True) or {}
    item_type = payload.get("type")  # "course" | "university"
    names = payload.get("names", [])

    user = User.objects(id=user_id).first()
    limit = (
        None
        if user and user.subscription_tier == "premium"
        else current_app.config.get("FREE_TIER_COMPARISON_LIMIT", 3)
    )
    if limit and len(names) > limit:
        return jsonify(
            {
                "error": f"Free tier allows comparing up to {limit} items at a time. Upgrade to Premium for unlimited comparisons.",
                "upgrade_required": True,
            }
        ), 402

    if item_type == "course":
        items = [c.to_mongo().to_dict() for c in Course.objects(name__in=names)]
    elif item_type == "university":
        items = [u.to_mongo().to_dict() for u in University.objects(name__in=names)]
    else:
        return jsonify({"error": "type must be 'course' or 'university'."}), 400

    return jsonify({"type": item_type, "items": items}), 200
