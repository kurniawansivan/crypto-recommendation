import streamlit as st
from utils.fetch_data import fetch_crypto_data
from utils.recommend import calculate_indicators, train_model, recommend

st.title("Crypto Recommendation Dashboard")
st.write("Dashboard untuk rekomendasi beli, jual, atau tahan (Hold) cryptocurrency.")

# Tombol untuk refresh data
if st.button("Refresh Data"):
    try:
        # Ambil data dan hitung indikator
        data = fetch_crypto_data()
        if data is not None:
            data = calculate_indicators(data)
            model = train_model(data)  # Latih model
            recommendations = recommend(data, model)

            # Tambahkan kolom perubahan harga 24 jam
            recommendations["percent_change_24h"] = data["percent_change_24h"]

            # Tampilkan rekomendasi dalam tabel
            st.subheader("Rekomendasi Cryptocurrency")
            st.table(recommendations[["symbol", "price", "market_cap", "percent_change_24h", "recommendation"]])
        else:
            st.write("Gagal mengambil data cryptocurrency.")
    except Exception as e:
        st.write(f"Error: {e}")
else:
    st.write("Klik tombol di atas untuk mengambil rekomendasi terbaru.")
