"""Autonomous Strategy Scheduler — Money Maker runs 24/7.

Strategies define entry/exit conditions and position sizing.
The scheduler checks conditions periodically and executes
trades through the risk-guarded executor pipeline.

Two modes:
  1. Periodic (cron-like): DCA, rebalance, recurring checks
  2. Event-driven: price alerts, volume spikes, threshold triggers

All trades flow through: strategy → risk guardrails → executor → broker
"""
from __future__ import annotations

import asyncio
import json
import logging
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Callable

logger = logging.getLogger(__name__)

DATA_DIR = Path(__file__).parent.parent.parent.parent.parent / "data"
STRATEGIES_FILE = DATA_DIR / "strategies.json"


@dataclass
class Strategy:
    """A trading strategy that runs autonomously."""
    name: str
    description: str
    strategy_type: str           # "dca", "rebalance", "threshold", "custom"
    account: str                 # coinbase, webull_brokerage, roth_ira
    enabled: bool = True

    # What to trade
    ticker: str = ""             # BTC, ETH, AAPL, etc.
    product_id: str = ""         # BTC-USD, ETH-USD (Coinbase format)

    # Position sizing
    amount_usd: float = 0       # Dollar amount per execution
    quantity: float = 0          # Or specific quantity
    max_position_pct: float = 0.10  # Max % of portfolio

    # Schedule (periodic)
    interval_seconds: int = 0   # 0 = event-driven only
    last_executed: float = 0

    # Conditions (event-driven)
    buy_below: float = 0        # Buy when price drops below
    sell_above: float = 0       # Sell when price rises above
    stop_loss: float = 0        # Stop loss price

    # DCA specific
    dca_frequency: str = ""     # "daily", "weekly", "monthly"

    # Limits
    max_executions: int = 0     # 0 = unlimited
    executions_count: int = 0

    def to_dict(self) -> dict:
        return {
            "name": self.name, "description": self.description,
            "strategy_type": self.strategy_type, "account": self.account,
            "enabled": self.enabled, "ticker": self.ticker,
            "product_id": self.product_id, "amount_usd": self.amount_usd,
            "quantity": self.quantity, "max_position_pct": self.max_position_pct,
            "interval_seconds": self.interval_seconds,
            "last_executed": self.last_executed,
            "buy_below": self.buy_below, "sell_above": self.sell_above,
            "stop_loss": self.stop_loss, "dca_frequency": self.dca_frequency,
            "max_executions": self.max_executions,
            "executions_count": self.executions_count,
        }

    @classmethod
    def from_dict(cls, d: dict) -> Strategy:
        return cls(**{k: v for k, v in d.items() if k in cls.__dataclass_fields__})


# ── Built-in Strategy Templates ───────────────────────────────────

def dca_strategy(
    name: str, ticker: str, amount_usd: float,
    frequency: str = "daily", account: str = "coinbase",
) -> Strategy:
    """Dollar-cost averaging — buy fixed amount on schedule."""
    intervals = {"hourly": 3600, "daily": 86400, "weekly": 604800, "monthly": 2592000}
    return Strategy(
        name=name,
        description=f"DCA ${amount_usd} into {ticker} {frequency}",
        strategy_type="dca",
        account=account,
        ticker=ticker,
        product_id=f"{ticker}-USD" if account == "coinbase" else "",
        amount_usd=amount_usd,
        interval_seconds=intervals.get(frequency, 86400),
        dca_frequency=frequency,
    )


def threshold_strategy(
    name: str, ticker: str, buy_below: float = 0,
    sell_above: float = 0, amount_usd: float = 0,
    account: str = "coinbase",
) -> Strategy:
    """Buy when price drops below threshold, sell when above."""
    return Strategy(
        name=name,
        description=f"Buy {ticker} below ${buy_below}, sell above ${sell_above}",
        strategy_type="threshold",
        account=account,
        ticker=ticker,
        product_id=f"{ticker}-USD" if account == "coinbase" else "",
        amount_usd=amount_usd,
        buy_below=buy_below,
        sell_above=sell_above,
        interval_seconds=300,  # Check every 5 min
    )


