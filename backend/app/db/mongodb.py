from mongoengine import connection


def get_db():
    """Return the active PyMongo database from mongoengine."""
    return connection.get_db(alias="default")
