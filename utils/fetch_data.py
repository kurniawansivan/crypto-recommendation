import requests
import pandas as pd
import os

# API CoinMarketCap
API_URL = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest"
API_KEY = os.getenv("CMC_API_KEY")  # API Key diambil dari .env

def fetch_crypto_data():
    """
    Mengambil data cryptocurrency dari API CoinMarketCap.
    """
    headers = {
        "Accepts": "application/json",
        "X-CMC_PRO_API_KEY": API_KEY,
    }

    try:
        response = requests.get(API_URL, headers=headers, params={"limit": 100})
        data = response.json()["data"]

        # Konversi data ke DataFrame
        df = pd.DataFrame([
            {
                "symbol": coin["symbol"],
                "name": coin["name"],
                "price": coin["quote"]["USD"]["price"],
                "volume_24h": coin["quote"]["USD"]["volume_24h"],
                "market_cap": coin["quote"]["USD"]["market_cap"]
            }
            for coin in data
        ])
        return df
    except Exception as e:
        print(f"Error fetching data: {e}")
        return None
