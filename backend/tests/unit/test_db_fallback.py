from flask import Flask

from app.config.database import init_db


def test_init_db_sets_local_fallback_when_uri_missing():
    app = Flask(__name__)
    app.config["MONGO_URI"] = None
    app.config["MONGO_DB_NAME"] = "unipath_test"

    init_db(app)

    assert app.config["DB_AVAILABLE"] is False
    assert "fallback_profiles" in app.config
    assert "fallback_assessments" in app.config
