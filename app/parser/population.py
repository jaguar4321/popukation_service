import os
import aiohttp
import pandas as pd
from bs4 import BeautifulSoup
from io import StringIO

class PopulationParser:
    WIKIPEDIA_URL = "https://en.wikipedia.org/w/index.php?title=List_of_countries_by_population_(United_Nations)&oldid=1215058959"
    STATISTICS_TIMES_URL = "https://statisticstimes.com/demographics/countries-by-population.php"

    async def fetch_data(self):
        # source = os.getenv("DATA_SOURCE", "wikipedia").lower()
        source = os.getenv("DATA_SOURCE", "statisticstimes").lower()
        async with aiohttp.ClientSession() as session:
            if source == "statisticstimes":
                return await self._fetch_statisticstimes(session)
            else:
                return await self._fetch_wikipedia(session)

    async def _fetch_wikipedia(self, session):
        async with session.get(self.WIKIPEDIA_URL) as response:
            response.raise_for_status()
            text = await response.text()
            soup = BeautifulSoup(text, "html.parser")
            table = soup.find("table", {"class": "wikitable"})
            df = pd.read_html(StringIO(str(table)))[0]
            return self._clean_wikipedia_data(df)

    async def _fetch_statisticstimes(self, session):
        async with session.get(self.STATISTICS_TIMES_URL) as response:
            response.raise_for_status()
            text = await response.text()
            soup = BeautifulSoup(text, "html.parser")
            table = soup.find("table", {"id": "table_id"})
            df = pd.read_html(StringIO(str(table)))[0]
            return self._clean_statisticstimes_data(df)

    def _clean_wikipedia_data(self, df):
        df = df.iloc[1:].reset_index(drop=True)
        df = df.rename(columns={
            df.columns[0]: "country",
            df.columns[2]: "population",
            df.columns[4]: "region"
        })
        df = df.dropna(subset=["population", "region"])
        df["population"] = df["population"].astype(str).str.replace(",", "").str.extract(r"(\d+)").astype(int)
        return df

    def _clean_statisticstimes_data(self, df):
        print("statisticstimes")

        if isinstance(df.columns, pd.MultiIndex):
            population_2024 = df['Population']['2024']
            country_region = df['Country/Region']['Country/Region']
            continent = df['Continent']['Continent']

            df = pd.DataFrame({
                "country": country_region,
                "population": population_2024,
                "region": continent
            })
        else:
            df = df.rename(columns={
                "Country/Region": "country",
                "Population": "population",
                "Continent": "region"
            })

        df = df[["country", "population", "region"]]

        df = df.dropna(subset=["population", "region"])

        if df["population"].dtype == "object":
            df["population"] = df["population"].astype(str).str.replace(",", "").str.extract(r"(\d+)").astype(int)
        else:
            df["population"] = df["population"].astype(int)

        return df