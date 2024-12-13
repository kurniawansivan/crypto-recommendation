import streamlit as st
from utils.fetch_data import fetch_crypto_data
from utils.recommend import calculate_indicators, recommend

st.title("Cryptocurrency Recommendation Engine")

# Load data
st.subheader("Data Cryptocurrency")
data = fetch_crypto_data()
if data is not None:
    data = calculate_indicators(data)
    st.dataframe(data)

    # Rekomendasi
    st.subheader("Rekomendasi")
    recommendations = recommend(data)
    st.table(recommendations)
else:
    st.error("Gagal mengambil data dari API.")

# Tombol Refresh
if st.button("Refresh Data"):
    st.experimental_rerun()
