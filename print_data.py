import os
import asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import func, select
from app.database import AsyncSessionLocal
from app.models import Country

class DataPrinter:
    def __init__(self, db_url):
        self.db_url = db_url
        os.environ["DB_URL"] = db_url

    async def print_data(self):
        async with AsyncSessionLocal() as session:
            stmt = (
                select(
                    Country.region,
                    func.sum(Country.population).label("total_population"),
                    func.max(Country.population).label("max_population"),
                    func.min(Country.population).label("min_population")
                )
                .group_by(Country.region)
            )
            results = (await session.execute(stmt)).all()

            for region, total_pop, max_pop, min_pop in results:
                max_stmt = (
                    select(Country)
                    .filter_by(region=region)
                    .order_by(Country.population.desc())
                )
                max_country = (await session.execute(max_stmt)).scalars().first()

                min_stmt = (
                    select(Country)
                    .filter_by(region=region)
                    .order_by(Country.population.asc())
                )
                min_country = (await session.execute(min_stmt)).scalars().first()

                print(f"Назва регіону: {region}")
                print(f"Загальне населення регіону: {total_pop}")
                print(f"Назва найбільшої країни в регіоні: {max_country.country}")
                print(f"Населення найбільшої країни в регіоні: {max_country.population}")
                print(f"Назва найменшої країни в регіоні: {min_country.country}")
                print(f"Населення найменшої країни в регіоні: {min_country.population}")
                print()

async def main():
    db_url = os.getenv("DB_URL", "postgresql+asyncpg://postgres:postgres@localhost:5432/population_db")
    printer = DataPrinter(db_url)
    await printer.print_data()

if __name__ == "__main__":
    asyncio.run(main())