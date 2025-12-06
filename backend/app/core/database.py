"""
Database Connection and Session Management

This module sets up SQLAlchemy for database operations.

Educational Notes:
- SQLAlchemy is an ORM (Object-Relational Mapper) that lets you work with
  database tables as Python objects
- Session management is crucial for proper transaction handling
- Using a context manager pattern ensures connections are properly closed
"""

from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session, sessionmaker

from app.core.config import settings

# Create database engine
# The engine manages the connection pool to the database
engine = create_engine(
    str(settings.DATABASE_URL),
    pool_pre_ping=True,  # Verify connections before using them
    echo=settings.DEBUG,  # Log SQL queries when debugging
)

# SessionLocal is a factory for creating database sessions
# A session represents a "workspace" for database operations
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for all database models
# All models will inherit from this
Base = declarative_base()


def get_db() -> Generator[Session, None, None]:
    """
    Dependency function that provides a database session.

    This is used with FastAPI's dependency injection system.
    The session is automatically closed when the request completes.

    Usage in FastAPI endpoints:
        @app.get("/items")
        def read_items(db: Session = Depends(get_db)):
            return db.query(Item).all()
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
