from fastapi import FastAPI
import time
from utils.fetch_data import fetch_crypto_data
from utils.recommend import calculate_indicators, recommend

# Inisialisasi FastAPI
app = FastAPI()

# File data
DATA_FILE = "data/crypto_data.csv"

@app.get("/")
def home():
    return {"message": "Crypto Recommendation Engine is running 24/7!"}

@app.get("/recommendations")
def get_recommendations():
    """
    Endpoint untuk mendapatkan rekomendasi cryptocurrency.
    """
    data = fetch_crypto_data()
    if data is not None:
        data = calculate_indicators(data)
        recommendations = recommend(data)
        return recommendations.to_dict(orient="records")
    return {"error": "Failed to fetch data"}

# Fungsi untuk loop 24/7
def continuous_update():
    """
    Fungsi yang berjalan 24/7 untuk memperbarui data dan memberikan rekomendasi.
    """
    while True:
        print("Fetching and updating data...")
        data = fetch_crypto_data()
        if data is not None:
            data = calculate_indicators(data)
            recommendations = recommend(data)
            print("Updated Recommendations:")
            print(recommendations)
        else:
            print("Failed to fetch data. Retrying in 10 seconds...")
        time.sleep(10)  # Tunggu 10 detik sebelum mencoba lagi

# Jalankan aplikasi FastAPI
if __name__ == "__main__":
    import threading
    import os
    import uvicorn

    # Jalankan loop pembaruan data di thread terpisah
    update_thread = threading.Thread(target=continuous_update, daemon=True)
    update_thread.start()

    # Jalankan server FastAPI
    port = int(os.environ.get("PORT", 8000))  # Railway mendukung variabel PORT otomatis
    uvicorn.run(app, host="0.0.0.0", port=port)
