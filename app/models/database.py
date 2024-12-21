from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.exc import SQLAlchemyError
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Database URL
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./bookmarks.db")

# Create a database engine
# `check_same_thread` is set to False for SQLite to allow multi-threaded access
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}
)

# Create a SessionLocal class for session management
SessionLocal = sessionmaker(
    autocommit=False,  # Changes won't be committed automatically
    autoflush=False,   # Prevent auto-flushing pending changes
    bind=engine        # Bind the session to our database engine
)

# Base class for creating models
Base = declarative_base()

# Dependency for getting a database session
def get_db():
    """
    Dependency to get a SQLAlchemy database session.
    Ensures the session is closed after use.
    """
    db = SessionLocal()
    try:
        yield db
    except SQLAlchemyError as e:
        print(f"Database Error: {e}")
        db.rollback()
    finally:
        db.close()
