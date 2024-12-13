import os
import requests
import pandas as pd
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

API_KEY = os.getenv("COINMARKETCAP_API_KEY")
BASE_URL = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest"

def fetch_crypto_data():
    headers = {"X-CMC_PRO_API_KEY": API_KEY}
    params = {"start": 1, "limit": 100, "convert": "USD"}
    response = requests.get(BASE_URL, headers=headers, params=params)

    if response.status_code == 200:
        data = response.json()["data"]
        df = pd.DataFrame([
            {
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "name": item["name"],
                "symbol": item["symbol"],
                "price": item["quote"]["USD"]["price"],
                "volume_24h": item["quote"]["USD"]["volume_24h"],
                "percent_change_1h": item["quote"]["USD"]["percent_change_1h"]
            } for item in data
        ])
        return df
    else:
        print(f"Error: {response.status_code}, {response.json()}")
        return None
