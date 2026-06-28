"""
Seed the 5 universities into MongoDB.
Run: python -m scripts.seed_universities  (from backend/)
"""
from datetime import datetime
from bson import ObjectId
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.config.settings import get_config
from pymongo import MongoClient

Config = get_config()

UNIVERSITIES = [
    {
        "_id": ObjectId("6650000000000000000000a1"),
        "short_name": "KNUST",
        "name": "Kwame Nkrumah University of Science and Technology",
        "location": "Kumasi, Ashanti Region, Ghana",
        "type": "Public",
        "established": 1952,
        "website": "https://www.knust.edu.gh",
        "overview": (
            "A leading science and technology university in Ghana, renowned for engineering, "
            "science, medicine, business, and innovation. It operates a collegiate system and "
            "is one of Africa's top research universities."
        ),
        "faculties": [
            "College of Agriculture & Natural Resources",
            "College of Art & Built Environment",
            "College of Engineering",
            "College of Health Sciences",
            "College of Humanities & Social Sciences",
            "College of Science",
        ],
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow(),
    },
    {
        "_id": ObjectId("6650000000000000000000a2"),
        "short_name": "UG",
        "name": "University of Ghana",
        "location": "Legon, Accra, Greater Accra Region, Ghana",
        "type": "Public",
        "established": 1948,
        "website": "https://www.ug.edu.gh",
        "overview": (
            "Ghana's oldest and largest university, offering comprehensive education and research "
            "across humanities, sciences, business, law, medicine, engineering, and social sciences."
        ),
        "faculties": [
            "College of Basic & Applied Sciences",
            "College of Education",
            "College of Health Sciences",
            "College of Humanities",
            "College of Social Sciences",
        ],
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow(),
    },
    {
        "_id": ObjectId("6650000000000000000000a3"),
        "short_name": "UCC",
        "name": "University of Cape Coast",
        "location": "Cape Coast, Central Region, Ghana",
        "type": "Public",
        "established": 1962,
        "website": "https://www.ucc.edu.gh",
        "overview": (
            "A premier public university recognised for teacher education, research, health sciences, "
            "business, and humanities, while also offering strong science and technology programmes."
        ),
        "faculties": [
            "Faculty of Humanities & Social Sciences Education",
            "Faculty of Educational Foundations",
            "Faculty of Science & Technology Education",
            "School of Business",
            "School of Medical Sciences",
            "School of Biological Sciences",
            "School of Physical Sciences",
            "School of Agriculture",
            "School of Nursing & Midwifery",
            "School of Allied Health Sciences",
            "School of Economics",
        ],
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow(),
    },
    {
        "_id": ObjectId("6650000000000000000000a4"),
        "short_name": "UDS",
        "name": "University for Development Studies",
        "location": "Tamale, Northern Region, Ghana",
        "type": "Public",
        "established": 1992,
        "website": "https://www.uds.edu.gh",
        "overview": (
            "A multi-campus public university focused on practical education, community engagement, "
            "agriculture, health sciences, engineering, natural resources, and sustainable development "
            "in Northern Ghana."
        ),
        "faculties": [
            "Faculty of Agriculture, Food & Consumer Sciences",
            "Faculty of Biosciences",
            "Faculty of Communication & Cultural Studies",
            "Faculty of Education",
            "Faculty of Environment & Sustainable Development",
            "Faculty of Mathematical Sciences",
            "Faculty of Physical Sciences",
            "School of Engineering",
            "School of Medicine",
            "School of Nursing & Midwifery",
            "School of Allied Health Sciences",
            "School of Public Health",
            "School of Veterinary Medicine",
            "Graduate School",
        ],
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow(),
    },
    {
        "_id": ObjectId("6650000000000000000000a5"),
        "short_name": "UPSA",
        "name": "University of Professional Studies, Accra",
        "location": "Madina, Accra, Greater Accra Region, Ghana",
        "type": "Public",
        "established": 1965,
        "website": "https://www.upsa.edu.gh",
        "overview": (
            "A public university specialising in business, accounting, management, law, information "
            "technology, communications, and professional education. It is Ghana's leading "
            "professional university."
        ),
        "faculties": [
            "Faculty of Accounting & Finance",
            "Faculty of Information Technology & Communication Studies",
            "Faculty of Management Studies",
            "UPSA Law School",
            "School of Graduate Studies",
            "Distance Learning School",
        ],
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow(),
    },
]


def run():
    client = MongoClient(Config.MONGO_URI)
    db = client[Config.MONGO_DB_NAME]

    db.universities.delete_many({"short_name": {"$in": ["KNUST", "UG", "UCC", "UDS", "UPSA"]}})
    result = db.universities.insert_many(UNIVERSITIES)
    print(f"✅ Inserted {len(result.inserted_ids)} universities")

    mapping = {u["short_name"]: str(u["_id"]) for u in UNIVERSITIES}
    print("University ID map:", mapping)
    client.close()


if __name__ == "__main__":
    run()
