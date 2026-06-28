"""
app/routes/auth_routes.py

POST /api/auth/register
POST /api/auth/login

Password hashing via bcrypt, tokens via flask-jwt-extended. Validation goes
through app/schemas/auth_schema.py before touching the DB.
"""

from datetime import datetime
from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, create_refresh_token
import bcrypt

from app.models.user import User
from app.schemas.auth_schema import RegisterSchema, LoginSchema
from app.utils.validators import validate_with_schema

auth_bp = Blueprint("auth", __name__)


@auth_bp.post("/register")
def register():
    data, errors = validate_with_schema(RegisterSchema(), request.get_json(silent=True) or {})
    if errors:
        return jsonify({"errors": errors}), 400

    if User.objects(email=data["email"]).first():
        return jsonify({"error": "An account with this email already exists."}), 409

    password_hash = bcrypt.hashpw(data["password"].encode("utf-8"), bcrypt.gensalt())

    user = User(
        full_name=data["full_name"],
        email=data["email"],
        password_hash=password_hash.decode("utf-8"),
    )
    user.save()

    access_token = create_access_token(identity=str(user.id))
    refresh_token = create_refresh_token(identity=str(user.id))

    return jsonify(
        {
            "user": user.to_public_dict(),
            "access_token": access_token,
            "refresh_token": refresh_token,
        }
    ), 201


@auth_bp.post("/login")
def login():
    data, errors = validate_with_schema(LoginSchema(), request.get_json(silent=True) or {})
    if errors:
        return jsonify({"errors": errors}), 400

    user = User.objects(email=data["email"]).first()
    if not user or not bcrypt.checkpw(
        data["password"].encode("utf-8"), user.password_hash.encode("utf-8")
    ):
        return jsonify({"error": "Invalid email or password."}), 401

    if not user.is_active:
        return jsonify({"error": "This account has been deactivated."}), 403

    user.last_login_at = datetime.utcnow()
    user.save()

    access_token = create_access_token(identity=str(user.id))
    refresh_token = create_refresh_token(identity=str(user.id))

    return jsonify(
        {
            "user": user.to_public_dict(),
            "access_token": access_token,
            "refresh_token": refresh_token,
        }
    ), 200
