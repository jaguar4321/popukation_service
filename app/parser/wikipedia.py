# import pandas as pd
# import requests
# from bs4 import BeautifulSoup
# from io import StringIO
#
# class WikipediaParser:
#     URL = "https://en.wikipedia.org/w/index.php?title=List_of_countries_by_population_(United_Nations)&oldid=1215058959"
#
#     def fetch_data(self):
#         r = requests.get(self.URL)
#         r.raise_for_status()
#         soup = BeautifulSoup(r.text, "html.parser")
#         table = soup.find("table", {"class": "wikitable"})
#         df = pd.read_html(StringIO(str(table)))[0]
#         return self.clean_data(df)
#
#     def clean_data(self, df):
#         df = df.rename(columns={df.columns[0]: "country", df.columns[1]: "population"})
#
#         # Убираем пустые строки
#         df = df.dropna(subset=["population"])
#
#         # Оставляем только те строки, где население — число
#         df["population"] = (
#             df["population"]
#             .astype(str)
#             .str.replace(",", "")
#             .str.replace(".0", "", regex=False)
#             .str.extract(r"(\d+)")
#         )
#
#         # Убираем строки, где не удалось извлечь число
#         df = df.dropna(subset=["population"])
#
#         # Приводим к int
#         df["population"] = df["population"].astype(int)
#
#         return df


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
        # Пропускаем первую строку (World)
        df = df.iloc[1:].reset_index(drop=True)
        # Переименовываем колонки: Location -> country, Population (1 July 2023) -> population, UN Statistical Subregion -> region
        df = df.rename(columns={
            df.columns[0]: "country",
            df.columns[2]: "population",  # Используем данные за 2023 год
            df.columns[5]: "region"       # UN Statistical Subregion
        })
        # Удаляем строки с пропущенными значениями
        df = df.dropna(subset=["population", "region"])
        # Очищаем население (убираем запятые и приводим к int)
        df["population"] = df["population"].astype(str).str.replace(",", "").str.extract(r"(\d+)").astype(int)
        return df