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
        df = df.rename(columns={df.columns[0]: "country", df.columns[1]: "population"})

        # Убираем пустые строки
        df = df.dropna(subset=["population"])

        # Оставляем только те строки, где население — число
        df["population"] = (
            df["population"]
            .astype(str)
            .str.replace(",", "")
            .str.replace(".0", "", regex=False)
            .str.extract(r"(\d+)")
        )

        # Убираем строки, где не удалось извлечь число
        df = df.dropna(subset=["population"])

        # Приводим к int
        df["population"] = df["population"].astype(int)

        return df
