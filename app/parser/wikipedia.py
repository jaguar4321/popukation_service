import pandas as pd
import requests
from bs4 import BeautifulSoup
from io import StringIO

class WikipediaParser:
    URL = "https://en.wikipedia.org/w/index.php?title=List_of_countries_by_population_(United_Nations)&oldid=1215058959"

    def fetch_data(self):
        r = requests.get(self.URL)
        r.raise_for_status()
        soup = BeautifulSoup(r.text, "html.parser")
        table = soup.find("table", {"class": "wikitable"})
        df = pd.read_html(StringIO(str(table)))[0]
        return self.clean_data(df)

    def clean_data(self, df):
        df = df.iloc[1:].reset_index(drop=True)
        df = df.rename(columns={
            df.columns[0]: "country",
            df.columns[2]: "population",
            df.columns[4]: "region"
        })
        df = df.dropna(subset=["population", "region"])
        df["population"] = df["population"].astype(str).str.replace(",", "").str.extract(r"(\d+)").astype(int)
        return df