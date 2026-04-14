"""Trade Executor — the Money Maker's hands.

Every trade flows through here:
  1. Money Maker proposes a trade (TradeRequest)
  2. RiskGuardrails.check() validates it
  3. If first strategy: requires user approval via HITL
  4. If approved: routes to correct broker (Coinbase/Webull)
  5. Logs everything to portfolio tracker

The executor NEVER bypasses risk guardrails. Period.
"""
from __future__ import annotations

import asyncio
import json
import logging
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from agentic_hub.core.trading.risk import (
    RiskGuardrails, TradeRequest, GuardrailResult, get_risk_engine,
)

logger = logging.getLogger(__name__)

DATA_DIR = Path(__file__).parent.parent.parent.parent.parent / "data"
TRADE_LOG = DATA_DIR / "trade_log.jsonl"


@dataclass
class TradeResult:
    """Result of an executed trade."""
    success: bool
    trade: TradeRequest
    guardrail_result: GuardrailResult
    broker_response: dict = field(default_factory=dict)
    error: str = ""
    timestamp: float = 0.0

    def __post_init__(self):
        if not self.timestamp:
            self.timestamp = time.time()


class TradeExecutor:
    """Routes trades through risk checks to the correct broker."""

    def __init__(self):
        self._risk = get_risk_engine()
        self._first_strategy_approved = False
        self._approved_strategies: set[str] = set()
        self._portfolio_cache: dict[str, float] = {}
        self._load_approved_strategies()

    def _load_approved_strategies(self):
        """Load previously approved strategies from disk."""
        path = DATA_DIR / "approved_strategies.json"
        if path.exists():
            try:
                self._approved_strategies = set(json.loads(path.read_text()))
                self._first_strategy_approved = len(self._approved_strategies) > 0
            except Exception:
                pass

    def _save_approved_strategies(self):
        """Persist approved strategies."""
        path = DATA_DIR / "approved_strategies.json"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(list(self._approved_strategies)))

    async def execute(
        self,
        trade: TradeRequest,
        portfolio_value: float = 0,
        positions: dict[str, float] | None = None,
        require_approval: bool = False,
    ) -> TradeResult:
        """Execute a trade with full risk checks.

        Args:
            trade: The proposed trade
            portfolio_value: Total portfolio value
            positions: Current positions {ticker: value}
            require_approval: Force HITL approval regardless of strategy
        """
        # Step 1: Risk check (non-negotiable)
        guardrail = self._risk.check(trade, portfolio_value, positions)

        if not guardrail.approved:
            return TradeResult(
                success=False,
                trade=trade,
                guardrail_result=guardrail,
                error=f"Risk violation: {'; '.join(guardrail.violations)}",
            )

        # Step 2: Strategy approval check
        needs_approval = require_approval or (
            trade.strategy not in self._approved_strategies
        )

        if needs_approval:
            approved = await self._request_approval(trade, guardrail)
            if not approved:
                return TradeResult(
                    success=False,
                    trade=trade,
                    guardrail_result=guardrail,
                    error="Trade rejected by user",
                )
            self._approved_strategies.add(trade.strategy)
            self._save_approved_strategies()

        # Step 3: Route to broker
        try:
            broker_response = await self._route_to_broker(trade)
        except Exception as e:
            return TradeResult(
                success=False,
                trade=trade,
                guardrail_result=guardrail,
                error=f"Broker error: {e}",
            )

        if "error" in broker_response:
            return TradeResult(
                success=False,
                trade=trade,
                guardrail_result=guardrail,
                broker_response=broker_response,
                error=broker_response["error"],
            )

        # Step 4: Record trade
        self._risk.record_trade(trade)
        self._log_trade(trade, broker_response)

        # Step 5: Log to portfolio tracker
        try:
            from agentic_hub.core.portfolio import log_trade
            log_trade(
                trade.account, trade.action, trade.ticker,
                trade.quantity, trade.price, trade.reason,
            )
        except Exception:
            pass

        return TradeResult(
            success=True,
            trade=trade,
            guardrail_result=guardrail,
            broker_response=broker_response,
        )

    async def _request_approval(
        self, trade: TradeRequest, guardrail: GuardrailResult
    ) -> bool:
        """Request user approval via HITL system."""
        try:
            from agentic_hub.core.hitl import get_hitl_manager, HITLType

            hitl = get_hitl_manager()
            warnings = "\n".join(f"⚠️ {w}" for w in guardrail.warnings)

            request = hitl.create_request(
                hitl_type=HITLType.APPROVAL,
                prompt=(
                    f"💰 **Trade Approval Required**\n\n"
                    f"**{trade.action.upper()}** {trade.quantity} {trade.ticker} "
                    f"@ ${trade.price:.2f} ({trade.order_type})\n"
                    f"Total: ${trade.total_value:.2f}\n"
                    f"Account: {trade.account}\n"
                    f"Strategy: {trade.strategy}\n"
                    f"Reason: {trade.reason}\n"
                    f"{warnings}"
                ),
                agent="money_maker",
                timeout=300,
                default="reject",
            )

            response = await hitl.request_input(request)
            return response.action == "approve"

        except Exception as e:
            logger.warning(f"HITL approval failed, defaulting to reject: {e}")
            return False

    async def _route_to_broker(self, trade: TradeRequest) -> dict:
        """Route trade to the correct broker."""
        if trade.account == "coinbase":
            return await self._execute_coinbase(trade)
        elif trade.account in ("webull_brokerage", "roth_ira"):
            return await self._execute_webull(trade)
        else:
            return {"error": f"Unknown account: {trade.account}"}

    async def _execute_coinbase(self, trade: TradeRequest) -> dict:
        """Execute on Coinbase."""
        from agentic_hub.core.trading.coinbase_client import get_coinbase
        cb = get_coinbase()

        # Convert ticker to Coinbase product_id format
        product_id = f"{trade.ticker}-USD"

        if trade.action == "buy":
            return cb.buy(
                product_id=product_id,
                amount_usd=trade.total_value if trade.order_type == "market" else None,
                quantity=trade.quantity if trade.order_type == "limit" else None,
                order_type=trade.order_type,
                limit_price=trade.price if trade.order_type == "limit" else None,
            )
        elif trade.action == "sell":
            return cb.sell(
                product_id=product_id,
                quantity=trade.quantity,
                order_type=trade.order_type,
                limit_price=trade.price if trade.order_type == "limit" else None,
            )
        return {"error": f"Unsupported action: {trade.action}"}

    async def _execute_webull(self, trade: TradeRequest) -> dict:
        """Execute on Webull."""
        from agentic_hub.core.trading.webull_client import get_webull
        wb = get_webull()

        accounts = await wb.get_accounts()
        if not accounts:
            return {"error": "No Webull accounts found"}

        # Find the right account
        target = accounts[0]
        for acct in accounts:
            if trade.account == "roth_ira" and "IRA" in acct.get("type", "").upper():
                target = acct
                break
            elif trade.account == "webull_brokerage" and "IRA" not in acct.get("type", "").upper():
                target = acct
                break

        account_id = target["account_id"]
        order_type = trade.order_type.upper()

        if trade.action == "buy":
            return await wb.buy(
                account_id=account_id,
                symbol=trade.ticker,
                quantity=int(trade.quantity),
                order_type=order_type,
                price=trade.price if order_type == "LIMIT" else None,
            )
        elif trade.action == "sell":
            return await wb.sell(
                account_id=account_id,
                symbol=trade.ticker,
                quantity=int(trade.quantity),
                order_type=order_type,
                price=trade.price if order_type == "LIMIT" else None,
            )
        return {"error": f"Unsupported action: {trade.action}"}

    def _log_trade(self, trade: TradeRequest, response: dict):
        """Append trade to JSONL log."""
        TRADE_LOG.parent.mkdir(parents=True, exist_ok=True)
        entry = {
            "timestamp": time.time(),
            "account": trade.account,
            "action": trade.action,
            "ticker": trade.ticker,
            "quantity": trade.quantity,
            "price": trade.price,
            "total": trade.total_value,
            "order_type": trade.order_type,
            "strategy": trade.strategy,
            "reason": trade.reason,
            "broker_response": response,
        }
        with open(TRADE_LOG, "a") as f:
            f.write(json.dumps(entry) + "\n")

    def get_trade_history(self, limit: int = 50) -> list[dict]:
        """Get recent trades from the log."""
        if not TRADE_LOG.exists():
            return []
        trades = []
        for line in TRADE_LOG.read_text().strip().split("\n"):
            if line:
                try:
                    trades.append(json.loads(line))
                except Exception:
                    pass
        return trades[-limit:]

    def get_status(self) -> dict:
        """Get executor status."""
        return {
            "risk": self._risk.get_status(),
            "approved_strategies": list(self._approved_strategies),
            "trade_count": len(self.get_trade_history(1000)),
        }


# Singleton
_executor: TradeExecutor | None = None


def get_executor() -> TradeExecutor:
    global _executor
    if _executor is None:
        _executor = TradeExecutor()
    return _executor
