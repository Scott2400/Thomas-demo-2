# Thomas Phase 1 – Cash Flow Engine (CLI)

This is a simulation-only command-line engine for the Thomas investment cash flow strategy. It reads a portfolio from CSV, applies Skim/Scoop logic, and outputs human-readable and machine-readable logs.

## 📦 Features

- **Skim** when gains ≥ 0% and price > cost basis
- **Scoop** when price < cost basis and cash is available
- **Minimum skim proceeds**: $10 (smaller skims are skipped with a note)
- Guardrails: No brokerage integrations, no external dependencies

## 🛠 Requirements

- Python 3.9+
- Only standard libraries used (no installs required)

## 📂 Input Format: `portfolio.csv`

```
Symbol,Shares,CostBasis,CurrentPrice,DividendYield,CoreShares
JEPQ,100,50.00,55.00,0.088,25
VYM,150,110.00,105.00,0.035,50
O,80,60.00,62.00,0.057,0
PDI,120,18.00,19.50,0.144,20
```

## 🚀 Run Example

```bash
python thomas_engine.py --portfolio portfolio.csv --cash 10000 --out-dir ./out
```

## 📤 Outputs

- `./out/actions_YYYYMMDD.csv` – logs of Skim/Scoop/Note actions
- `./out/portfolio_after.csv` – updated snapshot of your portfolio
- Console output – human-readable summary

## 📌 Notes

- `CoreShares` are never skimmed.
- All rules and parameters are currently hardcoded for simplicity.
- Great for backtesting and building toward a full automation system.
