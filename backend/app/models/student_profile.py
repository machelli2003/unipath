"""
student_profiles collection

Holds everything the recommendation engine needs: SHS program, WASSCE
subjects/grades, interests, self-rated skills, and career goals. One profile
per user; supports the 3 student modes (official / awaiting / nov-dec).
"""

from datetime import datetime
from mongoengine import (
    Document,
    EmbeddedDocument,
    EmbeddedDocumentField,
    EmbeddedDocumentListField,
    StringField,
    IntField,
    ReferenceField,
    DateTimeField,
    ListField,
)

from app.models.user import User

# Canonical WASSCE grade scale (A1 best, F9 fail) — used by grade_converter.py
GRADE_CHOICES = ["A1", "B2", "B3", "C4", "C5", "C6", "D7", "E8", "F9"]

INTEREST_CHOICES = [
    "Tech & Computing",
    "Health Sciences",
    "Engineering",
    "Business",
    "Arts",
    "Social Sciences",
    "Entrepreneurship",
]

SKILL_CHOICES = [
    "Analytical Thinking",
    "Problem Solving",
    "Mathematics",
    "Communication",
    "Leadership",
    "Creativity",
    "Teamwork",
]

CAREER_GOAL_CHOICES = [
    "Software Engineer",
    "Doctor",
    "Lawyer",
    "Engineer",
    "Accountant",
    "Data Scientist",
]


class SubjectGrade(EmbeddedDocument):
    """A single WASSCE subject + grade pair."""
    subject_name = StringField(required=True)
    grade = StringField(choices=GRADE_CHOICES, required=True)
    # For Awaiting Results mode, students may give a 1-5 strength rating
    # instead of (or alongside) a mock grade.
    self_rated_strength = IntField(min_value=1, max_value=5)


class SkillRating(EmbeddedDocument):
    skill_name = StringField(choices=SKILL_CHOICES, required=True)
    rating = IntField(min_value=1, max_value=5, required=True)


class StudentProfile(Document):
    user = ReferenceField(User, required=True, unique=True)

    # ----- Mode -----
    mode = StringField(
        choices=["official_results", "awaiting_results", "nov_dec"],
        required=True,
    )

    # ----- Academic Data -----
    shs_program = StringField(required=True)
    subjects = EmbeddedDocumentListField(SubjectGrade)

    # Only populated in nov_dec mode: original grades kept separately so the
    # frontend can show a side-by-side "original vs improved" comparison.
    original_subjects = EmbeddedDocumentListField(SubjectGrade)

    # ----- Interests / Skills / Goals -----
    interests = ListField(StringField(choices=INTEREST_CHOICES))
    skills = EmbeddedDocumentListField(SkillRating)
    career_goals = ListField(StringField(choices=CAREER_GOAL_CHOICES))

    created_at = DateTimeField(default=datetime.utcnow)
    updated_at = DateTimeField(default=datetime.utcnow)

    meta = {
        "collection": "student_profiles",
        "indexes": ["user"],
    }
