import os
from pathlib import Path

from dotenv import load_dotenv


BASE_DIR = Path(__file__).resolve().parent.parent


load_dotenv(
    BASE_DIR / ".env",
    override=True
)


APP_NAME = "FitBuddy - AI Fitness Plan Generator"


GEMINI_API_KEY = (
    os.getenv("GEMINI_API_KEY")
    or os.getenv("GOOGLE_API_KEY")
)


GEMINI_WORKOUT_MODEL = os.getenv(
    "GEMINI_WORKOUT_MODEL",
    "gemini-3.5-flash",
)


GEMINI_NUTRITION_MODEL = os.getenv(
    "GEMINI_NUTRITION_MODEL",
    "gemini-3.5-flash",
)


ALLOW_DEMO_FALLBACK = (
    os.getenv(
        "ALLOW_DEMO_FALLBACK",
        "true"
    ).lower() == "true"
)


DATABASE_URL = os.getenv(
    "DATABASE_URL",
    f"sqlite:///{BASE_DIR / 'fitbuddy.db'}",
)


ADMIN_USERNAME = os.getenv(
    "ADMIN_USERNAME",
    "admin"
)


ADMIN_PASSWORD = os.getenv(
    "ADMIN_PASSWORD",
    "change-me"
)


MIN_AGE = int(
    os.getenv(
        "MIN_AGE",
        "13"
    )
)


MAX_AGE = int(
    os.getenv(
        "MAX_AGE",
        "100"
    )
)