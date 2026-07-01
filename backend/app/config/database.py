"""
MongoDB Atlas connection setup.

Uses mongoengine for ODM-style document models (see app/models/). Connection
is established once when the Flask app is created.
"""

from flask import Flask
from mongoengine import connect, disconnect


def init_db(app: Flask) -> None:
    """Connect to MongoDB Atlas using the URI from config, but fall back safely."""
    mongo_uri = app.config.get("MONGO_URI")
    db_name = app.config.get("MONGO_DB_NAME")

    disconnect(alias="default")

    if not mongo_uri:
        app.config["DB_AVAILABLE"] = False
        app.config["DB_ERROR"] = "MONGO_URI is not set; using local fallback storage."
        app.config.setdefault("fallback_profiles", {})
        app.config.setdefault("fallback_assessments", {})
        return

    try:
        connect(
            db=db_name,
            host=mongo_uri,
            alias="default",
            serverSelectionTimeoutMS=2000,
        )
        app.config["DB_AVAILABLE"] = True
        app.config["DB_ERROR"] = None
    except Exception as exc:  # pragma: no cover - runtime fallback path
        app.config["DB_AVAILABLE"] = False
        app.config["DB_ERROR"] = str(exc)
        app.config.setdefault("fallback_profiles", {})
        app.config.setdefault("fallback_assessments", {})
