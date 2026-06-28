"""
app/utils/error_handlers.py

Centralized error handlers so every endpoint returns a consistent JSON
error shape instead of Flask's default HTML error pages.
"""

from flask import jsonify, Flask
from werkzeug.exceptions import HTTPException


def register_error_handlers(app: Flask) -> None:
    @app.errorhandler(404)
    def not_found(e):
        return jsonify({"error": "Resource not found."}), 404

    @app.errorhandler(400)
    def bad_request(e):
        return jsonify({"error": "Bad request."}), 400

    @app.errorhandler(HTTPException)
    def handle_http_exception(e):
        return jsonify({"error": e.description}), e.code

    @app.errorhandler(Exception)
    def handle_unexpected_error(e):
        app.logger.exception("Unhandled exception")
        return jsonify({"error": "An unexpected error occurred."}), 500
