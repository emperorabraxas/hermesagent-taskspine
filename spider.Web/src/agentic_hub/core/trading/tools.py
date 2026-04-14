"""Trading tools — Money Maker's hands for executing trades.

These tools are registered in the ToolRegistry and available ONLY
to the money_maker agent. Every trade goes through the executor
which enforces risk guardrails before reaching any broker.
"""
from __future__ import annotations

import json
import logging
from typing import Any

from agentic_hub.core.tools.base import BaseTool, ToolParameter, ToolResult

logger = logging.getLogger(__name__)


class TradeTool(BaseTool):
    """Execute a buy or sell order through the risk-checked executor."""

    @property
    def name(self) -> str:
        return "trade"

    @property
    def description(self) -> str:
        return (
            "Place a buy or sell order for stocks or crypto. Every trade is checked "
            "against risk guardrails before execution. Requires user approval for "
            "first use of any new strategy."
        )

    @property
    def parameters(self) -> list[ToolParameter]:
        return [
            ToolParameter("account", "string", "Account: coinbase, webull_brokerage, roth_ira", required=True),
            ToolParameter("action", "string", "Action: buy or sell", required=True),
            ToolParameter("ticker", "string", "Ticker symbol: AAPL, BTC, ETH, etc.", required=True),
            ToolParameter("quantity", "number", "Number of shares/units", required=True),
            ToolParameter("price", "number", "Current price per unit (for risk calculation)", required=True),
            ToolParameter("order_type", "string", "Order type: market or limit (default: market)"),
            ToolParameter("strategy", "string", "Strategy name that generated this trade", required=True),
            ToolParameter("reason", "string", "Why this trade (brief explanation)", required=True),
            ToolParameter("stop_loss", "number", "Stop loss price (recommended)"),
        ]

    async def execute(self, **kwargs: Any) -> ToolResult:
        import asyncio
        from agentic_hub.core.trading.risk import TradeRequest
        from agentic_hub.core.trading.executor import get_executor

        try:
            trade = TradeRequest(
                account=kwargs.get("account", ""),
                action=kwargs.get("action", ""),
                ticker=kwargs.get("ticker", "").upper(),
                quantity=float(kwargs.get("quantity", 0)),
                price=float(kwargs.get("price", 0)),
                order_type=kwargs.get("order_type", "market"),
                strategy=kwargs.get("strategy", "manual"),
                reason=kwargs.get("reason", ""),
                stop_loss=float(kwargs.get("stop_loss", 0)),
            )

            executor = get_executor()

            # Get portfolio value for risk calculations
            portfolio_value = await self._get_portfolio_value()

            result = await executor.execute(
                trade=trade,
                portfolio_value=portfolio_value,
            )

            if result.success:
                return ToolResult(
                    output=(
                        f"TRADE EXECUTED: {trade.action.upper()} {trade.quantity} {trade.ticker} "
                        f"@ ${trade.price:.2f} = ${trade.total_value:.2f}\n"
                        f"Account: {trade.account}\n"
                        f"Order: {trade.order_type}\n"
                        f"Broker response: {json.dumps(result.broker_response)}"
                    ),
                    success=True,
                )
            else:
                warnings = "\n".join(f"  ⚠️ {w}" for w in result.guardrail_result.warnings)
                violations = "\n".join(f"  ❌ {v}" for v in result.guardrail_result.violations)
                return ToolResult(
                    output=(
                        f"TRADE REJECTED: {trade.action} {trade.ticker}\n"
                        f"Error: {result.error}\n"
                        f"{violations}\n{warnings}"
                    ),
                    success=False,
                    error=result.error,
                )

        except Exception as e:
            return ToolResult(output="", success=False, error=f"Trade error: {e}")

    async def _get_portfolio_value(self) -> float:
        """Get total portfolio value from all sources."""
        total = 0.0
        # Try Coinbase
        try:
            from agentic_hub.core.trading.coinbase_client import get_coinbase
            cb = get_coinbase()
            if cb.is_configured:
                total += cb.get_portfolio_value()
        except Exception:
            pass
        # Try Plaid accounts
        try:
            from agentic_hub.core.plaid_client import get_plaid_manager
            from agentic_hub.core.secrets import get_vault
            mgr = get_plaid_manager()
            vault = get_vault()
            if vault:
                for key in vault.list_keys():
                    if key.startswith("PLAID_ACCESS_"):
                        token = vault.retrieve(key)
                        if token:
                            balances = mgr.get_balances(token)
                            total += sum(b.get("current", 0) for b in balances)
        except Exception:
            pass
        return total or 10000.0  # Default $10K if no accounts connected


