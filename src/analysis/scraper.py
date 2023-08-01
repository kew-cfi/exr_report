import io
import os
import requests
import pandas as pd
import datetime as dt
from typing import List, Any, Dict

from src.config import Config
    

def main(start_period: Any, 
         end_period: str, 
         country: List[str]) -> pd.DataFrame:
    """Main function to retrieve exchange rate data from ECB API.

    Returns:
        pd.DataFrame: final output of exchange rate data in pandas dataframe
    """
    parameters = {
        "startPeriod": start_period,
        "endPeriod": end_period
    }

    df = pd.DataFrame()
    for country in country:
        try:
            print(f"  fetching data for country: {country}...")
            url = f"https://data-api.ecb.europa.eu/service/data/EXR/D.{country}.EUR.SP00.A"
            temp_df = get_ecb_dataframe(url=url, param_grid=parameters)
            df = pd.concat([df, temp_df])
        except:
            print(f"  fail to fetch data for country: {country}...")

    df = df.rename(columns=Config._RENAME_COLUMNS["EXR"])
    df["ID"] = range(1, (len(df)+1))
    df = df.reset_index(drop=True)

    df = assert_exr_columns_and_sort(df)

    if Config.QDEBUG:
        fname = os.path.join(Config.FILES["PREPROCESS_DATA"], "ecb_exchange_rate_{}.csv".format(end_period))
        df.to_csv(fname, index=False)
    
    return df


def get_ecb_dataframe(url: str, 
                      param_grid: Dict[str, Any]) -> pd.DataFrame:
    """Based on ECB provided API, retrive data on the exchange rate of each currencies to the Euro.
    Convert retrieved data from ECB API to pandas dataframe.

    'param_grid' controls the start and end period of data to be retrieved. If start period is not defined, 
    there will be no value to be retrieved from start period but jus end period.

    Args:
        url (str): API url of exchange rate of each currencies to the Eur from ECB website
        param_grid (Dict[str:Any]): Dictionary of to define how the data to be extracted from API, for now only start and end period

    Returns:
        pd.DataFrame: data of exchange rate of each currencies to the Euro in pandas dataframe
    """
    response = requests.get(url)
    if response.status_code == 200:
        data = requests.get(url, params=param_grid, headers={"Accept": "text/csv"})
    else:
        print(f"Failed to fetch data. Status code: {response.status_code}")
        data = None

    if data is not None:
        df = pd.read_csv(io.StringIO(data.text), parse_dates=["TIME_PERIOD"])
        df = df[df["TIME_PERIOD"]==df["TIME_PERIOD"].max()][Config.vars(types=["EXR"], wc_vars=df.columns, qreturn_dict=False)]
        df["MODIFIED_DATE"] = dt.date.today().strftime("%Y-%m-%d")
        df["SOURCE"] = "ECB"
        return df
    else:
        return None
    

def assert_exr_columns_and_sort(df):
    sort_columns = ["ID", "SOURCE", "ORIGIN_CURRENCY", "TARGET_CURRENCY", "EXCHANGE_RATE", "REPORT_DATE", "MODIFIED_DATE"]

    if all(col in df.columns for col in sort_columns):
        df = df[sort_columns]
    else:
        raise ValueError("Columns in dataframe is not as expected.")

    return df