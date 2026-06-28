"""
app/schemas/auth_schema.py

Marshmallow schemas validating request bodies for auth endpoints, before
any data reaches the database.
"""

from marshmallow import Schema, fields, validate


class RegisterSchema(Schema):
    full_name = fields.String(required=True, validate=validate.Length(min=2, max=120))
    email = fields.Email(required=True)
    password = fields.String(required=True, validate=validate.Length(min=8))


class LoginSchema(Schema):
    email = fields.Email(required=True)
    password = fields.String(required=True)
