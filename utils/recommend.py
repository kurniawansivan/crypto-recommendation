from ta.momentum import RSIIndicator
from ta.volatility import BollingerBands
from ta.trend import MACD, EMAIndicator
from sklearn.ensemble import RandomForestClassifier
import pandas as pd
import numpy as np

def calculate_indicators(data):
    """
    Menghitung indikator teknikal untuk data cryptocurrency.
    """
    data["rsi"] = RSIIndicator(close=data["price"], window=14).rsi()
    bb = BollingerBands(close=data["price"], window=20, window_dev=2)
    data["bb_upper"] = bb.bollinger_hband()
    data["bb_lower"] = bb.bollinger_lband()
    macd = MACD(close=data["price"], window_slow=26, window_fast=12, window_sign=9)
    data["macd"] = macd.macd_diff()
    ema = EMAIndicator(close=data["price"], window=20)
    data["ema"] = ema.ema_indicator()
    return data

def train_model(data):
    """
    Melatih model machine learning untuk menentukan Buy/Sell/Hold.
    """
    # Labelkan data berdasarkan aturan manual (target: Buy, Sell, Hold)
    data["target"] = np.where(
        (data["rsi"] < 30) & (data["price"] < data["bb_lower"]), "BUY",
        np.where((data["rsi"] > 70) & (data["price"] > data["bb_upper"]), "SELL", "HOLD")
    )

    # Fitur dan label
    features = data[["rsi", "bb_upper", "bb_lower", "macd", "ema"]]
    labels = data["target"]

    # Model Random Forest
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(features, labels)
    return model

def recommend(data, model):
    """
    Memberikan rekomendasi berdasarkan model machine learning.
    """
    features = data[["rsi", "bb_upper", "bb_lower", "macd", "ema"]]
    data["recommendation"] = model.predict(features)
    return data[["symbol", "price", "recommendation"]]
