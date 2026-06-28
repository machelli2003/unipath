"""
Configuration classes for each environment.

get_config() picks the right class based on FLASK_ENV. Secrets are pulled
from environment variables (see .env.example) — never hardcode credentials.
"""

import os
from datetime import timedelta
from dotenv import load_dotenv

load_dotenv()


class BaseConfig:
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key")
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "dev-jwt-secret")
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(
        minutes=int(os.getenv("JWT_ACCESS_TOKEN_EXPIRES_MINUTES", 60))
    )
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(
        days=int(os.getenv("JWT_REFRESH_TOKEN_EXPIRES_DAYS", 30))
    )

    MONGO_URI = os.getenv("MONGO_URI")
    MONGO_DB_NAME = os.getenv("MONGO_DB_NAME", "unipath_ghana")

    FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:5173")

    ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
    AI_MODEL = os.getenv("AI_MODEL", "claude-sonnet-4-6")

    FREE_TIER_RECOMMENDATION_LIMIT = int(
        os.getenv("FREE_TIER_RECOMMENDATION_LIMIT", 10)
    )
    FREE_TIER_COMPARISON_LIMIT = int(os.getenv("FREE_TIER_COMPARISON_LIMIT", 3))

    DEBUG = False
    TESTING = False


class DevelopmentConfig(BaseConfig):
    DEBUG = True


class TestingConfig(BaseConfig):
    TESTING = True
    MONGO_DB_NAME = "unipath_ghana_test"


class ProductionConfig(BaseConfig):
    DEBUG = False


_CONFIG_MAP = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig,
}


def get_config(name: str = "development"):
    return _CONFIG_MAP.get(name, DevelopmentConfig)
