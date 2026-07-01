from mongoengine import connection


def get_db():
    """Return the active PyMongo database from mongoengine."""
    try:
        return connection.get_db(alias="default")
    except Exception:  # pragma: no cover - runtime fallback path
        return None
