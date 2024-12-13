import streamlit as st
import pandas as pd
from utils.recommend import recommend_top_cryptos

DATA_FILE = "data/crypto_data.csv"

st.title("Cryptocurrency Recommendation Engine")

# Load recommendations
st.header("Top Recommendations")
recommendations = recommend_top_cryptos(DATA_FILE)
st.table(recommendations)

# Show cached data
st.header("Cached Data")
df = pd.read_csv(DATA_FILE)
st.dataframe(df)
