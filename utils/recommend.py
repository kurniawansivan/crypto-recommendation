import pandas as pd
from ta.momentum import RSIIndicator
from ta.volatility import BollingerBands

def calculate_indicators(data):
    """
    Menghitung indikator teknikal untuk analisis pergerakan cryptocurrency.
    :param data: DataFrame dengan kolom ['price']
    :return: DataFrame dengan indikator teknikal baru
    """
    # RSI
    data["rsi"] = RSIIndicator(close=data["price"], window=14).rsi()

    # Bollinger Bands
    bb = BollingerBands(close=data["price"], window=20, window_dev=2)
    data["bb_upper"] = bb.bollinger_hband()
    data["bb_lower"] = bb.bollinger_lband()

    return data


def recommend(data):
    """
    Memberikan sinyal rekomendasi beli atau jual berdasarkan indikator teknikal.
    :param data: DataFrame dengan kolom ['price', 'rsi', 'bb_upper', 'bb_lower']
    :return: DataFrame dengan sinyal rekomendasi
    """
    recommendations = []
    for _, row in data.iterrows():
        if row["rsi"] < 30 and row["price"] < row["bb_lower"]:
            recommendations.append({
                "crypto": row["symbol"],
                "signal": "BUY",
                "current_price": row["price"],
                "take_profit": row["price"] * 1.05,  # Target profit 5%
                "stop_loss": row["price"] * 0.95,   # Stop loss 5%
                "reason": "RSI < 30 and price < Bollinger lower band"
            })
        elif row["rsi"] > 70 and row["price"] > row["bb_upper"]:
            recommendations.append({
                "crypto": row["symbol"],
                "signal": "SELL",
                "current_price": row["price"],
                "reason": "RSI > 70 and price > Bollinger upper band"
            })
    return pd.DataFrame(recommendations)
