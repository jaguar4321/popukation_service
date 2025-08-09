import os
from app.database import SessionLocal, init_db
from app.models import Country
from app.parser.wikipedia import WikipediaParser

class DataLoader:
    def load_data(self):
        init_db()
        with SessionLocal() as session:
            parser = WikipediaParser()
            data = parser.fetch_data()
            for _, row in data.iterrows():
                country = Country(
                    country=row["country"],
                    population=row["population"],
                    region=row["region"]
                )
                session.add(country)
            session.commit()
        print("✅ The data is saved in the database")

if __name__ == "__main__":
    loader = DataLoader()
    loader.load_data()
