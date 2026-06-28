"""
app/utils/validators.py

Shared helper to run a marshmallow schema and return (data, errors) in a
consistent shape so routes don't repeat try/except ValidationError blocks.
"""

from marshmallow import ValidationError


def validate_with_schema(schema, payload: dict):
    try:
        data = schema.load(payload)
        return data, None
    except ValidationError as err:
        return None, err.messages
