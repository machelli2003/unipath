"""
UniPath Ghana - Flask Application Factory

Wires together config, MongoDB connection, JWT auth, CORS, and all route
blueprints. Keeping this as a factory (create_app) instead of a global app
instance makes it easy to spin up isolated app instances for testing.
"""

from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager

from app.config.settings import get_config
from app.config.database import init_db


def create_app(config_name: str = "development") -> Flask:
    app = Flask(__name__)
    app.config.from_object(get_config(config_name))

    # ----- Extensions -----
    CORS(app, resources={r"/api/*": {"origins": app.config["FRONTEND_URL"]}})
    JWTManager(app)
    init_db(app)

    # ----- Blueprints (API routes) -----
    from app.routes.auth_routes import auth_bp
    from app.routes.profile_routes import profile_bp
    from app.routes.assessment_routes import assessment_bp
    from app.routes.recommendation_routes import recommendation_bp
    from app.routes.simulation_routes import simulation_bp
    from app.routes.comparison_routes import comparison_bp
    from app.routes.report_routes import report_bp
    from app.routes.course_routes import course_bp
    from app.routes.university_routes import university_bp
    from app.routes.career_routes import career_bp
    from app.routes.chat_routes import chat_bp

    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(profile_bp, url_prefix="/api/profile")
    app.register_blueprint(assessment_bp, url_prefix="/api/assess")
    app.register_blueprint(recommendation_bp, url_prefix="/api/recommend")
    app.register_blueprint(simulation_bp, url_prefix="/api/simulate")
    app.register_blueprint(comparison_bp, url_prefix="/api/compare")
    app.register_blueprint(report_bp, url_prefix="/api/report")
    app.register_blueprint(course_bp, url_prefix="/api/courses")
    app.register_blueprint(university_bp, url_prefix="/api/universities")
    app.register_blueprint(career_bp, url_prefix="/api/careers")
    app.register_blueprint(chat_bp, url_prefix="/api/chat")

    # ----- Error handlers -----
    from app.utils.error_handlers import register_error_handlers
    register_error_handlers(app)

    @app.get("/api/health")
    def health_check():
        return {"status": "ok", "service": "unipath-ghana-api"}, 200

    return app