class QuoteTool(BaseTool):
    """Get real-time price quotes for stocks and crypto."""

    @property
    def name(self) -> str:
        return "quote"

    @property
    def description(self) -> str:
        return "Get current price, bid/ask, volume, and change for a stock or crypto ticker."

    @property
    def parameters(self) -> list[ToolParameter]:
        return [
            ToolParameter("ticker", "string", "Ticker symbol: AAPL, BTC, ETH, SPY, etc.", required=True),
        ]

    async def execute(self, **kwargs: Any) -> ToolResult:
        ticker = kwargs.get("ticker", "").upper()
        if not ticker:
            return ToolResult(output="", success=False, error="Ticker required")

        # Try crypto first (via Coinbase)
        crypto_tickers = {"BTC", "ETH", "SOL", "DOGE", "ADA", "XRP", "AVAX", "DOT", "LINK", "MATIC"}
        if ticker in crypto_tickers:
            try:
                from agentic_hub.core.trading.coinbase_client import get_coinbase
                cb = get_coinbase()
                if cb.is_configured:
                    price = cb.get_price(f"{ticker}-USD")
                    if price:
                        return ToolResult(
                            output=f"{ticker}: ${price:,.2f} (Coinbase)",
                            success=True,
                        )
            except Exception:
                pass
            # Fallback to CoinGecko
            try:
                import httpx
                gecko_ids = {"BTC": "bitcoin", "ETH": "ethereum", "SOL": "solana",
                            "DOGE": "dogecoin", "ADA": "cardano", "XRP": "ripple"}
                gid = gecko_ids.get(ticker, ticker.lower())
                async with httpx.AsyncClient() as client:
                    r = await client.get(f"https://api.coingecko.com/api/v3/simple/price?ids={gid}&vs_currencies=usd&include_24hr_change=true")
                    data = r.json()
                    if gid in data:
                        price = data[gid]["usd"]
                        change = data[gid].get("usd_24h_change", 0)
                        return ToolResult(
                            output=f"{ticker}: ${price:,.2f} ({change:+.2f}% 24h)",
                            success=True,
                        )
            except Exception as e:
                return ToolResult(output="", success=False, error=f"Quote failed: {e}")

        # Stock quote via Webull or Yahoo
        try:
            from agentic_hub.core.trading.webull_client import get_webull
            webull = get_webull()
            if webull.is_configured and webull.is_authorized:
                quote = webull.get_quote(ticker)
                if quote:
                    return ToolResult(
                        output=(
                            f"{ticker}: ${quote['price']:.2f} ({quote['change_pct']:+.2f}%)\n"
                            f"Bid: ${quote['bid']:.2f} Ask: ${quote['ask']:.2f} Vol: {quote['volume']:,}"
                        ),
                        success=True,
                    )
        except Exception:
            pass

        # Yahoo Finance fallback
        try:
            import httpx
            async with httpx.AsyncClient() as client:
                r = await client.get(
                    f"https://query1.finance.yahoo.com/v8/finance/chart/{ticker}?interval=1d&range=1d",
                    headers={"User-Agent": "spider.Web/2.5"},
                )
                data = r.json()
                meta = data["chart"]["result"][0]["meta"]
                price = meta["regularMarketPrice"]
                prev = meta.get("chartPreviousClose", price)
                change = ((price - prev) / prev * 100) if prev else 0
                return ToolResult(
                    output=(
                        f"{ticker}: ${price:.2f} ({change:+.2f}%)\n"
                        f"High: ${meta.get('regularMarketDayHigh', 0):.2f} "
                        f"Low: ${meta.get('regularMarketDayLow', 0):.2f}"
                    ),
                    success=True,
                )
        except Exception as e:
            return ToolResult(output="", success=False, error=f"Quote failed for {ticker}: {e}")


