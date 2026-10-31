
import os
from pathlib import Path

from dotenv import load_dotenv
from sqlalchemy import create_engine, text

# Load database details from backend/.env
env_path = Path(__file__).resolve().parent / ".env"
load_dotenv(env_path)

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    print("Database URL not found in .env")
else:
    try:
        engine = create_engine(DATABASE_URL)

        with engine.connect() as connection:
            result = connection.execute(text("SELECT 1"))
            print("Database connection successful!")
            print("Test result:", result.scalar())

    except Exception as error:
        print("Database connection failed!")
        print("Error:", error)
