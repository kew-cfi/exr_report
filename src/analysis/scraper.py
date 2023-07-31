import io
import requests
import pandas as pd
import datetime as dt
from typing import List, Any

from src.config import Config


class Logger():
    info = print
    error = print
    warning = print
    debug = print


class Scraper(Config):
    def __init__(self, country=["*"], logger=Logger()):
        if country == ["*"]:
            self.country = self.ANALYSIS_CONFIG["COUNTRY_LIST"]
        else:
            self.country = country
        self.logger = logger
    

    def main(self) -> pd.DataFrame:
        """Main function to retrieve exchange rate data from ECB API.

        Returns:
            pd.DataFrame: final output of exchange rate data in pandas dataframe
        """
        df = pd.DataFrame()
        for country in self.country:
            try:
                print(f"  fetching data for country: {country}...")
                url = f"https://data-api.ecb.europa.eu/service/data/EXR/D.{country}.EUR.SP00.A"
                temp_df = self.get_ecb_dataframe(url=url)
                df = pd.concat([df, temp_df])
            except:
                print(f"  fail to fetch data for country: {country}...")

        df = df.reset_index(drop=True)
        
        return df


    def get_ecb_dataframe(self,url:str) -> pd.DataFrame:
        """Convert retrieved data from ECB API to pandas dataframe.

        Args:
            url (str): API url of exchange rate of each currencies to the Eur from ECB website

        Returns:
            pd.DataFrame: data of exchange rate of each currencies to the Euro in pandas dataframe
        """
        data = self._get_ecb_url(url)

        if data is not None:
            df = pd.read_csv(io.StringIO(data.text), parse_dates=["TIME_PERIOD"]) # , index_col="TIME_PERIOD"
            df = df[df["TIME_PERIOD"]==df["TIME_PERIOD"].max()][self.vars(types=["EXR"], wc_vars=df.columns, qreturn_dict=False)]
            return df
        else:
            return None


    def _get_ecb_url(self, url:str) -> str:
        """Based on ECB provided API, retrive data on the exchange rate of each currencies to the Euro.

        Currencies countries are defined in Config class. Start and end period of data to be retrieved
        are also defined in Config class. If start period is not defined, there will be no value to be retrieved
        from start period but jus end period.

        Args:
            url (str): API url of exchange rate of each currencies to the Eur from ECB website

        Returns:
            str: data of exchange rate of each currencies to the Euro in text form
        """
        parameters = {
            "startPeriod": self.ANALYSIS_CONFIG["START_DATE"],
            "endPeriod": self.ANALYSIS_CONFIG["END_DATE"]
        }
        response = requests.get(url)
        if response.status_code == 200:
            data = requests.get(url, params=parameters, headers={"Accept": "text/csv"})
            return data
        else:
            print(f"Failed to fetch data. Status code: {response.status_code}")
            return None
        