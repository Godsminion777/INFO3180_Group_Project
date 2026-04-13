import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    SQLALCHEMY_ENGINE_OPTIONS = {
        "connect_args": {"sslmode": "require"}
    }

    CORS_ORIGINS = os.getenv(
        "CORS_ORIGINS",
        "http://localhost:5173"
    ).split(",")

    SECRET_KEY = os.getenv(
        "SECRET_KEY",
        "INFO3180_GROUP_PROJECT_SECRET_KEY"
    )