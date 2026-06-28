"""
MongoDB Atlas connection setup.

Uses mongoengine for ODM-style document models (see app/models/). Connection
is established once when the Flask app is created.
"""

from flask import Flask
from mongoengine import connect, disconnect


def init_db(app: Flask) -> None:
    """Connect to MongoDB Atlas using the URI from config."""
    mongo_uri = app.config.get("MONGO_URI")
    db_name = app.config.get("MONGO_DB_NAME")

    if not mongo_uri:
        raise RuntimeError(
            "MONGO_URI is not set. Copy .env.example to .env and add your "
            "MongoDB Atlas connection string."
        )

    # Disconnect any existing alias (useful when re-creating app in tests)
    disconnect(alias="default")

    connect(
        db=db_name,
        host=mongo_uri,
        alias="default",
    )
