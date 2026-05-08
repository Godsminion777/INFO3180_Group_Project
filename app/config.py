import os
from dotenv import load_dotenv

load_dotenv()


def _engine_options():
    db_url = os.getenv("DATABASE_URL", "")
    if db_url.startswith("sqlite"):
        return {}
    return {"connect_args": {"sslmode": "require"}}


class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = _engine_options()

    SESSION_COOKIE_SAMESITE = "None"
    SESSION_COOKIE_SECURE = True

    CORS_ORIGINS = os.getenv(
        "CORS_ORIGINS",
        "http://localhost:5173"
    ).split(",")

    SECRET_KEY = os.getenv(
        "SECRET_KEY",
        "INFO3180_GROUP_PROJECT_SECRET_KEY"
    )

    UPLOAD_FOLDER = os.path.join(os.getcwd(), "uploads")
