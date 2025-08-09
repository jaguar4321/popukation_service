import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

Base = declarative_base()

def get_engine():
    db_url = os.getenv(
        "DB_URL",
        # "postgresql+psycopg2://postgres:jaguar@localhost:5432/population_db"
    )
    return create_engine(db_url)

engine = get_engine()
SessionLocal = sessionmaker(bind=engine)

def init_db():
    Base.metadata.create_all(engine)
