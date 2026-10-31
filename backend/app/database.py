
import os
from pathlib import Path

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# Load environment variables
env_path = Path(__file__).resolve().parents[1] / ".env"
load_dotenv(env_path)

DATABASE_URL = os.getenv("DATABASE_URL")

# Connect to PostgreSQL
engine = create_engine(DATABASE_URL)

# Create database sessions
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# Base class for database tables
Base = declarative_base()
