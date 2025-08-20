#!/usr/bin/env python3
"""
Thomas Phase 1 – Logic Engine (CLI, simulation-only)

Purpose
-------
Replicate the spreadsheet behavior described in the Thomas MVP: accept a
portfolio CSV and a few global knobs, apply Skim/Scoop rules, and emit a
plain-English action log plus machine-readable CSV outputs. No brokerage
integrations. No UI. Guardrails on by default.

Usage
-----
$ python thomas_engine.py \
    --portfolio portfolio.csv \
    --cash 10000 \
    --out-dir ./out

Required CSV schema (header row)
--------------------------------
Symbol,Shares,CostBasis,CurrentPrice,DividendYield[,CoreShares]
- Symbol:            str   (e.g., JEPQ)
- Shares:            float (# of shares currently held)
- CostBasis:         float (dollars per share, average)
- CurrentPrice:      float (dollars per share, current)
- DividendYield:     float (annual yield as decimal, e.g., 0.085 for 8.5%)
- CoreShares:        float (optional; part of the position that can NEVER be skimmed)

Outputs
-------
- out/actions_YYYYMMDD.csv  : machine-readable action log
- out/portfolio_after.csv   : portfolio snapshot after simulated actions
- stdout                    : human-readable recommendations

Design Notes
------------
- Skim trigger: gain ≥ 0 and price > cost basis.
- Skim size: sell all skimmable shares (≥ 0 means no limit).
- Minimum skim proceeds: $10 (skip smaller skims, but log a Note).
- Scoop trigger: price < cost basis.
- Scoop size: $10 per scoop.
- Guardrails: only enforced rule is “never scoop without cash.”

Dependencies: Only Python stdlib.
"""
from __future__ import annotations

import argparse
import csv
import datetime as dt
from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional, Tuple

# ---------------------------- Data Models ---------------------------- #

@dataclass
class Position:
    symbol: str
    shares: float
    cost_basis: float
    price: float
    dividend_yield: float
    core_shares: float = 0.0

    def gain_pct(self) -> float:
        if self.cost_basis <= 0:
            return 0.0
        return (self.price - self.cost_basis) / self.cost_basis


@dataclass
class Action:
    date: dt.date
    symbol: str
    action: str  # "Skim" or "Scoop" or "Note"
    shares: float
    price: float
    cash_delta: float  # + for selling (skim), - for buying (scoop)
    reason: str

# ---------------------------- Engine ---------------------------- #

