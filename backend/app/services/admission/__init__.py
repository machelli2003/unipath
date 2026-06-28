"""Admission services package."""

from .classifier import admission_probability, classify_admission

__all__ = ["classify_admission", "admission_probability"]
