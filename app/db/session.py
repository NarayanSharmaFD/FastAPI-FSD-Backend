from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import settings
import os

# If using SQLite for local dev we need to pass connect_args
connect_args = {}
if settings.DATABASE_URL.startswith("sqlite"):
    connect_args = {"check_same_thread": False}

engine = create_engine(settings.DATABASE_URL, pool_pre_ping=True, connect_args=connect_args)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Import Base metadata from models
from app.db.base import Base  # noqa: E402
# Import all models to register them with Base
from app.models.models import User, Project, Task, Role  # noqa: F401, E402


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
