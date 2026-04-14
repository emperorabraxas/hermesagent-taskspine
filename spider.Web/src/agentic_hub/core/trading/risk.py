"""Risk Guardrails — hard limits that even Money Maker can't override.

These are CODE-LEVEL constraints, not prompt instructions. The LLM
cannot talk itself out of these. If a trade violates any guardrail,
it's rejected before reaching the broker.

Guardrails scale with portfolio size, not arbitrary fixed numbers.
"""
from __future__ import annotations

import logging
import time
from dataclasses import dataclass, field
from typing import Any

logger = logging.getLogger(__name__)


# ══════════════════════════════════════════════════════════════════════
# HARD LIMITS — MODIFY THESE IN CODE ONLY, NEVER VIA PROMPT/API
# ══════════════════════════════════════════════════════════════════════

# Max % of total portfolio in a single position
MAX_POSITION_PCT = 0.15  # 15% max in any one ticker

# Max % of account value to risk per trade (stop-loss based)
MAX_RISK_PER_TRADE_PCT = 0.02  # 2% max risk per trade

# Max daily drawdown before all trading halts
MAX_DAILY_DRAWDOWN_PCT = 0.05  # 5% daily loss = full stop

# Max number of trades per day (prevents panic trading)
MAX_TRADES_PER_DAY = 20

# Max single order value (absolute dollar cap)
MAX_SINGLE_ORDER_USD = 5000.0

# Min time between trades on same ticker (seconds)
MIN_TRADE_INTERVAL = 300  # 5 minutes

# Max portfolio leverage (1.0 = no leverage)
MAX_LEVERAGE = 1.0  # Cash only, no margin

# Max correlation — don't overload same sector/direction
MAX_CORRELATED_POSITIONS = 3  # Max 3 positions in same sector

# Crypto-specific
MAX_CRYPTO_PCT = 0.20  # Max 20% of portfolio in crypto
MAX_SINGLE_CRYPTO_PCT = 0.10  # Max 10% in any one crypto

# Gambling-specific
MAX_DAILY_GAMBLING_USD = 100.0  # Hard daily cap on gambling
MAX_SINGLE_BET_USD = 25.0  # Per-bet cap

# ══════════════════════════════════════════════════════════════════════


@dataclass
class TradeRequest:
    """A proposed trade that must pass guardrails before execution."""
    account: str           # webull_brokerage, roth_ira, coinbase, etc.
    action: str            # buy, sell, short, cover
    ticker: str            # AAPL, BTC, ETH, etc.
    quantity: float        # Shares or units
    price: float           # Current/limit price
    order_type: str        # market, limit, stop, stop_limit
    strategy: str          # Name of the strategy that generated this
    reason: str            # Why this trade
    stop_loss: float = 0   # Stop loss price (0 = none)
    take_profit: float = 0 # Take profit price (0 = none)

    @property
    def total_value(self) -> float:
        return abs(self.quantity * self.price)


@dataclass
class GuardrailResult:
    """Result of a guardrail check."""
    approved: bool
    violations: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)


