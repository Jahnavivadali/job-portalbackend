import os
from dotenv import load_dotenv
from secrets_manager import get_database_credentials

load_dotenv(os.path.join(os.path.dirname(__file__), ".env"))


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "jobportal-secret-key")
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "jobportal-jwt-secret")

    try:
        db_credentials = get_database_credentials()

        SQLALCHEMY_DATABASE_URI = (
            f"mysql+pymysql://{db_credentials['username']}:"
            f"{db_credentials['password']}@"
            f"{db_credentials['host']}:"
            f"{db_credentials['port']}/"
            f"{db_credentials.get('dbname', '')}"
        )

    except Exception:
        SQLALCHEMY_DATABASE_URI = os.getenv(
            "DATABASE_URL",
            "sqlite:///jobportal.db",
        )

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    UPLOAD_FOLDER = os.path.join(
        os.path.dirname(__file__),
        "uploads",
        "resumes"
    )

    CORS_ORIGINS = [
        origin.strip()
        for origin in os.getenv(
            "CORS_ORIGINS",
            "http://localhost:5173,http://127.0.0.1:5173,"
            "http://localhost:5174,http://127.0.0.1:5174,"
            "http://localhost:3000,http://127.0.0.1:3000,"
            "http://localhost:3001,http://127.0.0.1:3001",
        ).split(",")
        if origin.strip()
    ]
