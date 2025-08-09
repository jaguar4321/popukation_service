import os
from app.database import SessionLocal, init_db, engine
from app.models import Country
from app.parser.wikipedia import WikipediaParser

class DataLoader:
    def __init__(self, db_url):
        self.db_url = db_url
        os.environ["DB_URL"] = db_url

    def load_data(self):
        init_db()
        with SessionLocal() as session:
            parser = WikipediaParser()
            data = parser.fetch_data()
            for _, row in data.iterrows():
                country = Country(country=row["country"], population=row["population"], region=row["region"])
                session.add(country)
            session.commit()
        print("✅ Данные сохранены в БД")

if __name__ == "__main__":
    db_url = os.getenv("DB_URL", "postgresql+psycopg2://postgres:postgres@db:5432/population_db")
    loader = DataLoader(db_url)
    loader.load_data()