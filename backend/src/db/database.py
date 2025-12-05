from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = "sqlite:///./events.db"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},  # needed for SQLite + FastAPI
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)

Base = declarative_base()

# --- INITIALIZE DB OUTSIDE APP TO RUN TEST SCRIPTS --- #
from . import models # !!!This is needed even tho it says its never used!!!
Base.metadata.create_all(bind=engine)
