from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

# Load .env file
load_dotenv()

# Get database URL from .env
DATABASE_URL = os.getenv("DATABASE_URL")

# Create engine — this is the connection to your database
engine = create_engine(DATABASE_URL)

# Each request gets its own session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for all your database models
Base = declarative_base()

# Dependency — gives a database session to each endpoint
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()