import streamlit as st
import pandas as pd

st.set_page_config(page_title="Thomas – What Can I Do for You?", layout="centered")
st.title("🧠 Thomas – What Can I Do for You Today?")

option = st.radio("Choose an option:", [
    "🔵 I already have a portfolio",
    "🟢 Help me build one",
    "🟠 I'm curious about a specific stock"
])

if option == "🔵 I already have a portfolio":
    st.subheader("Tell me what you own")
    rows = st.number_input("How many different holdings do you want to enter?", min_value=1, max_value=10, value=3)
    portfolio = []

    for i in range(int(rows)):
        st.markdown("---")
        st.markdown(f"**Asset {i+1}**")
        symbol = st.text_input(f"Ticker {i+1}", key=f"sym_{i}")
        shares = st.number_input(f"Shares {i+1}", key=f"sh_{i}", min_value=0.0)
        cost = st.number_input(f"Avg cost basis {i+1} (optional)", key=f"cb_{i}", value=0.0)
        price = st.number_input(f"Current price {i+1} (optional)", key=f"cp_{i}", value=0.0)
        if symbol and shares:
            portfolio.append({
                "Symbol": symbol.upper(),
                "Shares": shares,
                "CostBasis": cost,
                "CurrentPrice": price
            })

    if st.button("Estimate My Income"):
        st.markdown("### 💰 Projected Results")
        for asset in portfolio:
            symbol = asset["Symbol"]
            sh = asset["Shares"]
            cb = asset["CostBasis"]
            cp = asset["CurrentPrice"]
            if cb and cp:
                gain = (cp - cb) / cb if cb else 0
                if cp > cb:
                    proceeds = sh * cp
                    st.write(f"{symbol}: Estimated Skim – ${proceeds:,.2f}")
                elif cp < cb:
                    scoop_qty = round(10 / cp, 2) if cp else 0
                    st.write(f"{symbol}: Scoop Opportunity – Buy ~{scoop_qty} more @ ${cp:.2f}")
            else:
                st.write(f"{symbol}: Based on holdings, Thomas can likely generate monthly income with this asset.")

elif option == "🟢 Help me build one":
    st.subheader("Let’s design your starter portfolio")
    amount = st.number_input("How much money do you want to invest?", min_value=1000, step=500)
    goal = st.selectbox("Primary goal", ["Monthly income", "Some growth + some income", "Long-term capital growth"])

    if st.button("Build My Portfolio"):
        st.markdown("### 🧱 Starter Portfolio")
        if goal == "Monthly income":
            data = [
                {"Symbol": "JEPQ", "Allocation": 0.5, "EstYield": 0.11},
                {"Symbol": "PDI", "Allocation": 0.3, "EstYield": 0.14},
                {"Symbol": "AGNC", "Allocation": 0.2, "EstYield": 0.13}
            ]
        elif goal == "Some growth + some income":
            data = [
                {"Symbol": "SCHD", "Allocation": 0.4, "EstYield": 0.035},
                {"Symbol": "JEPQ", "Allocation": 0.3, "EstYield": 0.11},
                {"Symbol": "VYM", "Allocation": 0.3, "EstYield": 0.038}
            ]
        else:
            data = [
                {"Symbol": "VTI", "Allocation": 0.5, "EstYield": 0.015},
                {"Symbol": "SCHD", "Allocation": 0.3, "EstYield": 0.035},
                {"Symbol": "JEPQ", "Allocation": 0.2, "EstYield": 0.11}
            ]
        total_income = 0
        for item in data:
            dollars = amount * item["Allocation"]
            income = dollars * item["EstYield"]
            total_income += income
            st.write(f"{item['Symbol']}: Invest ${dollars:,.0f}, Est. income: ${income:,.0f}/yr")
        st.markdown(f"**💵 Estimated Total Income: ${total_income:,.0f} / year**")

elif option == "🟠 I'm curious about a specific stock":
    st.subheader("Enter a stock you're curious about")
    symbol = st.text_input("Stock ticker")
    if symbol:
        sym = symbol.upper()
        st.markdown(f"### 🔍 TomScore for {sym}")
        if sym in ["PDI", "JEPQ", "AGNC"]:
            st.success("5 – High Confidence Income Producer")
            st.write("This asset is ideal for frequent skimming and can reliably support income generation.")
        elif sym in ["SCHD", "VYM", "O"]:
            st.info("4 – Reliable Dividend Asset")
            st.write("A stable choice that contributes consistent yield, though less aggressive.")
        elif sym == "VTI":
            st.warning("3 – Growth-Focused")
            st.write("More suitable for long-term holding than monthly income.")
        else:
            st.error("1 – Not optimized for Skim/Scoop")
            st.write("This asset may not support reliable income through Thomas.")