class PortfolioTool(BaseTool):
    """View current portfolio balances and positions."""

    @property
    def name(self) -> str:
        return "portfolio"

    @property
    def description(self) -> str:
        return "View current portfolio balances, positions, and P&L across all connected accounts."

    @property
    def parameters(self) -> list[ToolParameter]:
        return [
            ToolParameter("account", "string", "Filter by account (optional): coinbase, webull_brokerage, roth_ira, all"),
        ]

    async def execute(self, **kwargs: Any) -> ToolResult:
        account_filter = kwargs.get("account", "all").lower()
        lines = ["PORTFOLIO STATUS"]
        total = 0.0

        # Coinbase
        if account_filter in ("all", "coinbase"):
            try:
                from agentic_hub.core.trading.coinbase_client import get_coinbase
                cb = get_coinbase()
                if cb.is_configured:
                    accounts = cb.get_accounts()
                    if accounts:
                        lines.append("\n📊 COINBASE:")
                        for a in accounts:
                            lines.append(f"  {a['currency']}: {a['balance']:.6f}")
                            total += a["balance"] if a["currency"] == "USD" else 0
                        cb_val = cb.get_portfolio_value()
                        lines.append(f"  Total: ${cb_val:,.2f}")
                        total += cb_val
            except Exception as e:
                lines.append(f"\n📊 COINBASE: {e}")

        # Webull
        if account_filter in ("all", "webull_brokerage", "roth_ira"):
            try:
                from agentic_hub.core.trading.webull_client import get_webull
                webull = get_webull()
                if webull.is_configured and webull.is_authorized:
                    accounts = webull.get_accounts()
                    for a in accounts:
                        lines.append(f"\n🏦 WEBULL ({a['type']}):")
                        lines.append(f"  Cash: ${a['cash_balance']:,.2f}")
                        lines.append(f"  Total: ${a['total_value']:,.2f}")
                        for p in a.get("positions", []):
                            lines.append(
                                f"  {p['symbol']}: {p['quantity']} shares "
                                f"@ ${p['avg_price']:.2f} → ${p['market_value']:,.2f}"
                            )
                        total += a["total_value"]
            except Exception as e:
                lines.append(f"\n🏦 WEBULL: {e}")

        # Manual accounts from vault
        try:
            import json as _json
            vault_accounts = _json.loads(
                __import__("builtins").__dict__["__import__"]("os")
                .environ.get("_vault_accounts", "[]")
            )
        except Exception:
            pass

        lines.append(f"\n💰 NET WORTH: ${total:,.2f}" if total > 0 else "\n💰 No accounts connected")

        # Risk status
        try:
            from agentic_hub.core.trading.risk import get_risk_engine
            risk = get_risk_engine()
            status = risk.get_status()
            lines.append(f"\n📊 RISK: {status['trades_today']}/{status['max_trades']} trades today, P&L: ${status['daily_pnl']:+,.2f}")
        except Exception:
            pass

        return ToolResult(output="\n".join(lines), success=True)


class RiskStatusTool(BaseTool):
    """Check current risk guardrail status and limits."""

    @property
    def name(self) -> str:
        return "risk_status"

    @property
    def description(self) -> str:
        return "Check trading risk limits, daily trade count, P&L, and guardrail configuration."

    @property
    def parameters(self) -> list[ToolParameter]:
        return []

    async def execute(self, **kwargs: Any) -> ToolResult:
        from agentic_hub.core.trading.risk import get_risk_engine
        risk = get_risk_engine()
        status = risk.get_status()
        limits = status["limits"]

        output = (
            f"RISK GUARDRAILS\n"
            f"Trades today: {status['trades_today']}/{status['max_trades']}\n"
            f"Daily P&L: ${status['daily_pnl']:+,.2f}\n"
            f"Daily gambling: ${status['daily_gambling']:.2f}/${status['max_daily_gambling']:.2f}\n\n"
            f"LIMITS:\n"
            f"  Max position: {limits['max_position_pct']:.0%} of portfolio\n"
            f"  Max risk/trade: {limits['max_risk_per_trade']:.0%}\n"
            f"  Max drawdown: {limits['max_daily_drawdown']:.0%}/day\n"
            f"  Max order: ${limits['max_single_order']:,.0f}\n"
            f"  Max crypto: {limits['max_crypto_pct']:.0%} of portfolio\n"
            f"  Leverage: {limits['leverage']}"
        )
        return ToolResult(output=output, success=True)


