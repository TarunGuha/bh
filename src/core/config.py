import os
from dotenv import load_dotenv

load_dotenv()

APP_NAME = os.environ.get("APP_NAME", "BH")
APP_ENV = os.environ.get("APP_ENV", "development")
SHOW_DOCS_ENVIRONMENT = [
    "development",
]

if APP_ENV in SHOW_DOCS_ENVIRONMENT:
    APP_CONFIGS = {
        "title": APP_NAME.replace("-", " ").title(),
        "openapi_url": "/openapi.json",
        "docs_url": "/docs",
        "description": "For Track And Trace!",
    }
else:
    APP_CONFIGS = {}

# Database
BH_DATABASE_NAME = os.environ.get("BH_DATABASE_NAME", "")
BH_DATABASE_HOST = os.environ.get("BH_DATABASE_HOST", "")
BH_DATABASE_USER = os.environ.get("BH_DATABASE_USER", "")
BH_DATABASE_PASSWORD = os.environ.get("BH_DATABASE_PASSWORD", "")
BH_DATABASE_PORT = os.environ.get("BH_DATABASE_PORT", "")

BH_DATABASE_URL = f"postgresql://{BH_DATABASE_USER}:{BH_DATABASE_PASSWORD}@{BH_DATABASE_HOST}:{BH_DATABASE_PORT}/{BH_DATABASE_NAME}"


# Credentials
PASSWORD_SALT = os.getenv("PASSWORD_SALT")
