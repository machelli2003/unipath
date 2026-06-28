"""
scripts/seed_database.py

Loads the placeholder seed data (data/seed/*.json) into MongoDB Atlas.
Run with:
    python scripts/seed_database.py

IMPORTANT: the seed data is illustrative/placeholder data, NOT verified
admissions facts. Replace it with real, sourced data (official cut-off
lists, verified course/university details) before using this in
production — the whole system's "no hallucination" guarantee depends on
the DB itself only ever containing verified facts.
"""

import json
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from dotenv import load_dotenv
from mongoengine import connect

load_dotenv()

from app.models.course import Course
from app.models.university import University
from app.models.cut_off_point import CutOffPoint

SEED_DIR = os.path.join(os.path.dirname(__file__), "..", "data", "seed")


def load_json(filename: str) -> list:
    path = os.path.join(SEED_DIR, filename)
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def seed_courses():
    for entry in load_json("courses_seed.json"):
        Course.objects(name=entry["name"]).update_one(upsert=True, **{f"set__{k}": v for k, v in entry.items() if k != "name"})
    print(f"Seeded {Course.objects().count()} courses.")


def seed_universities():
    for entry in load_json("universities_seed.json"):
        University.objects(name=entry["name"]).update_one(upsert=True, **{f"set__{k}": v for k, v in entry.items() if k != "name"})
    print(f"Seeded {University.objects().count()} universities.")


def seed_cutoffs():
    for entry in load_json("cutoffs_seed.json"):
        CutOffPoint.objects(
            university_name=entry["university_name"],
            course_name=entry["course_name"],
            year=entry["year"],
        ).update_one(upsert=True, **{f"set__{k}": v for k, v in entry.items()})
    print(f"Seeded {CutOffPoint.objects().count()} cut-off records.")


if __name__ == "__main__":
    mongo_uri = os.getenv("MONGO_URI")
    db_name = os.getenv("MONGO_DB_NAME", "unipath_ghana")

    if not mongo_uri:
        raise SystemExit("MONGO_URI is not set. Copy .env.example to .env and add your MongoDB Atlas connection string.")

    connect(db=db_name, host=mongo_uri, alias="default")

    seed_courses()
    seed_universities()
    seed_cutoffs()

    print("\nSeeding complete. Remember: this is placeholder data — replace with verified sources before production.")
