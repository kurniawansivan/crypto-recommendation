import schedule
import time
import os
from utils.fetch_data import fetch_crypto_data
from utils.recommend import calculate_indicators, recommend

# Path untuk file data
DATA_FILE = "data/crypto_data.csv"

def update_data():
    """
    Mengambil data dari API, menghitung indikator, dan menyimpan rekomendasi ke file CSV.
    """
    try:
        print("Fetching new data...")
        df = fetch_crypto_data()
        if df is not None:
            # Hitung indikator teknikal
            df = calculate_indicators(df)
            # Dapatkan rekomendasi
            recommendations = recommend(df)
            print("Recommendations:")
            print(recommendations)

            # Simpan data ke file CSV
            if not os.path.exists(DATA_FILE):
                df.to_csv(DATA_FILE, index=False)
            else:
                df.to_csv(DATA_FILE, mode="a", header=False, index=False)
            print("Data updated successfully!")
        else:
            print("No data fetched. API might be down or empty response.")
    except Exception as e:
        print(f"Error during data update: {e}")

# Jadwal pembaruan data
schedule.every().day.at("07:00").do(update_data)  # Pembaruan pagi
schedule.every().day.at("23:59").do(update_data)  # Pembaruan malam

# Loop penjadwalan
print("Scheduler started. Waiting for tasks...")
while True:
    schedule.run_pending()
    time.sleep(1)
