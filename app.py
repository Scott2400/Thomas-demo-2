import streamlit as st
import pandas as pd

st.set_page_config(page_title="Thomas App", layout="centered")

st.sidebar.title("What do you want Thomas to help you with?")
page = st.sidebar.radio("Choose a page", [
    "🔵 I already have a portfolio",
    "🟢 Help me build one",
    "🟠 I'm curious about a specific stock",
    "📋 Summary"
])

if page == "🟢 Help me build one":
    st.title("🟢 Help Me Build a Portfolio")
    total_amount = st.number_input("How much money do you have available to invest right now?", min_value=0, step=1000)
    account_type = st.radio("What type of account will you be using?", ["Regular taxable account", "Qualified retirement account", "Both"])
    monthly_income_goal = st.number_input("How much additional monthly income would you like to generate?", min_value=0, step=100)

    if total_amount > 0 and monthly_income_goal > 0:
        st.markdown("---")
        st.subheader("📊 Suggested Starter Portfolio")
        if total_amount < 250_000:
            portfolio = [
                {"Symbol": "JEPQ", "Allocation": 0.5, "EstYield": 0.11},
                {"Symbol": "PDI", "Allocation": 0.3, "EstYield": 0.14},
                {"Symbol": "AGNC", "Allocation": 0.2, "EstYield": 0.13}
            ]
        elif total_amount < 750_000:
            portfolio = [
                {"Symbol": "JEPQ", "Allocation": 0.3, "EstYield": 0.11},
                {"Symbol": "PDI", "Allocation": 0.25, "EstYield": 0.14},
                {"Symbol": "AGNC", "Allocation": 0.2, "EstYield": 0.13},
                {"Symbol": "SCHD", "Allocation": 0.15, "EstYield": 0.035},
                {"Symbol": "VYM", "Allocation": 0.1, "EstYield": 0.038}
            ]
        else:
            portfolio = [
                {"Symbol": "JEPQ", "Allocation": 0.2, "EstYield": 0.11},
                {"Symbol": "PDI", "Allocation": 0.15, "EstYield": 0.14},
                {"Symbol": "AGNC", "Allocation": 0.1, "EstYield": 0.13},
                {"Symbol": "SCHD", "Allocation": 0.2, "EstYield": 0.035},
                {"Symbol": "VYM", "Allocation": 0.15, "EstYield": 0.038},
                {"Symbol": "O", "Allocation": 0.1, "EstYield": 0.06},
                {"Symbol": "VTI", "Allocation": 0.1, "EstYield": 0.015}
            ]

        total_annual_income = 0
        for asset in portfolio:
            dollars = total_amount * asset["Allocation"]
            income = dollars * asset["EstYield"]
            total_annual_income += income
            st.write(f"{asset['Symbol']}: Invest ${dollars:,.0f}, Est. income: ${income:,.0f}/yr")

        total_monthly = total_annual_income / 12
        st.markdown(f"### 💵 Estimated Monthly Income: **${total_monthly:,.0f}**")

        if total_monthly < monthly_income_goal:
            shortfall = monthly_income_goal - total_monthly
            st.error(f"You're projected to generate ${total_monthly:,.0f}/mo — that's ${shortfall:,.0f} below your target of ${monthly_income_goal:,.0f}/mo.")
            st.markdown("Thomas can help you explore ways to close this gap by adjusting expectations, reallocating funds, or increasing your investable assets.")
        elif total_monthly > monthly_income_goal:
            surplus = total_monthly - monthly_income_goal
            st.success(f"You're projected to generate ${total_monthly:,.0f}/mo — that's ${surplus:,.0f} above your target!")
        else:
            st.info("Your portfolio is projected to hit your monthly income goal exactly.")
    else:
        st.info("Please enter both your total investable amount and your income goal to continue.")

elif page == "🔵 I already have a portfolio":
    st.title("🔵 I Already Have a Portfolio")
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

elif page == "🟠 I'm curious about a specific stock":
    st.title("🟠 I'm Curious About a Stock")
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

elif page == "📋 Summary":
    st.title("📋 Summary")
    st.markdown("You’ve now seen how Thomas can:")
    st.markdown("- Build a portfolio from scratch")
    st.markdown("- Estimate income from your existing holdings")
    st.markdown("- Evaluate any ticker with the TomScore")
    st.markdown("More features coming soon!")