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
            results = session.query(
                Country.region,
                func.sum(Country.population).label("total_population"),
                func.max(Country.population).label("max_population"),
                func.min(Country.population).label("min_population")
            ).group_by(Country.region).all()

            for region, total_pop, max_pop, min_pop in results:
                max_country = session.query(Country).filter_by(region=region).order_by(
                    Country.population.desc()).first()
                min_country = session.query(Country).filter_by(region=region).order_by(Country.population.asc()).first()
                print(f"Назва регіону: {region}")
                print(f"Загальне населення регіону: {total_pop}")
                print(f"Назва найбільшої країни в регіоні: {max_country.country}")
                print(f"Населення найбільшої країни в регіоні: {max_country.population}")
                print(f"Назва найменшої країни в регіоні: {min_country.country}")
                print(f"Населення найменшої країни в регіоні: {min_country.population}")
                print()

if __name__ == "__main__":
    db_url = os.getenv("DB_URL", "postgresql+psycopg2://postgres:postgres@db:5432/population_db")
    printer = DataPrinter(db_url)
    printer.print_data()