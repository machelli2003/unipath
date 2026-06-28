"""
Seed career documents.
Run: python -m scripts.seed_careers  (from backend/)
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from datetime import datetime
from bson import ObjectId
from pymongo import MongoClient
from app.config.settings import get_config

Config = get_config()

CAREERS = [
    {
        "key": "software_engineer",
        "title": "Software Engineer",
        "industry": "Technology",
        "description": (
            "Design, develop, and maintain software systems and applications. "
            "Work in web, mobile, AI, embedded systems, or enterprise software."
        ),
        "related_courses": [
            "BSc Computer Science", "BSc Software Engineering",
            "BSc Computer Engineering", "BSc Information Technology",
        ],
        "required_skills": ["analytical_thinking", "problem_solving", "mathematics"],
        "interest_tags": ["tech_computing"],
        "salary_range": {"min": 2500, "max": 15000, "currency": "GHS", "period": "monthly"},
        "employment_rate": 85,
        "professional_body": "Ghana ICT Professionals Network",
    },
    {
        "key": "doctor",
        "title": "Medical Doctor",
        "industry": "Healthcare",
        "description": (
            "Diagnose, treat, and prevent illnesses in patients across specialisations "
            "such as general practice, surgery, paediatrics, obstetrics, and more."
        ),
        "related_courses": ["MBChB Medicine", "BSc Human Biology (Medicine)", "Bachelor of Medicine and Surgery"],
        "required_skills": ["analytical_thinking", "problem_solving", "communication"],
        "interest_tags": ["health_sciences"],
        "salary_range": {"min": 5000, "max": 30000, "currency": "GHS", "period": "monthly"},
        "employment_rate": 95,
        "professional_body": "Ghana Medical & Dental Council",
    },
    {
        "key": "nurse",
        "title": "Nurse / Midwife",
        "industry": "Healthcare",
        "description": (
            "Provide direct patient care, health education, and support in hospitals, "
            "clinics, and community settings. Midwives specialise in maternal and newborn care."
        ),
        "related_courses": ["BSc Nursing", "BSc Midwifery", "BSc Community Health Nursing"],
        "required_skills": ["communication", "teamwork", "problem_solving"],
        "interest_tags": ["health_sciences"],
        "salary_range": {"min": 2000, "max": 8000, "currency": "GHS", "period": "monthly"},
        "employment_rate": 92,
        "professional_body": "Nursing & Midwifery Council of Ghana",
    },
    {
        "key": "pharmacist",
        "title": "Pharmacist",
        "industry": "Healthcare",
        "description": (
            "Dispense medications, counsel patients, and ensure safe drug use in "
            "hospitals, retail pharmacies, research, and regulatory agencies."
        ),
        "related_courses": ["Doctor of Pharmacy", "BSc Pharmacy"],
        "required_skills": ["analytical_thinking", "problem_solving", "communication"],
        "interest_tags": ["health_sciences"],
        "salary_range": {"min": 3000, "max": 12000, "currency": "GHS", "period": "monthly"},
        "employment_rate": 88,
        "professional_body": "Pharmacy Council of Ghana",
    },
    {
        "key": "lawyer",
        "title": "Lawyer / Legal Practitioner",
        "industry": "Legal",
        "description": (
            "Represent clients in legal matters, draft contracts, provide legal counsel, "
            "and uphold justice across civil, criminal, commercial, and constitutional law."
        ),
        "related_courses": ["Bachelor of Laws (LLB)", "LLB Law"],
        "required_skills": ["communication", "analytical_thinking", "leadership"],
        "interest_tags": ["social_sciences"],
        "salary_range": {"min": 3000, "max": 20000, "currency": "GHS", "period": "monthly"},
        "employment_rate": 80,
        "professional_body": "Ghana Bar Association",
    },
    {
        "key": "engineer",
        "title": "Engineer",
        "industry": "Engineering & Construction",
        "description": (
            "Design, build, and maintain physical and digital infrastructure. "
            "Specialisations include civil, mechanical, electrical, chemical, and aerospace."
        ),
        "related_courses": [
            "BSc Civil Engineering", "BSc Mechanical Engineering",
            "BSc Electrical Engineering", "BSc Chemical Engineering",
        ],
        "required_skills": ["analytical_thinking", "problem_solving", "mathematics"],
        "interest_tags": ["engineering"],
        "salary_range": {"min": 3000, "max": 18000, "currency": "GHS", "period": "monthly"},
        "employment_rate": 82,
        "professional_body": "Ghana Institution of Engineering (GhIE)",
    },
    {
        "key": "accountant",
        "title": "Accountant / Finance Professional",
        "industry": "Finance & Accounting",
        "description": (
            "Manage financial records, audit accounts, prepare financial statements, "
            "and advise on tax and financial strategy for organisations."
        ),
        "related_courses": [
            "BBA Accounting", "BSc Accounting", "BSc Accounting and Finance",
            "BBA Banking and Finance", "BSc Auditing",
        ],
        "required_skills": ["analytical_thinking", "mathematics", "leadership"],
        "interest_tags": ["business"],
        "salary_range": {"min": 2500, "max": 15000, "currency": "GHS", "period": "monthly"},
        "employment_rate": 83,
        "professional_body": "Institute of Chartered Accountants Ghana (ICAG)",
    },
    {
        "key": "data_scientist",
        "title": "Data Scientist / Analyst",
        "industry": "Technology & Analytics",
        "description": (
            "Collect, analyse, and interpret large datasets to support decision-making "
            "using statistical models, machine learning, and data visualisation tools."
        ),
        "related_courses": [
            "BSc Data Science and Analytics", "BSc Statistics",
            "BSc Computer Science", "BSc Actuarial Science",
        ],
        "required_skills": ["analytical_thinking", "mathematics", "problem_solving"],
        "interest_tags": ["tech_computing"],
        "salary_range": {"min": 3000, "max": 20000, "currency": "GHS", "period": "monthly"},
        "employment_rate": 87,
        "professional_body": "Ghana Statistical Service",
    },
    {
        "key": "architect",
        "title": "Architect",
        "industry": "Built Environment",
        "description": (
            "Design functional and aesthetic buildings and spaces, overseeing projects "
            "from concept through construction within building codes and client briefs."
        ),
        "related_courses": ["BSc Architecture", "BSc Planning", "BSc Quantity Surveying"],
        "required_skills": ["creativity", "analytical_thinking", "mathematics"],
        "interest_tags": ["engineering"],
        "salary_range": {"min": 3000, "max": 15000, "currency": "GHS", "period": "monthly"},
        "employment_rate": 76,
        "professional_body": "Architects Registration Board",
    },
    {
        "key": "teacher",
        "title": "Teacher / Lecturer",
        "industry": "Education",
        "description": (
            "Educate and mentor students at basic, secondary, or tertiary levels across "
            "various subject areas, contributing to Ghana's human capital development."
        ),
        "related_courses": [
            "BA Education", "BEd Basic Education", "BEd Mathematics",
            "BEd Science", "BEd Computer Science",
        ],
        "required_skills": ["communication", "leadership", "teamwork"],
        "interest_tags": ["social_sciences", "arts"],
        "salary_range": {"min": 1800, "max": 8000, "currency": "GHS", "period": "monthly"},
        "employment_rate": 90,
        "professional_body": "National Teaching Council (NTC)",
    },
    {
        "key": "entrepreneur",
        "title": "Entrepreneur / Business Owner",
        "industry": "Business",
        "description": (
            "Start and manage businesses, identifying market opportunities, managing risk, "
            "and building organisations across sectors such as tech, agri, trade, and services."
        ),
        "related_courses": [
            "BSc Entrepreneurship", "BBA Business Administration",
            "BSc Agribusiness", "BSc Marketing",
        ],
        "required_skills": ["leadership", "creativity", "analytical_thinking"],
        "interest_tags": ["business", "entrepreneurship"],
        "salary_range": {"min": 1000, "max": 50000, "currency": "GHS", "period": "monthly"},
        "employment_rate": 70,
        "professional_body": "Association of Ghana Industries (AGI)",
    },
]


def run():
    client = MongoClient(Config.MONGO_URI)
    db = client[Config.MONGO_DB_NAME]

    index_info = db.careers.index_information()
    if "name_1" in index_info:
        db.careers.drop_index("name_1")
        print("Dropped legacy unique index on careers.name")

    db.careers.delete_many({})

    docs = []
    for c in CAREERS:
        docs.append({
            "_id": ObjectId(),
            "key": c["key"],
            "title": c["title"],
            "industry": c["industry"],
            "description": c["description"],
            "related_courses": c["related_courses"],
            "required_skills": c["required_skills"],
            "interest_tags": c["interest_tags"],
            "salary_range": c["salary_range"],
            "employment_rate": c["employment_rate"],
            "professional_body": c.get("professional_body", ""),
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow(),
        })

    result = db.careers.insert_many(docs)
    print(f"✅ Inserted {len(result.inserted_ids)} careers")
    client.close()


if __name__ == "__main__":
    run()
