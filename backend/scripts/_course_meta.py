"""
Master mapping file — subject requirements, SHS eligibility,
career paths, skills, interest tags, difficulty, duration.
Imported by seed_courses.py and seed_cut_offs.py.
"""

# ── University ObjectId map ────────────────────────────────
UNI_IDS = {
    "KNUST": "6650000000000000000000a1",
    "UG": "6650000000000000000000a2",
    "UCC": "6650000000000000000000a3",
    "UDS": "6650000000000000000000a4",
    "UPSA": "6650000000000000000000a5",
}

# ── Core subjects always required ─────────────────────────
CORE_ENGLISH = "English Language (Core)"
CORE_MATHS = "Mathematics (Core)"
CORE_SCIENCE = "Integrated Science (Core)"
CORE_SOCIAL = "Social Studies (Core)"

# ── Electives ─────────────────────────────────────────────
EL_MATHS = "Elective Mathematics"
EL_PHYSICS = "Physics"
EL_CHEM = "Chemistry"
EL_BIO = "Biology"
EL_ECON = "Economics"
EL_ACCT = "Financial Accounting"
EL_BIZ = "Business Management"
EL_GEOG = "Geography"
EL_GOV = "Government"
EL_LIT = "Literature in English"
EL_AGRIC = "Agricultural Science"
EL_ICT = "Information & Communication Technology"
EL_ART = "General Knowledge in Art"
EL_FOOD = "Foods & Nutrition"
EL_CLOTH = "Clothing & Textiles"
EL_MUSIC = "Music"
EL_FRENCH = "French"

SCI_CORE = [CORE_ENGLISH, CORE_MATHS, CORE_SCIENCE]
BIZ_CORE = [CORE_ENGLISH, CORE_MATHS]

# ── SHS Programme eligibility ─────────────────────────────
SHS_SCIENCE = ["Science"]
SHS_BUSINESS = ["Business"]
SHS_ARTS = ["General Arts"]
SHS_VISUAL = ["Visual Arts"]
SHS_HOME_EC = ["Home Economics"]
SHS_AGRIC = ["Agricultural Science"]
SHS_TECH = ["Technical"]
SHS_ANY = ["Science", "Business", "General Arts", "Visual Arts", "Home Economics", "Agricultural Science", "Technical"]
SHS_SCI_TECH = ["Science", "Technical"]
SHS_SCI_BIZ = ["Science", "Business"]
SHS_SCI_BIZ_ARTS = ["Science", "Business", "General Arts"]
SHS_SCI_AGRIC = ["Science", "Agricultural Science"]
SHS_BIZ_ARTS = ["Business", "General Arts"]
SHS_BIZ_ARTS_SCI = ["Business", "General Arts", "Science"]
SHS_ARTS_SCI = ["General Arts", "Science"]

# ── Duration lookup ───────────────────────────────────────
def get_duration(name: str) -> int:
    n = name.lower()
    if any(k in n for k in ["mbchb", "medicine", "surgery", "pharmacy", "pharm", "dentistry", "dental", "veterinary", "optometry"]):
        return 6
    if "diploma" in n:
        return 2
    return 4

# ── Category → required subjects ─────────────────────────
SUBJECT_MAP = {
    "Engineering": (SCI_CORE, [EL_MATHS, EL_PHYSICS, EL_CHEM]),
    "Health": (SCI_CORE, [EL_BIO, EL_CHEM, EL_PHYSICS]),
    "Health Sciences": (SCI_CORE, [EL_BIO, EL_CHEM, EL_PHYSICS]),
    "Science": (SCI_CORE, [EL_MATHS, EL_PHYSICS, EL_CHEM]),
    "Computing": (SCI_CORE, [EL_MATHS, EL_ICT]),
    "Technology": (SCI_CORE, [EL_MATHS, EL_ICT]),
    "Agriculture": (SCI_CORE, [EL_BIO, EL_AGRIC, EL_CHEM]),
    "Built Environment": (SCI_CORE, [EL_MATHS, EL_PHYSICS]),
    "Business": (BIZ_CORE, [EL_ECON, EL_ACCT, EL_BIZ]),
    "Law": (BIZ_CORE, [EL_LIT, EL_GOV, EL_ECON]),
    "Social Science": (BIZ_CORE, [EL_ECON, EL_GOV, EL_GEOG]),
    "Social Sciences": (BIZ_CORE, [EL_ECON, EL_GOV, EL_GEOG]),
    "Arts": (BIZ_CORE, [EL_LIT, EL_GOV, EL_ECON]),
    "Arts & Humanities": (BIZ_CORE, [EL_LIT, EL_GOV, EL_ECON]),
    "Humanities": (BIZ_CORE, [EL_LIT, EL_GOV, EL_ECON]),
    "Education": (BIZ_CORE, [EL_LIT, EL_ECON, EL_GOV]),
    "Sciences": (SCI_CORE, [EL_BIO, EL_CHEM, EL_MATHS]),
}

# ── Category → SHS programmes allowed ─────────────────────
SHS_MAP = {
    "Engineering": SHS_SCI_TECH,
    "Health": SHS_SCIENCE,
    "Health Sciences": SHS_SCIENCE,
    "Science": SHS_SCI_BIZ,
    "Sciences": SHS_SCI_BIZ,
    "Computing": SHS_SCI_BIZ_ARTS,
    "Technology": SHS_SCI_BIZ_ARTS,
    "Agriculture": SHS_SCI_AGRIC,
    "Built Environment": SHS_SCI_TECH,
    "Business": SHS_BIZ_ARTS_SCI,
    "Law": SHS_ANY,
    "Social Science": SHS_BIZ_ARTS,
    "Social Sciences": SHS_BIZ_ARTS,
    "Arts": SHS_ARTS_SCI,
    "Arts & Humanities": SHS_ARTS_SCI,
    "Humanities": SHS_ARTS_SCI,
    "Education": SHS_ANY,
}

