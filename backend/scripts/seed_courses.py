"""
Seed all degree-level courses from the 5 university CSVs.
Skips diplomas, evening, distance, IDL, sandwich, weekend variants.
Run: python -m scripts.seed_courses  (from backend/)
"""
import sys, os, re
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from datetime import datetime
from bson import ObjectId
import pandas as pd
from pymongo import MongoClient
from app.config.settings import get_config
from scripts._course_meta import (
    UNI_IDS, SUBJECT_MAP, SHS_MAP, INTEREST_MAP, SKILLS_MAP,
    CAREER_MAP, DIFFICULTY_MAP, get_duration, get_career_override,
    DEMAND_MAP,
)

Config = get_config()

CSV_FILES = {
    "KNUST": "C:/Users/Machelli/Desktop/unipath/backend/data/seed/knust_programmes.csv",
    "UG": "C:/Users/Machelli/Desktop/unipath/backend/data/seed/ug_programmes.csv",
    "UCC": "C:/Users/Machelli/Desktop/unipath/backend/data/seed/ucc_programmes.csv",
    "UDS": "C:/Users/Machelli/Desktop/unipath/backend/data/seed/uds.csv",
    "UPSA": "C:/Users/Machelli/Desktop/unipath/backend/data/seed/upsa.csv",
}

SKIP_PATTERNS = [
    r"\(evening\)", r"\(distance\)", r"\(idl\)", r"\(weekend\)",
    r"\(sandwich\)", r"\(code\)", r"\(obuasi campus\)", r"\(accra city campus\)",
    r"\(kumasi city campus\)", r"diploma in", r"^diploma ",
]


def should_skip(name: str) -> bool:
    n = name.lower()
    return any(re.search(p, n) for p in SKIP_PATTERNS)


def build_course_doc(programme: str, cut_off: int, demand: str, category: str, uni_short: str) -> dict:
    cat = category.strip()
    subj_core, subj_elec = SUBJECT_MAP.get(cat, (["English Language (Core)", "Mathematics (Core)"], []))
    shs_progs = SHS_MAP.get(cat, ["Science", "Business", "General Arts"])
    interests = INTEREST_MAP.get(cat, ["social_sciences"])
    skills = SKILLS_MAP.get(cat, ["analytical_thinking", "communication"])
    difficulty = DIFFICULTY_MAP.get(cat, "medium")
    duration = get_duration(programme)
    careers = get_career_override(programme) or CAREER_MAP.get(cat, ["teacher", "entrepreneur"])

    description = (
        f"{programme} offered at {uni_short}. "
        f"A {duration}-year {cat.lower()} programme with a cut-off aggregate of {cut_off}. "
        f"Graduates pursue careers in {', '.join(careers[:2])} and related fields."
    )

    return {
        "_id": ObjectId(),
        "name": programme,
        "university_short": uni_short,
        "university_id": UNI_IDS[uni_short],
        "category": cat,
        "faculty": cat,
        "duration_years": duration,
        "cut_off_2025": cut_off,
        "competitiveness": DEMAND_MAP.get(demand, "medium"),
        "difficulty": difficulty,
        "required_subjects": subj_core + subj_elec,
        "core_subjects": subj_core,
        "elective_subjects": subj_elec,
        "eligible_shs_programmes": shs_progs,
        "interest_tags": interests,
        "required_skills": skills,
        "career_paths": careers,
        "description": description,
        "national_service": duration >= 4,
        "internship_required": cat in ["Engineering", "Health", "Health Sciences", "Computing", "Technology"],
        "professional_body": _get_prof_body(programme, cat),
        "related_courses": [],
        "average_cut_off": cut_off,
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow(),
    }


def _get_prof_body(name: str, cat: str) -> str:
    n = name.lower()
    if "medicine" in n or "mbchb" in n:
        return "Ghana Medical & Dental Council"
    if "pharmacy" in n or "pharmacist" in n:
        return "Pharmacy Council of Ghana"
    if "nursing" in n or "midwifery" in n:
        return "Nursing & Midwifery Council"
    if "law" in n or "llb" in n:
        return "Ghana Bar Association"
    if "accounti" in n or "audit" in n:
        return "Institute of Chartered Accountants Ghana (ICAG)"
    if "engineering" in n:
        return "Ghana Institution of Engineering (GhIE)"
    if "architecture" in n:
        return "Architects Registration Board"
    if "veterinary" in n:
        return "Veterinary Council of Ghana"
    if "optometry" in n:
        return "Ghana Optometric Association"
    if "physiotherapy" in n:
        return "Allied Health Professions Council"
    return ""


def run():
    client = MongoClient(Config.MONGO_URI)
    db = client[Config.MONGO_DB_NAME]

    index_info = db.courses.index_information()
    if "name_1" in index_info:
        db.courses.drop_index("name_1")
        print("Dropped legacy unique index on courses.name")

    db.courses.delete_many({})

    all_docs = []

    for uni_short, csv_path in CSV_FILES.items():
        df = pd.read_csv(csv_path)
        prog_col = "Programme"
        co_col = "Cut-Off" if "Cut-Off" in df.columns else "CutOffPoints"
        demand_col = "Demand" if "Demand" in df.columns else "CompetitionLevel"
        cat_col = "Category" if "Category" in df.columns else "FacultyCategory"
        level_col = "Level" if "Level" in df.columns else "AwardType"

        df = df[df[level_col] == "Degree"]
        df = df[~df[prog_col].apply(should_skip)]

        print(f"\n{uni_short}: {len(df)} programmes to seed")

        for _, row in df.iterrows():
            doc = build_course_doc(
                programme=str(row[prog_col]).strip(),
                cut_off=int(row[co_col]),
                demand=str(row[demand_col]).strip(),
                category=str(row[cat_col]).strip(),
                uni_short=uni_short,
            )
            all_docs.append(doc)
            print(f"  ✓ {doc['name']} [{doc['category']}] cut-off:{doc['cut_off_2025']}")

    if all_docs:
        result = db.courses.insert_many(all_docs)
        print(f"\n✅ Inserted {len(result.inserted_ids)} courses across 5 universities")
    else:
        print("⚠️  No courses inserted")

    client.close()


if __name__ == "__main__":
    run()
