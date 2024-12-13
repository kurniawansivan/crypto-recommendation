import schedule
import time
import os
from utils.fetch_data import fetch_crypto_data

# Path untuk file data
DATA_FILE = "data/crypto_data.csv"

# Fungsi untuk memperbarui data
def update_data():
    try:
        print("Fetching new data...")
        df = fetch_crypto_data()  # Mengambil data dari API
        if df is not None:
            # Menyimpan data ke CSV (append mode)
            df.to_csv(DATA_FILE, mode="a", header=not os.path.exists(DATA_FILE), index=False)
            print("Data updated successfully!")
        else:
            print("No data fetched. API might be down or empty response.")
    except Exception as e:
        print(f"Error during data update: {e}")

# Jadwal pembaruan data
schedule.every().day.at("07:00").do(update_data)  # Mulai pembaruan pukul 07:00
schedule.every().day.at("23:59").do(update_data)  # Pembaruan terakhir pukul 23:59

# Loop untuk menjalankan penjadwalan
print("Scheduler started. Waiting for tasks...")
while True:
    schedule.run_pending()
    time.sleep(1)  # Tunggu 1 detik sebelum cek tugas berikutnya
