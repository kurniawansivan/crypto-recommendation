import pandas as pd

def recommend_top_cryptos(file_path, top_n=5):
    # Load cached data
    df = pd.read_csv(file_path)

    # Select the latest data
    latest_data = df.sort_values(by="timestamp", ascending=False).groupby("symbol").first()

    # Filter and sort by volume and price change
    recommendations = latest_data.sort_values(by=["percent_change_1h", "volume_24h"], ascending=False).head(top_n)
    return recommendations[["name", "symbol", "price", "volume_24h", "percent_change_1h"]]
