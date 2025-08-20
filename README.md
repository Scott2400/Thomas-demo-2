# Thomas Engine – GitHub Version

This is a GitHub-deployable demo of the Thomas Skim/Scoop logic engine.

## 🧾 Instructions

1. Upload a `.csv` with the following columns:
   - `Symbol`, `Shares`, `CostBasis`, `CurrentPrice`, `DividendYield`

2. Enter available cash (e.g. 10000)

3. Click **Run Thomas Engine** to see suggested skims/scoops.

## 🔧 Setup locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

## ✅ Skim Logic

- Skim if price > cost basis and gain ≥ 0%
- Skip if proceeds < $10

## ✅ Scoop Logic

- Scoop if price < cost basis and you have at least $10 cash
- Always buy $10 worth