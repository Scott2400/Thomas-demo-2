import streamlit as st
import pandas as pd

st.title("Thomas Engine – Skim/Scoop Demo")

uploaded_file = st.file_uploader("Upload your portfolio CSV", type="csv")
cash = st.number_input("Available Cash ($)", min_value=0, value=10000, step=100)
run = st.button("Run Thomas Engine")

if uploaded_file and run:
    df = pd.read_csv(uploaded_file)
    if not all(col in df.columns for col in ["Symbol", "Shares", "CostBasis", "CurrentPrice", "DividendYield"]):
        st.error("Missing required columns.")
    else:
        st.subheader("Thomas Actions")
        for _, row in df.iterrows():
            symbol = row["Symbol"]
            shares = row["Shares"]
            cost_basis = row["CostBasis"]
            price = row["CurrentPrice"]
            gain = (price - cost_basis) / cost_basis if cost_basis else 0

            if price > cost_basis and gain >= 0:
                proceeds = shares * price
                if proceeds >= 10:
                    st.write(f"{symbol}: Skim — Selling {shares} @ ${price:.2f} for ${proceeds:.2f}")
                else:
                    st.write(f"{symbol}: Note — Skim skipped, proceeds ${proceeds:.2f} < $10 minimum")
            elif price < cost_basis and cash >= 10:
                buy_shares = round(10 / price, 2)
                st.write(f"{symbol}: Scoop — Buying {buy_shares} @ ${price:.2f}")
            else:
                st.write(f"{symbol}: No action")