class RiskGuardrails:
    """Enforces hard risk limits on all trades.

    Every trade passes through check() before reaching any broker.
    Violations = rejected. No exceptions. No overrides.
    """

    def __init__(self):
        self._daily_trades: list[dict] = []
        self._daily_pnl: float = 0.0
        self._daily_gambling: float = 0.0
        self._last_trade_time: dict[str, float] = {}  # ticker -> timestamp
        self._day_start: float = 0.0
        self._reset_daily()

    def _reset_daily(self):
        """Reset daily counters at midnight."""
        now = time.time()
        # Check if it's a new day
        import datetime
        today = datetime.date.today()
        if self._day_start == 0 or datetime.date.fromtimestamp(self._day_start) != today:
            self._daily_trades = []
            self._daily_pnl = 0.0
            self._daily_gambling = 0.0
            self._day_start = time.time()

    def check(
        self,
        trade: TradeRequest,
        portfolio_value: float,
        positions: dict[str, float] | None = None,
    ) -> GuardrailResult:
        """Check a trade against all guardrails.

        Args:
            trade: The proposed trade
            portfolio_value: Total portfolio value across all accounts
            positions: Current positions {ticker: current_value}

        Returns:
            GuardrailResult with approved/rejected + reasons
        """
        self._reset_daily()
        violations = []
        warnings = []
        positions = positions or {}

        # 1. Single order value cap
        if trade.total_value > MAX_SINGLE_ORDER_USD:
            violations.append(
                f"Order ${trade.total_value:.2f} exceeds max ${MAX_SINGLE_ORDER_USD:.2f}"
            )

        # 2. Position size limit
        if portfolio_value > 0:
            position_pct = trade.total_value / portfolio_value
            if position_pct > MAX_POSITION_PCT:
                violations.append(
                    f"Position {position_pct:.1%} exceeds max {MAX_POSITION_PCT:.0%} of portfolio"
                )

            # Check existing position + this trade
            existing = positions.get(trade.ticker, 0)
            new_total = existing + trade.total_value
            if new_total / portfolio_value > MAX_POSITION_PCT:
                violations.append(
                    f"Combined position ${new_total:.2f} ({new_total/portfolio_value:.1%}) exceeds limit"
                )

        # 3. Daily trade count
        if len(self._daily_trades) >= MAX_TRADES_PER_DAY:
            violations.append(
                f"Daily trade limit reached ({MAX_TRADES_PER_DAY})"
            )

        # 4. Daily drawdown
        if self._daily_pnl < -(portfolio_value * MAX_DAILY_DRAWDOWN_PCT):
            violations.append(
                f"Daily drawdown ${abs(self._daily_pnl):.2f} exceeds {MAX_DAILY_DRAWDOWN_PCT:.0%} limit — TRADING HALTED"
            )

        # 5. Trade interval (same ticker)
        last = self._last_trade_time.get(trade.ticker, 0)
        if time.time() - last < MIN_TRADE_INTERVAL:
            remaining = int(MIN_TRADE_INTERVAL - (time.time() - last))
            violations.append(
                f"Too soon — wait {remaining}s before trading {trade.ticker} again"
            )

        # 6. Risk per trade (if stop loss provided)
        if trade.stop_loss and trade.action == "buy" and portfolio_value > 0:
            risk = abs(trade.price - trade.stop_loss) * trade.quantity
            risk_pct = risk / portfolio_value
            if risk_pct > MAX_RISK_PER_TRADE_PCT:
                violations.append(
                    f"Risk ${risk:.2f} ({risk_pct:.1%}) exceeds {MAX_RISK_PER_TRADE_PCT:.0%} per-trade limit"
                )

        # 7. Crypto limits
        if trade.ticker in ("BTC", "ETH", "SOL", "DOGE", "ADA", "XRP", "AVAX", "DOT", "LINK", "MATIC"):
            crypto_total = sum(v for t, v in positions.items()
                             if t in ("BTC", "ETH", "SOL", "DOGE", "ADA", "XRP"))
            if portfolio_value > 0:
                if (crypto_total + trade.total_value) / portfolio_value > MAX_CRYPTO_PCT:
                    violations.append(
                        f"Crypto allocation would exceed {MAX_CRYPTO_PCT:.0%} limit"
                    )

        # 8. Gambling limits
        if trade.account == "gambling" or trade.strategy.startswith("bet_"):
            if self._daily_gambling + trade.total_value > MAX_DAILY_GAMBLING_USD:
                violations.append(
                    f"Daily gambling ${self._daily_gambling + trade.total_value:.2f} exceeds ${MAX_DAILY_GAMBLING_USD:.2f} cap"
                )
            if trade.total_value > MAX_SINGLE_BET_USD:
                violations.append(
                    f"Bet ${trade.total_value:.2f} exceeds ${MAX_SINGLE_BET_USD:.2f} per-bet cap"
                )

        # 9. No leverage
        if trade.action in ("short", "margin_buy"):
            violations.append("Leverage/shorting disabled — cash only")

        # Warnings (non-blocking)
        if trade.order_type == "market":
            warnings.append("Market order — consider using limit for better fills")
        if not trade.stop_loss and trade.action == "buy":
            warnings.append("No stop loss set — consider adding one")

        approved = len(violations) == 0

        if violations:
            logger.warning(f"TRADE REJECTED: {trade.ticker} {trade.action} — {violations}")
        else:
            logger.info(f"TRADE APPROVED: {trade.ticker} {trade.action} ${trade.total_value:.2f}")

        return GuardrailResult(approved=approved, violations=violations, warnings=warnings)

    def record_trade(self, trade: TradeRequest, pnl: float = 0) -> None:
        """Record a completed trade for daily tracking."""
        self._daily_trades.append({
            "ticker": trade.ticker,
            "action": trade.action,
            "value": trade.total_value,
            "time": time.time(),
        })
        self._last_trade_time[trade.ticker] = time.time()
        self._daily_pnl += pnl

        if trade.account == "gambling" or trade.strategy.startswith("bet_"):
            self._daily_gambling += trade.total_value

    def get_status(self) -> dict:
        """Get current risk status."""
        self._reset_daily()
        return {
            "trades_today": len(self._daily_trades),
            "max_trades": MAX_TRADES_PER_DAY,
            "daily_pnl": round(self._daily_pnl, 2),
            "daily_gambling": round(self._daily_gambling, 2),
            "max_daily_gambling": MAX_DAILY_GAMBLING_USD,
            "limits": {
                "max_position_pct": MAX_POSITION_PCT,
                "max_risk_per_trade": MAX_RISK_PER_TRADE_PCT,
                "max_daily_drawdown": MAX_DAILY_DRAWDOWN_PCT,
                "max_single_order": MAX_SINGLE_ORDER_USD,
                "max_crypto_pct": MAX_CRYPTO_PCT,
                "leverage": "disabled",
            },
        }


# Singleton
_engine: RiskGuardrails | None = None


def get_risk_engine() -> RiskGuardrails:
    global _engine
    if _engine is None:
        _engine = RiskGuardrails()
    return _engine
