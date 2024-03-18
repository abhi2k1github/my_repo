import os
from dotenv import load_dotenv

load_dotenv()

# ENV
APP_ENV = os.getenv("APP_ENV")

# Main DB connection
DATABASE_NAME = os.getenv("DATABASE_NAME")
DATABASE_USER = os.getenv("DATABASE_USER")
DATABASE_PASSWORD = os.getenv("DATABASE_PASSWORD")
DATABASE_HOST = os.getenv("DATABASE_HOST")
DATABASE_PORT = os.getenv("DATABASE_PORT")
ENVIRONMENT_TYPE = os.getenv("ENVIRONMENT_TYPE")