def rebalance_strategy(
    name: str, targets: dict[str, float], account: str = "coinbase",
) -> Strategy:
    """Rebalance portfolio to target allocations."""
    return Strategy(
        name=name,
        description=f"Rebalance to targets: {targets}",
        strategy_type="rebalance",
        account=account,
        interval_seconds=86400,  # Daily check
    )


class StrategyScheduler:
    """Runs strategies on schedule and monitors conditions."""

    def __init__(self):
        self._strategies: list[Strategy] = []
        self._running = False
        self._task: asyncio.Task | None = None
        self._load_strategies()

    def _load_strategies(self):
        """Load saved strategies from disk."""
        if STRATEGIES_FILE.exists():
            try:
                data = json.loads(STRATEGIES_FILE.read_text())
                self._strategies = [Strategy.from_dict(s) for s in data]
                logger.info(f"Loaded {len(self._strategies)} strategies")
            except Exception as e:
                logger.warning(f"Strategy load failed: {e}")

    def _save_strategies(self):
        """Save strategies to disk."""
        STRATEGIES_FILE.parent.mkdir(parents=True, exist_ok=True)
        STRATEGIES_FILE.write_text(
            json.dumps([s.to_dict() for s in self._strategies], indent=2)
        )

    def add_strategy(self, strategy: Strategy) -> None:
        """Add a new strategy."""
        # Remove existing with same name
        self._strategies = [s for s in self._strategies if s.name != strategy.name]
        self._strategies.append(strategy)
        self._save_strategies()
        logger.info(f"Strategy added: {strategy.name}")

    def remove_strategy(self, name: str) -> bool:
        """Remove a strategy by name."""
        before = len(self._strategies)
        self._strategies = [s for s in self._strategies if s.name != name]
        self._save_strategies()
        return len(self._strategies) < before

    def get_strategies(self) -> list[dict]:
        """List all strategies with status."""
        return [
            {
                **s.to_dict(),
                "next_check": max(0, (s.last_executed + s.interval_seconds) - time.time())
                if s.interval_seconds > 0 else 0,
            }
            for s in self._strategies
        ]

    def toggle_strategy(self, name: str, enabled: bool) -> bool:
        """Enable/disable a strategy."""
        for s in self._strategies:
            if s.name == name:
                s.enabled = enabled
                self._save_strategies()
                return True
        return False

    async def start(self):
        """Start the autonomous scheduler loop."""
        if self._running:
            return
        self._running = True
        self._task = asyncio.create_task(self._run_loop())
        logger.info(f"Strategy scheduler started — {len(self._strategies)} strategies")

    async def stop(self):
        """Stop the scheduler."""
        self._running = False
        if self._task:
            self._task.cancel()
            self._task = None
        logger.info("Strategy scheduler stopped")

    async def _run_loop(self):
        """Main scheduler loop — checks strategies every 30 seconds."""
        while self._running:
            try:
                for strategy in self._strategies:
                    if not strategy.enabled:
                        continue
                    if strategy.max_executions and strategy.executions_count >= strategy.max_executions:
                        continue

                    # Check if it's time
                    if strategy.interval_seconds > 0:
                        elapsed = time.time() - strategy.last_executed
                        if elapsed < strategy.interval_seconds:
                            continue

                    # Execute based on strategy type
                    try:
                        await self._execute_strategy(strategy)
                    except Exception as e:
                        logger.error(f"Strategy {strategy.name} error: {e}")

            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"Scheduler loop error: {e}")

            await asyncio.sleep(30)  # Check every 30 seconds

    async def _execute_strategy(self, strategy: Strategy):
        """Execute a single strategy check."""
        if strategy.strategy_type == "dca":
            await self._execute_dca(strategy)
        elif strategy.strategy_type == "threshold":
            await self._execute_threshold(strategy)
        elif strategy.strategy_type == "rebalance":
            await self._execute_rebalance(strategy)

    async def _execute_dca(self, strategy: Strategy):
        """Dollar-cost average — buy fixed amount."""
        from agentic_hub.core.trading.risk import TradeRequest
        from agentic_hub.core.trading.executor import get_executor

        # Get current price
        price = await self._get_price(strategy)
        if not price:
            return

        quantity = strategy.amount_usd / price

        trade = TradeRequest(
            account=strategy.account,
            action="buy",
            ticker=strategy.ticker,
            quantity=quantity,
            price=price,
            order_type="market",
            strategy=strategy.name,
            reason=f"DCA {strategy.dca_frequency}: ${strategy.amount_usd}",
        )

        executor = get_executor()
        result = await executor.execute(trade, portfolio_value=await self._get_portfolio_value())

        if result.success:
            strategy.last_executed = time.time()
            strategy.executions_count += 1
            self._save_strategies()
            logger.info(f"DCA executed: {strategy.ticker} ${strategy.amount_usd}")

            # Log to hustle engine
            try:
                from agentic_hub.core.trading.hustle import get_hustle_engine
                # DCA is spending, not earning — but track it
            except Exception:
                pass
        else:
            logger.warning(f"DCA rejected: {result.error}")

    async def _execute_threshold(self, strategy: Strategy):
        """Threshold strategy — buy below, sell above."""
        from agentic_hub.core.trading.risk import TradeRequest
        from agentic_hub.core.trading.executor import get_executor

        price = await self._get_price(strategy)
        if not price:
            return

        trade = None

        if strategy.buy_below and price <= strategy.buy_below:
            quantity = strategy.amount_usd / price if strategy.amount_usd else strategy.quantity
            trade = TradeRequest(
                account=strategy.account, action="buy",
                ticker=strategy.ticker, quantity=quantity, price=price,
                order_type="market", strategy=strategy.name,
                reason=f"Price ${price:.2f} <= threshold ${strategy.buy_below:.2f}",
                stop_loss=strategy.stop_loss,
            )
        elif strategy.sell_above and price >= strategy.sell_above:
            quantity = strategy.quantity or (strategy.amount_usd / price if strategy.amount_usd else 0)
            if quantity > 0:
                trade = TradeRequest(
                    account=strategy.account, action="sell",
                    ticker=strategy.ticker, quantity=quantity, price=price,
                    order_type="market", strategy=strategy.name,
                    reason=f"Price ${price:.2f} >= threshold ${strategy.sell_above:.2f}",
                )

        if trade:
            executor = get_executor()
            result = await executor.execute(trade, portfolio_value=await self._get_portfolio_value())
            if result.success:
                strategy.last_executed = time.time()
                strategy.executions_count += 1
                self._save_strategies()
                logger.info(f"Threshold executed: {trade.action} {strategy.ticker} @ ${price:.2f}")
            else:
                logger.warning(f"Threshold rejected: {result.error}")

        # Update last check time regardless
        strategy.last_executed = time.time()
        self._save_strategies()

    async def _execute_rebalance(self, strategy: Strategy):
        """Rebalance portfolio to target allocations. (Stub — needs target config)"""
        strategy.last_executed = time.time()
        self._save_strategies()
        logger.info(f"Rebalance check: {strategy.name} (not yet implemented with targets)")

    async def _get_price(self, strategy: Strategy) -> float | None:
        """Get current price for a strategy's ticker."""
        if strategy.account == "coinbase":
            try:
                from agentic_hub.core.trading.coinbase_client import get_coinbase
                cb = get_coinbase()
                return cb.get_price(strategy.product_id or f"{strategy.ticker}-USD")
            except Exception:
                pass

        # Fallback to Yahoo Finance
        try:
            import httpx
            async with httpx.AsyncClient() as client:
                r = await client.get(
                    f"https://query1.finance.yahoo.com/v8/finance/chart/{strategy.ticker}",
                    headers={"User-Agent": "spider.Web/2.5"},
                )
                data = r.json()
                return data["chart"]["result"][0]["meta"]["regularMarketPrice"]
        except Exception:
            pass
        return None

    async def _get_portfolio_value(self) -> float:
        """Get total portfolio value."""
        try:
            from agentic_hub.core.trading.coinbase_client import get_coinbase
            cb = get_coinbase()
            if cb.is_configured:
                return cb.get_portfolio_value()
        except Exception:
            pass
        return 10000.0  # Default


# Singleton
_scheduler: StrategyScheduler | None = None


def get_scheduler() -> StrategyScheduler:
    global _scheduler
    if _scheduler is None:
        _scheduler = StrategyScheduler()
    return _scheduler


async def start_scheduler():
    """Start the autonomous strategy scheduler."""
    scheduler = get_scheduler()
    await scheduler.start()
