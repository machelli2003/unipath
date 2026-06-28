"""
app/schemas/assessment_schema.py
"""

from marshmallow import Schema, fields, validate

from app.models.student_profile import GRADE_CHOICES


class SubjectGradeSchema(Schema):
    subject_name = fields.String(required=True)
    grade = fields.String(required=True, validate=validate.OneOf(GRADE_CHOICES))


class AssessmentSchema(Schema):
    mode = fields.String(
        required=True,
        validate=validate.OneOf(["official_results", "awaiting_results", "nov_dec"]),
    )
    subjects = fields.List(fields.Nested(SubjectGradeSchema), required=True, validate=validate.Length(min=1))
    is_simulation = fields.Boolean(required=False, load_default=False)