class HustleTool(BaseTool):
    """Track zero-capital earnings and opportunities toward the $600 goal."""

    @property
    def name(self) -> str:
        return "hustle"

    @property
    def description(self) -> str:
        return (
            "Track the bootstrap experiment: log earnings, find opportunities, "
            "check progress toward the $600 Series 65 goal. Actions: progress, "
            "log_earning, opportunities, seed."
        )

    @property
    def parameters(self) -> list[ToolParameter]:
        return [
            ToolParameter("action", "string", "Action: progress, log_earning, opportunities, seed", required=True),
            ToolParameter("source", "string", "Earning source: airdrop, dfs, sportsbook, referral, credit_card"),
            ToolParameter("amount", "number", "Dollar amount earned"),
            ToolParameter("description", "string", "Description of the earning or opportunity"),
        ]

    async def execute(self, **kwargs: Any) -> ToolResult:
        from agentic_hub.core.trading.hustle import get_hustle_engine

        action = kwargs.get("action", "progress")
        engine = get_hustle_engine()

        if action == "progress":
            p = engine.get_progress()
            bar_len = 20
            filled = int(bar_len * p["progress_pct"] / 100)
            bar = "█" * filled + "░" * (bar_len - filled)

            lines = [
                f"BOOTSTRAP EXPERIMENT — Series 65 Fund",
                f"{'=' * 45}",
                f"[{bar}] {p['progress_pct']}%",
                f"Earned: ${p['earned']:.2f} / ${p['goal']:.2f}",
                f"Remaining: ${p['remaining']:.2f}",
                f"",
                f"BREAKDOWN:",
            ]
            for src, amt in sorted(p["breakdown"].items(), key=lambda x: -x[1]):
                lines.append(f"  {src}: ${amt:.2f}")
            if not p["breakdown"]:
                lines.append("  (no earnings yet)")
            lines.append(f"\nOpportunities: {p['active_opportunities']} active / {p['opportunities']} total")
            return ToolResult(output="\n".join(lines), success=True)

        elif action == "log_earning":
            source = kwargs.get("source", "other")
            amount = float(kwargs.get("amount", 0))
            desc = kwargs.get("description", "")
            if amount <= 0:
                return ToolResult(output="", success=False, error="Amount must be positive")
            engine.log_earning(source, amount, desc)
            total = engine.get_total_earnings()
            remaining = max(0, 600 - total)
            return ToolResult(
                output=f"Logged: +${amount:.2f} from {source}\nTotal: ${total:.2f} / $600.00\nRemaining: ${remaining:.2f}",
                success=True,
            )

        elif action == "opportunities":
            source = kwargs.get("source", "")
            opps = engine.get_opportunities(source=source, status="open")
            if not opps:
                return ToolResult(output="No open opportunities. Run action=seed to populate.", success=True)
            lines = [f"{len(opps)} OPEN OPPORTUNITIES:"]
            total_potential = 0
            for o in opps:
                val = o.get("potential_value", 0)
                total_potential += val
                lines.append(f"  [{o['source']}] {o['name']} — ${val:.0f}")
                if o.get("notes"):
                    lines.append(f"    {o['notes']}")
            lines.append(f"\nTotal potential: ${total_potential:.0f}")
            return ToolResult(output="\n".join(lines), success=True)

        elif action == "seed":
            added = engine.seed_opportunities()
            return ToolResult(output=f"Seeded {added} new opportunities. Run action=opportunities to see them.", success=True)

        return ToolResult(output="", success=False, error=f"Unknown action: {action}")


