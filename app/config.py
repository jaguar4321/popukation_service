import os

DB_URL = os.getenv(
    "DB_URL",
    "postgresql+psycopg2://postgres:jaguar@localhost:5432/population_db"
)
