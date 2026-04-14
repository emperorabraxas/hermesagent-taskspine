"""Portfolio persistence for Money Maker.

Tracks all trades, positions, account balances, and performance over time.
Stored as JSON — survives restarts, builds a complete picture of the user's
financial profile across all accounts.
"""
from __future__ import annotations

import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)

DATA_DIR = Path(__file__).parent.parent.parent.parent / "data"
PORTFOLIO_FILE = DATA_DIR / "portfolio.json"


def _default_portfolio() -> dict:
    """Create empty portfolio structure."""
    return {
        "accounts": {
            "webull_checking": {"type": "checking", "provider": "Webull", "balance": 0},
            "roth_ira": {"type": "retirement", "provider": "Webull", "balance": 0, "positions": []},
            "webull_brokerage": {"type": "brokerage", "provider": "Webull", "balance": 0, "positions": []},
            "coinbase": {"type": "crypto", "provider": "Coinbase", "balance": 0, "positions": []},
            "chime": {"type": "savings", "provider": "Chime", "balance": 0},
            "cashapp": {"type": "peer", "provider": "CashApp/Venmo", "balance": 0},
        },
        "trades": [],
        "watchlist": [],
        "notes": [],
        "stats": {
            "total_invested": 0,
            "total_realized_pnl": 0,
            "trades_count": 0,
            "first_trade_date": None,
            "last_updated": None,
        },
    }


def load_portfolio() -> dict:
    """Load portfolio from disk."""
    if PORTFOLIO_FILE.exists():
        try:
            return json.loads(PORTFOLIO_FILE.read_text())
        except Exception as e:
            logger.warning(f"Failed to load portfolio: {e}")
    return _default_portfolio()


def save_portfolio(portfolio: dict):
    """Save portfolio to disk."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    portfolio["stats"]["last_updated"] = datetime.now().isoformat()
    PORTFOLIO_FILE.write_text(json.dumps(portfolio, indent=2, default=str))


def log_trade(
    account: str,
    action: str,  # buy, sell, deposit, withdraw, swap, stake
    ticker: str,
    quantity: float,
    price: float,
    notes: str = "",
) -> dict:
    """Log a trade and update positions."""
    portfolio = load_portfolio()
    now = datetime.now().isoformat()

    trade = {
        "id": len(portfolio["trades"]) + 1,
        "account": account,
        "action": action,
        "ticker": ticker.upper(),
        "quantity": quantity,
        "price": price,
        "total": round(quantity * price, 2),
        "notes": notes,
        "timestamp": now,
    }
    portfolio["trades"].append(trade)
    portfolio["stats"]["trades_count"] += 1

    if not portfolio["stats"]["first_trade_date"]:
        portfolio["stats"]["first_trade_date"] = now

    # Update positions in the account
    acct = portfolio["accounts"].get(account)
    if acct and "positions" in acct:
        _update_positions(acct, action, ticker.upper(), quantity, price)

    if action in ("buy", "deposit"):
        portfolio["stats"]["total_invested"] += trade["total"]

    save_portfolio(portfolio)
    return trade


def _update_positions(acct: dict, action: str, ticker: str, qty: float, price: float):
    """Update position list after a trade."""
    positions = acct["positions"]
    existing = next((p for p in positions if p["ticker"] == ticker), None)

    if action in ("buy", "stake"):
        if existing:
            # Average cost basis
            total_cost = existing["avg_cost"] * existing["quantity"] + price * qty
            existing["quantity"] += qty
            existing["avg_cost"] = round(total_cost / existing["quantity"], 4) if existing["quantity"] else 0
        else:
            positions.append({
                "ticker": ticker,
                "quantity": qty,
                "avg_cost": price,
                "first_bought": datetime.now().isoformat(),
            })
    elif action in ("sell", "swap"):
        if existing:
            existing["quantity"] -= qty
            if existing["quantity"] <= 0:
                positions.remove(existing)


def update_balance(account: str, balance: float):
    """Update an account's cash balance."""
    portfolio = load_portfolio()
    if account in portfolio["accounts"]:
        portfolio["accounts"][account]["balance"] = balance
        save_portfolio(portfolio)


def add_to_watchlist(ticker: str, notes: str = ""):
    """Add a ticker to the watchlist."""
    portfolio = load_portfolio()
    if not any(w["ticker"] == ticker.upper() for w in portfolio["watchlist"]):
        portfolio["watchlist"].append({
            "ticker": ticker.upper(),
            "added": datetime.now().isoformat(),
            "notes": notes,
        })
        save_portfolio(portfolio)


def get_portfolio_summary() -> str:
    """Generate a human-readable portfolio summary for injection into Money Maker's context."""
    p = load_portfolio()

    lines = ["=== YOUR PORTFOLIO ===\n"]

    # Accounts
    for key, acct in p["accounts"].items():
        name = acct.get("provider", key)
        atype = acct.get("type", "")
        balance = acct.get("balance", 0)
        lines.append(f"📊 {name} ({atype}): ${balance:,.2f}")

        positions = acct.get("positions", [])
        if positions:
            for pos in positions:
                lines.append(f"   {pos['ticker']}: {pos['quantity']} @ ${pos['avg_cost']:.2f} avg")

    # Stats
    s = p["stats"]
    lines.append(f"\n📈 Total invested: ${s['total_invested']:,.2f}")
    lines.append(f"🔢 Total trades: {s['trades_count']}")
    if s.get("first_trade_date"):
        lines.append(f"📅 Trading since: {s['first_trade_date'][:10]}")

    # Recent trades
    recent = p["trades"][-10:]
    if recent:
        lines.append("\n🕐 Recent trades:")
        for t in reversed(recent):
            lines.append(f"   {t['timestamp'][:10]} {t['action'].upper()} {t['quantity']} {t['ticker']} @ ${t['price']:.2f} ({t['account']})")

    # Watchlist
    if p["watchlist"]:
        lines.append("\n👀 Watchlist: " + ", ".join(w["ticker"] for w in p["watchlist"]))

    return "\n".join(lines)