class StrategyTool(BaseTool):
    """Create and manage autonomous trading strategies."""

    @property
    def name(self) -> str:
        return "strategy"

    @property
    def description(self) -> str:
        return (
            "Create, list, enable/disable autonomous trading strategies. "
            "Strategies run 24/7: DCA (dollar-cost averaging), threshold "
            "(buy below/sell above price), rebalance. Actions: list, create_dca, "
            "create_threshold, enable, disable, remove."
        )

    @property
    def parameters(self) -> list[ToolParameter]:
        return [
            ToolParameter("action", "string", "Action: list, create_dca, create_threshold, enable, disable, remove", required=True),
            ToolParameter("name", "string", "Strategy name"),
            ToolParameter("ticker", "string", "Ticker: BTC, ETH, SOL, AAPL, etc."),
            ToolParameter("amount", "number", "Dollar amount per execution"),
            ToolParameter("frequency", "string", "DCA frequency: hourly, daily, weekly, monthly"),
            ToolParameter("buy_below", "number", "Buy when price drops below this"),
            ToolParameter("sell_above", "number", "Sell when price rises above this"),
            ToolParameter("account", "string", "Account: coinbase, webull_brokerage, roth_ira"),
        ]

    async def execute(self, **kwargs: Any) -> ToolResult:
        from agentic_hub.core.trading.scheduler import (
            get_scheduler, dca_strategy, threshold_strategy,
        )

        action = kwargs.get("action", "list")
        scheduler = get_scheduler()

        if action == "list":
            strategies = scheduler.get_strategies()
            if not strategies:
                return ToolResult(output="No strategies configured. Create one with action=create_dca or create_threshold.", success=True)

            lines = [f"STRATEGIES: {len(strategies)}"]
            for s in strategies:
                status = "ON" if s["enabled"] else "OFF"
                next_check = f"next: {int(s['next_check'])}s" if s["next_check"] > 0 else "event-driven"
                lines.append(
                    f"  [{status}] {s['name']} ({s['strategy_type']}) — {s['ticker']} "
                    f"${s['amount_usd']:.2f} | {next_check} | {s['executions_count']} executions"
                )
            return ToolResult(output="\n".join(lines), success=True)

        elif action == "create_dca":
            name = kwargs.get("name", "")
            ticker = kwargs.get("ticker", "")
            amount = float(kwargs.get("amount", 0))
            freq = kwargs.get("frequency", "daily")
            account = kwargs.get("account", "coinbase")

            if not name or not ticker or not amount:
                return ToolResult(output="", success=False, error="name, ticker, and amount required")

            strat = dca_strategy(name, ticker, amount, freq, account)
            scheduler.add_strategy(strat)
            return ToolResult(
                output=f"DCA strategy created: {name}\n{strat.description}\nRunning autonomously.",
                success=True,
            )

        elif action == "create_threshold":
            name = kwargs.get("name", "")
            ticker = kwargs.get("ticker", "")
            buy_below = float(kwargs.get("buy_below", 0))
            sell_above = float(kwargs.get("sell_above", 0))
            amount = float(kwargs.get("amount", 0))
            account = kwargs.get("account", "coinbase")

            if not name or not ticker:
                return ToolResult(output="", success=False, error="name and ticker required")

            strat = threshold_strategy(name, ticker, buy_below, sell_above, amount, account)
            scheduler.add_strategy(strat)
            return ToolResult(
                output=f"Threshold strategy created: {name}\n{strat.description}\nMonitoring...",
                success=True,
            )

        elif action in ("enable", "disable"):
            name = kwargs.get("name", "")
            if not name:
                return ToolResult(output="", success=False, error="name required")
            ok = scheduler.toggle_strategy(name, action == "enable")
            return ToolResult(
                output=f"Strategy '{name}' {'enabled' if action == 'enable' else 'disabled'}",
                success=ok,
            )

        elif action == "remove":
            name = kwargs.get("name", "")
            if not name:
                return ToolResult(output="", success=False, error="name required")
            ok = scheduler.remove_strategy(name)
            return ToolResult(
                output=f"Strategy '{name}' removed" if ok else f"Strategy '{name}' not found",
                success=ok,
            )

        return ToolResult(output="", success=False, error=f"Unknown action: {action}")


class EarnTool(BaseTool):
    """Automate Coinbase Earn — watch videos, answer quizzes, claim free crypto."""

    @property
    def name(self) -> str:
        return "earn"

    @property
    def description(self) -> str:
        return (
            "Run Coinbase Earn automation — opens a browser, finds available "
            "learn & earn campaigns, watches videos, answers quizzes, and claims "
            "free crypto rewards. This is Money Maker's bootstrap tool for earning "
            "seed capital from zero."
        )

    @property
    def parameters(self) -> list[ToolParameter]:
        return [
            ToolParameter("action", "string", "Action: run (do all campaigns) or check (count available)", required=True),
        ]

    async def execute(self, **kwargs: Any) -> ToolResult:
        action = kwargs.get("action", "check")

        if action == "check":
            from agentic_hub.core.trading.earner import CoinbaseEarner
            earner = CoinbaseEarner()
            count = await earner.check_available()
            if count < 0:
                return ToolResult(output="Could not check — browser error", success=False, error="Browser failed")
            return ToolResult(output=f"{count} Coinbase Earn campaigns available", success=True)

        elif action == "run":
            from agentic_hub.core.trading.earner import run_coinbase_earn
            results = await run_coinbase_earn()
            if results:
                lines = [f"Completed {len(results)} campaigns:"]
                for r in results:
                    lines.append(f"  {r.get('status','?')}: {r.get('campaign','?')}")
                return ToolResult(output="\n".join(lines), success=True)
            return ToolResult(output="No campaigns completed — may need to log in first", success=True)

        return ToolResult(output="", success=False, error="action must be 'run' or 'check'")
