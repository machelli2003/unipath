"""
Seed cut-off points — one record per university+course combination.
Uses 2025 as primary year. Also synthesises 2022–2024 historical values.
Run: python -m scripts.seed_cut_offs  (from backend/)
"""
import sys, os, random
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from datetime import datetime
from bson import ObjectId
from pymongo import MongoClient
from app.config.settings import get_config

Config = get_config()
random.seed(42)


def _historical(base: int, year_offset: int) -> int:
    delta = random.choice([-1, -1, 0, 0, 1]) + year_offset
    return max(6, min(36, base + delta))


def run():
    client = MongoClient(Config.MONGO_URI)
    db = client[Config.MONGO_DB_NAME]

    index_info = db.cut_off_points.index_information()
    if "university_name_1_course_name_1_year_1" in index_info:
        db.cut_off_points.drop_index("university_name_1_course_name_1_year_1")
        print("Dropped legacy unique index on cut_off_points")

    courses = list(db.courses.find({}))
    if not courses:
        print("❌ No courses found. Run seed_courses.py first.")
        client.close()
        return

    db.cut_off_points.delete_many({})

    docs = []
    for course in courses:
        base = course["cut_off_2025"]
        uni_id = course["university_id"]
        uni_short = course["university_short"]
        course_id = str(course["_id"])

        for year, offset in [(2022, 2), (2023, 1), (2024, 0), (2025, 0)]:
            agg = _historical(base, offset) if year < 2025 else base
            docs.append({
                "_id": ObjectId(),
                "university_id": uni_id,
                "university_short": uni_short,
                "course_id": course_id,
                "course_name": course["name"],
                "year": year,
                "aggregate": agg,
                "competitiveness": course["competitiveness"],
                "category": course["category"],
                "created_at": datetime.utcnow(),
            })

    result = db.cut_off_points.insert_many(docs)
    print(f"✅ Inserted {len(result.inserted_ids)} cut-off records")
    print(f"   ({len(courses)} courses × 4 years)")
    client.close()


if __name__ == "__main__":
    run()