# ── Category → interest tags ──────────────────────────────
INTEREST_MAP = {
    "Engineering": ["engineering", "tech_computing"],
    "Health": ["health_sciences"],
    "Health Sciences": ["health_sciences"],
    "Science": ["health_sciences", "engineering"],
    "Sciences": ["health_sciences"],
    "Computing": ["tech_computing"],
    "Technology": ["tech_computing"],
    "Agriculture": ["health_sciences", "social_sciences"],
    "Built Environment": ["engineering"],
    "Business": ["business", "entrepreneurship"],
    "Law": ["social_sciences"],
    "Social Science": ["social_sciences"],
    "Social Sciences": ["social_sciences"],
    "Arts": ["arts"],
    "Arts & Humanities": ["arts"],
    "Humanities": ["arts"],
    "Education": ["social_sciences", "arts"],
}

# ── Category → required skills ────────────────────────────
SKILLS_MAP = {
    "Engineering": ["analytical_thinking", "problem_solving", "mathematics"],
    "Health": ["analytical_thinking", "problem_solving", "communication"],
    "Health Sciences": ["analytical_thinking", "problem_solving", "communication"],
    "Science": ["analytical_thinking", "mathematics", "problem_solving"],
    "Sciences": ["analytical_thinking", "mathematics"],
    "Computing": ["analytical_thinking", "problem_solving", "mathematics"],
    "Technology": ["analytical_thinking", "problem_solving"],
    "Agriculture": ["problem_solving", "teamwork"],
    "Built Environment": ["analytical_thinking", "creativity", "mathematics"],
    "Business": ["leadership", "communication", "analytical_thinking"],
    "Law": ["communication", "analytical_thinking", "leadership"],
    "Social Science": ["communication", "analytical_thinking", "teamwork"],
    "Social Sciences": ["communication", "analytical_thinking", "teamwork"],
    "Arts": ["creativity", "communication"],
    "Arts & Humanities": ["creativity", "communication"],
    "Humanities": ["creativity", "communication"],
    "Education": ["communication", "leadership", "teamwork"],
}

# ── Category → career paths ───────────────────────────────
CAREER_MAP = {
    "Engineering": ["engineer", "software_engineer", "data_scientist"],
    "Health": ["doctor", "nurse", "pharmacist"],
    "Health Sciences": ["doctor", "nurse", "pharmacist"],
    "Science": ["doctor", "data_scientist", "engineer"],
    "Sciences": ["doctor", "nurse"],
    "Computing": ["software_engineer", "data_scientist"],
    "Technology": ["software_engineer", "data_scientist"],
    "Agriculture": ["entrepreneur", "teacher"],
    "Built Environment": ["engineer", "architect"],
    "Business": ["accountant", "entrepreneur", "lawyer"],
    "Law": ["lawyer"],
    "Social Science": ["teacher", "lawyer", "entrepreneur"],
    "Social Sciences": ["teacher", "lawyer", "entrepreneur"],
    "Arts": ["teacher", "entrepreneur"],
    "Arts & Humanities": ["teacher", "entrepreneur"],
    "Humanities": ["teacher"],
    "Education": ["teacher"],
}

# ── Category → difficulty ─────────────────────────────────
DIFFICULTY_MAP = {
    "Engineering": "high",
    "Health": "high",
    "Health Sciences": "high",
    "Science": "high",
    "Sciences": "medium",
    "Computing": "medium",
    "Technology": "medium",
    "Agriculture": "medium",
    "Built Environment": "medium",
    "Business": "medium",
    "Law": "high",
    "Social Science": "medium",
    "Social Sciences": "medium",
    "Arts": "low",
    "Arts & Humanities": "low",
    "Humanities": "low",
    "Education": "low",
}

# ── Programme name → specific career overrides ────────────
CAREER_OVERRIDES = {
    "computer science": ["software_engineer", "data_scientist"],
    "software engineering": ["software_engineer"],
    "data science": ["data_scientist", "software_engineer"],
    "cyber security": ["software_engineer", "data_scientist"],
    "information technology": ["software_engineer", "data_scientist"],
    "medicine": ["doctor"],
    "pharmacy": ["pharmacist"],
    "nursing": ["nurse"],
    "midwifery": ["nurse"],
    "law": ["lawyer"],
    "accounting": ["accountant"],
    "finance": ["accountant"],
    "banking": ["accountant"],
    "economics": ["accountant", "entrepreneur"],
    "architecture": ["architect", "engineer"],
    "civil engineering": ["engineer"],
    "mechanical engineering": ["engineer"],
    "electrical engineering": ["engineer", "software_engineer"],
    "chemical engineering": ["engineer"],
    "biomedical engineering": ["engineer", "doctor"],
    "agricultural engineering": ["engineer"],
}


def get_career_override(name: str) -> list | None:
    n = name.lower()
    for key, careers in CAREER_OVERRIDES.items():
        if key in n:
            return careers
    return None

# ── Demand → competitiveness ──────────────────────────────
DEMAND_MAP = {
    "Very High": "very_high",
    "High": "high",
    "Medium": "medium",
    "Low": "low",
}
