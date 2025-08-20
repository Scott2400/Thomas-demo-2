import streamlit as st
import pandas as pd

st.title("Thomas Portfolio Builder")

st.write("Answer a few questions and we'll generate a starter portfolio designed for skim/scoop logic.")

age = st.slider("How old are you?", 18, 80, 45)
income_focus = st.selectbox("Primary goal?", ["Maximize income", "Balanced", "Long-term growth"])
risk = st.selectbox("Risk tolerance?", ["Low", "Medium", "High"])
monthly_cash_goal = st.number_input("Monthly Cash Flow Goal ($)", value=500)

run = st.button("Build Portfolio")

if run:
    allocations = []
    if income_focus == "Maximize income":
        allocations = [
            {"Symbol": "PDI", "Shares": 200, "CostBasis": 19.50, "CurrentPrice": 19.50, "DividendYield": 0.145},
            {"Symbol": "AGNC", "Shares": 150, "CostBasis": 10.00, "CurrentPrice": 10.00, "DividendYield": 0.14},
            {"Symbol": "JEPQ", "Shares": 100, "CostBasis": 55.00, "CurrentPrice": 55.00, "DividendYield": 0.11},
        ]
    elif income_focus == "Balanced":
        allocations = [
            {"Symbol": "JEPQ", "Shares": 100, "CostBasis": 55.00, "CurrentPrice": 55.00, "DividendYield": 0.11},
            {"Symbol": "VYM", "Shares": 80, "CostBasis": 105.00, "CurrentPrice": 105.00, "DividendYield": 0.035},
            {"Symbol": "O", "Shares": 50, "CostBasis": 60.00, "CurrentPrice": 60.00, "DividendYield": 0.06},
        ]
    else:  # Long-term growth
        allocations = [
            {"Symbol": "VTI", "Shares": 60, "CostBasis": 240.00, "CurrentPrice": 240.00, "DividendYield": 0.015},
            {"Symbol": "SCHD", "Shares": 75, "CostBasis": 72.00, "CurrentPrice": 72.00, "DividendYield": 0.038},
            {"Symbol": "JEPQ", "Shares": 40, "CostBasis": 55.00, "CurrentPrice": 55.00, "DividendYield": 0.11},
        ]
    df = pd.DataFrame(allocations)
    st.write("### Suggested Portfolio")
    st.dataframe(df)
    st.download_button("Download Portfolio CSV", df.to_csv(index=False), file_name="portfolio.csv")