class ThomasEngine:
    def __init__(
        self,
        positions: List[Position],
        cash: float,
        today: Optional[dt.date] = None,
        scoop_amount: float = 10.0,
        min_skim_proceeds: float = 10.0,
    ) -> None:
        self.positions = {p.symbol.upper(): p for p in positions}
        self.cash = float(cash)
        self.today = today or dt.date.today()
        self.scoop_amount = scoop_amount
        self.min_skim_proceeds = min_skim_proceeds
        self.actions: List[Action] = []

    # ---------- Core logic ---------- #
    def run(self) -> None:
        for sym, pos in self.positions.items():
            # --- Skim logic ---
            if pos.price > pos.cost_basis and pos.gain_pct() >= 0:
                skimmable = max(0.0, pos.shares - pos.core_shares)
                if skimmable > 0:
                    sell_shares = round(skimmable, 2)
                    proceeds = sell_shares * pos.price
                    if proceeds >= self.min_skim_proceeds:
                        pos.shares -= sell_shares
                        self.cash += proceeds
                        self._log(
                            "Skim",
                            pos,
                            sell_shares,
                            pos.price,
                            proceeds,
                            reason=(
                                f"Gain {pos.gain_pct():.1%} ≥ 0; sold {sell_shares} to lock profit and add to cash."
                            ),
                        )
                    else:
                        self._log(
                            "Note",
                            pos,
                            0.0,
                            pos.price,
                            0.0,
                            reason=(
                                f"Skim trigger met but proceeds ${proceeds:.2f} < minimum ${self.min_skim_proceeds:.2f}; skipped."
                            ),
                        )

            # --- Scoop logic ---
            if pos.price < pos.cost_basis and self.cash >= self.scoop_amount:
                buy_shares = round(self.scoop_amount / pos.price, 2)
                cost = buy_shares * pos.price
                if cost <= self.cash and buy_shares > 0:
                    new_total_cost = pos.cost_basis * pos.shares + cost
                    pos.shares += buy_shares
                    pos.cost_basis = new_total_cost / pos.shares if pos.shares > 0 else pos.cost_basis
                    self.cash -= cost
                    self._log(
                        "Scoop",
                        pos,
                        buy_shares,
                        pos.price,
                        -cost,
                        reason=(
                            f"Price {pos.price:.2f} < cost basis {pos.cost_basis:.2f}; bought {buy_shares} to lower basis."
                        ),
                    )

    def _log(self, action: str, pos: Position, shares: float, price: float, cash_delta: float, reason: str) -> None:
        self.actions.append(
            Action(
                date=self.today,
                symbol=pos.symbol,
                action=action,
                shares=shares,
                price=price,
                cash_delta=cash_delta,
                reason=reason,
            )
        )

    # ---------- Output writers ---------- #
    def write_outputs(self, out_dir: Path) -> Tuple[Path, Path]:
        out_dir.mkdir(parents=True, exist_ok=True)
        actions_path = out_dir / f"actions_{self.today.strftime('%Y%m%d')}.csv"
        with actions_path.open("w", newline="", encoding="utf-8") as fh:
            w = csv.writer(fh)
            w.writerow(["Date", "Symbol", "Action", "Shares", "Price", "CashDelta", "Reason"]) 
            for a in self.actions:
                w.writerow([a.date.isoformat(), a.symbol, a.action, f"{a.shares:.2f}", f"{a.price:.2f}", f"{a.cash_delta:.2f}", a.reason])

        portfolio_path = out_dir / "portfolio_after.csv"
        with portfolio_path.open("w", newline="", encoding="utf-8") as fh:
            w = csv.writer(fh)
            w.writerow(["Symbol", "Shares", "CostBasis", "CurrentPrice", "DividendYield", "CoreShares"]) 
            for p in self.positions.values():
                w.writerow([p.symbol, f"{p.shares:.2f}", f"{p.cost_basis:.2f}", f"{p.price:.2f}", f"{p.dividend_yield:.6f}", f"{p.core_shares:.2f}"])

        return actions_path, portfolio_path

    def render_human_summary(self) -> str:
        lines = []
        if not self.actions:
            lines.append("No actions today — all positions within safe ranges.")
        else:
            for a in self.actions:
                if a.action in ("Skim", "Scoop"):
                    verb = "Selling" if a.action == "Skim" else "Buying"
                    lines.append(
                        f"{a.symbol}: {a.action} — {verb} {a.shares:.2f} @ ${a.price:.2f}. Cash change: ${a.cash_delta:.2f}. {a.reason}"
                    )
                elif a.action == "Note":
                    lines.append(f"{a.symbol}: Note — {a.reason}")
                else:
                    lines.append(f"{a.symbol}: {a.action} — {a.reason}")
        lines.append(f"\nEnding cash balance: ${self.cash:.2f}")
        return "\n".join(lines)

# ---------------------------- CSV Loader ---------------------------- #

def load_portfolio_csv(path: Path) -> List[Position]:
    positions: List[Position] = []
    with path.open(newline="", encoding="utf-8") as fh:
        r = csv.DictReader(fh)
        required = {"Symbol", "Shares", "CostBasis", "CurrentPrice", "DividendYield"}
        missing = [c for c in required if c not in r.fieldnames]
        if missing:
            raise ValueError(f"Missing required columns: {missing}")
        for row in r:
            positions.append(
                Position(
                    symbol=row["Symbol"].strip().upper(),
                    shares=float(row["Shares"]),
                    cost_basis=float(row["CostBasis"]),
                    price=float(row["CurrentPrice"]),
                    dividend_yield=float(row["DividendYield"]),
                    core_shares=float(row.get("CoreShares", 0) or 0),
                )
            )
    return positions

# ---------------------------- CLI ---------------------------- #

def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Thomas Phase 1 – Logic Engine (simulation)")
    p.add_argument("--portfolio", type=Path, required=True, help="Path to portfolio CSV")
    p.add_argument("--cash", type=float, required=True, help="Available cash balance for scoops")
    p.add_argument("--scoop-amount", type=float, default=10.0, help="Dollar amount to spend per scoop action")
    p.add_argument("--min-skim-proceeds", type=float, default=10.0, help="Minimum proceeds required for a skim")
    p.add_argument("--out-dir", type=Path, default=Path("out"), help="Output directory for logs")
    p.add_argument("--date", type=str, help="Override date YYYY-MM-DD for simulation")
    return p.parse_args()


def main() -> None:
    args = parse_args()

    positions = load_portfolio_csv(args.portfolio)
    today = dt.date.fromisoformat(args.date) if args.date else None

    engine = ThomasEngine(
        positions=positions,
        cash=args.cash,
        today=today,
        scoop_amount=args.scoop_amount,
        min_skim_proceeds=args.min_skim_proceeds,
    )

    engine.run()

    actions_path, portfolio_path = engine.write_outputs(args.out_dir)

    print(engine.render_human_summary())
    print(f"\nWrote: {actions_path}")
    print(f"Wrote: {portfolio_path}")


if __name__ == "__main__":
    main()
