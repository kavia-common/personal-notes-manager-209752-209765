import os
from datetime import timedelta


class Config:
    """Base configuration for the Flask app."""
    # API Docs configuration (flask-smorest)
    API_TITLE = "Personal Notes Manager API"
    API_VERSION = "v1"
    OPENAPI_VERSION = "3.0.3"
    OPENAPI_URL_PREFIX = "/docs"
    OPENAPI_SWAGGER_UI_PATH = ""
    OPENAPI_SWAGGER_UI_URL = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"

    # Security and JWT
    SECRET_KEY = os.getenv("FLASK_SECRET_KEY", "dev-secret-change-me")  # replace in production via .env
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "dev-jwt-secret-change-me")  # replace in production via .env
    JWT_TOKEN_LOCATION = ["headers"]
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=12)

    # Database
    BASE_DIR = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
    DB_PATH = os.getenv("DATABASE_URL", f"sqlite:///{os.path.join(BASE_DIR, 'app.db')}")
    SQLALCHEMY_DATABASE_URI = DB_PATH
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # CORS
    CORS_ORIGINS = os.getenv("CORS_ORIGINS", "*")
