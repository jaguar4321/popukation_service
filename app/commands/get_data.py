from app.database import SessionLocal, init_db
from app.models import Country
from app.parser.wikipedia import WikipediaParser

def main():
    init_db()
    session = SessionLocal()

    parser = WikipediaParser()
    data = parser.fetch_data()

    for _, row in data.iterrows():
        country = Country(country=row["country"], population=row["population"])
        session.add(country)

    session.commit()
    session.close()
    print("✅ Данные сохранены в БД")

if __name__ == "__main__":
    main()
