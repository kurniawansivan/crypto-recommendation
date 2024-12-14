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
                "price": round(coin["quote"]["USD"]["price"], 8),  # Presisi hingga 8 digit
                "market_cap": coin["quote"]["USD"]["market_cap"],
                "percent_change_24h": coin["quote"]["USD"]["percent_change_24h"]  # Perubahan harga 24 jam dalam persen
            }
            for coin in data
        ])

        # Urutkan berdasarkan market cap
        df = df.sort_values(by="market_cap", ascending=False).reset_index(drop=True)
        return df
    except Exception as e:
        print(f"Error fetching data: {e}")
        return None
