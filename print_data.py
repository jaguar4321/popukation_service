import os
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models import Country
from sqlalchemy import func

class DataPrinter:
    def __init__(self, db_url):
        self.db_url = db_url
        os.environ["DB_URL"] = db_url

    def print_data(self):
        with SessionLocal() as session:
            # Агрегатний SQL-запрос
            result = session.query(
                func.sum(Country.population).label("total_population"),
                func.max(Country.population).label("max_population"),
                func.min(Country.population).label("min_population")
            ).one()

            # Отримання назв країн з максимальним і мінімальним населенням
            max_country = session.query(Country).order_by(Country.population.desc()).first()
            min_country = session.query(Country).order_by(Country.population.asc()).first()

            print(f"Назва регіону")
            print(f"Загальне населення регіону: {result.total_population}")
            print(f"Назва найбільшої країни в регіоні (за населенням): {max_country.country}")
            print(f"Населення найбільшої країни в регіоні: {max_country.population}")
            print(f"Назва найменшої країни в регіоні: {min_country.country}")
            print(f"Населення найменшої країни в регіоні: {min_country.population}")

if __name__ == "__main__":
    db_url = os.getenv("DB_URL", "postgresql+psycopg2://postgres:jaguar@db:5432/population_db")
    printer = DataPrinter(db_url)
    printer.print_data()