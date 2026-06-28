"""
app/middleware/rbac.py

Role-based access control decorators. Wrap a route with @role_required
to restrict it (e.g. admin-only seed/management endpoints). Wrap with
@premium_required to gate premium features (AI chat, simulator, PDF
reports) per the business model spec.
"""

from functools import wraps
from flask import jsonify
from flask_jwt_extended import get_jwt_identity, jwt_required

from app.models.user import User


def role_required(*allowed_roles):
    def decorator(fn):
        @wraps(fn)
        @jwt_required()
        def wrapper(*args, **kwargs):
            user = User.objects(id=get_jwt_identity()).first()
            if not user or user.role not in allowed_roles:
                return jsonify({"error": "You do not have permission to access this resource."}), 403
            return fn(*args, **kwargs)
        return wrapper
    return decorator


def premium_required(fn):
    @wraps(fn)
    @jwt_required()
    def wrapper(*args, **kwargs):
        user = User.objects(id=get_jwt_identity()).first()
        if not user or user.subscription_tier != "premium":
            return jsonify(
                {"error": "This feature requires a Premium subscription.", "upgrade_required": True}
            ), 402
        return fn(*args, **kwargs)
    return wrapper
