import os
from dotenv import load_dotenv


load_dotenv()


def _engine_options():
    db_url = os.getenv("DATABASE_URL", "")
    if db_url.startswith("sqlite"):
        return {}
    if "localhost" in db_url or "127.0.0.1" in db_url:
        return {}
    return {"connect_args": {"sslmode": "require"}}


class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite:///dev.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = _engine_options()

    CORS_ORIGINS = os.getenv(
        "CORS_ORIGINS",
        "http://localhost:5173"
    ).split(",")

    SECRET_KEY = os.getenv(
        "SECRET_KEY",
        "INFO3180_GROUP_PROJECT_SECRET_KEY"
    )

    SESSION_COOKIE_HTTPONLY = os.getenv("SESSION_COOKIE_HTTPONLY", "True")
    SESSION_COOKIE_SAMESITE = os.getenv("SESSION_COOKIE_SAMESITE", "Lax")
    SESSION_COOKIE_SECURE = os.getenv("SESSION_COOKIE_SECURE", "False")


    UPLOAD_FOLDER = os.path.join(os.getcwd(), "uploads")
