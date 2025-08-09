import os
import asyncio
from app.database import AsyncSessionLocal, init_db
from app.models import Country
from app.parser.population import PopulationParser

class DataLoader:
    async def load_data(self):
        await init_db()
        async with AsyncSessionLocal() as session:
            async with session.begin():
                parser = PopulationParser()
                data = await parser.fetch_data()
                for _, row in data.iterrows():
                    country = Country(
                        country=row["country"],
                        population=row["population"],
                        region=row["region"]
                    )
                    session.add(country)
                await session.commit()
            print("✅ The data is saved in the database")

async def main():
    loader = DataLoader()
    await loader.load_data()

if __name__ == "__main__":
    asyncio.run(main())