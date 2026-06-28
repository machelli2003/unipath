"""
Create all MongoDB indexes needed for performance.
Run: python -m scripts.create_indexes  (from backend/)
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from pymongo import MongoClient, ASCENDING, DESCENDING, TEXT
from app.config.settings import get_config

Config = get_config()


def run():
    client = MongoClient(Config.MONGO_URI)
    db = client[Config.MONGO_DB_NAME]

    def ensure_index(collection, keys, **kwargs):
        try:
            collection.create_index(keys, **kwargs)
        except Exception as exc:
            if "already exists" in str(exc).lower() or "same name" in str(exc).lower():
                print(f"Index already exists for {collection.name}: {keys}")
            else:
                raise

    ensure_index(db.users, [("email", ASCENDING)], unique=True)
    ensure_index(db.student_profiles, [("user_id", ASCENDING)], unique=True)

    ensure_index(db.courses, [("university_short", ASCENDING)])
    ensure_index(db.courses, [("category", ASCENDING)])
    ensure_index(db.courses, [("cut_off_2025", ASCENDING)])
    ensure_index(db.courses, [("career_paths", ASCENDING)])
    ensure_index(db.courses, [("interest_tags", ASCENDING)])
    ensure_index(db.courses, [("name", TEXT)])

    ensure_index(db.universities, [("short_name", ASCENDING)], unique=True)

    ensure_index(db.cut_off_points, [
        ("university_id", ASCENDING),
        ("course_id", ASCENDING),
        ("year", DESCENDING),
    ])
    ensure_index(db.cut_off_points, [("course_id", ASCENDING), ("year", DESCENDING)])

    ensure_index(db.recommendations, [("student_id", ASCENDING), ("created_at", DESCENDING)])
    ensure_index(db.chat_history, [("user_id", ASCENDING), ("created_at", DESCENDING)])
    ensure_index(db.careers, [("key", ASCENDING)], unique=True)

    print("✅ All MongoDB indexes created")
    client.close()


if __name__ == "__main__":
    run()
