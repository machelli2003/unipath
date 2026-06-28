from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime
from bson import ObjectId

from ...db.mongodb import get_db

assess_bp = Blueprint("assess", __name__)


@assess_bp.post("")
@jwt_required()
def submit_assessment():
    user_id = get_jwt_identity()
    data = request.get_json() or {}
    db = get_db()

    doc = {
        "_id": ObjectId(),
        "user_id": user_id,
        "data": data,
        "created_at": datetime.utcnow(),
    }
    db.assessments.insert_one(doc)
    return jsonify({"message": "Assessment saved.", "id": str(doc["_id"])}), 201
