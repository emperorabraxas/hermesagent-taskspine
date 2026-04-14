"""Plaid tools for Money Maker + Scholar — full financial data access.

21 tools covering every PlaidManager method. No dead code.

Read-only tools (money_maker + scholar):
  bank_accounts, transactions, investments, liabilities, statements,
  institutions, network_status, enrich

Mutating tools (money_maker only):
  transfer, transfer_recurring, transfer_refund, identity,
  identity_verification, assets, income, signal, beacon,
  item_management, link, sandbox, webhook_verify
"""
from __future__ import annotations

import json
import logging
from typing import Any

from agentic_hub.core.tools.base import BaseTool, ToolParameter, ToolResult

logger = logging.getLogger(__name__)


def _get_mgr():
    from agentic_hub.core.plaid_client import get_plaid_manager
    return get_plaid_manager()


def _check_configured() -> ToolResult | None:
    if not _get_mgr().is_configured:
        return ToolResult(output="Plaid not configured. Set PLAID_CLIENT_ID and PLAID_SECRET.", success=False, error="Not configured")
    return None


def _get_vault():
    from agentic_hub.core.secrets import get_vault
    return get_vault()


def _iter_tokens():
    """Yield (key, token) for all linked institutions."""
    return _get_mgr()._iter_access_tokens()


# ══════════════════════════════════════════════════════════════════
# 1. ACCOUNTS (read-only)
# ══════════════════════════════════════════════════════════════════

class PlaidAccountsTool(BaseTool):
    """View linked bank accounts and balances."""

    @property
    def name(self) -> str:
        return "bank_accounts"

    @property
    def description(self) -> str:
        return (
            "View linked bank accounts. Actions: "
            "'summary' (default) — balances across all institutions, "
            "'detail' — full account info with routing/account numbers, "
            "'balances' — real-time balance refresh."
        )

    @property
    def parameters(self) -> list[ToolParameter]:
        return [
            ToolParameter("action", "string", "summary | detail | balances", required=False, default="summary",
                          enum=["summary", "detail", "balances"]),
        ]

    async def execute(self, **kwargs: Any) -> ToolResult:
        err = _check_configured()
        if err:
            return err
        try:
            mgr = _get_mgr()
            action = kwargs.get("action", "summary")

            if action == "detail":
                all_data = []
                for _, token in _iter_tokens():
                    try:
                        all_data.extend(mgr.get_auth(token))
                    except Exception:
                        all_data.extend(mgr.get_accounts(token))
                if not all_data:
                    return ToolResult(output="No linked accounts.", success=True)
                return ToolResult(output=json.dumps(all_data, indent=2), success=True)

            elif action == "balances":
                all_data = []
                for _, token in _iter_tokens():
                    try:
                        all_data.extend(mgr.get_balances(token))
                    except Exception as e:
                        logger.warning(f"Balance fetch failed: {e}")
                if not all_data:
                    return ToolResult(output="No linked accounts.", success=True)
                lines = ["REAL-TIME BALANCES:"]
                total = 0
                for a in all_data:
                    bal = a.get("current", 0)
                    total += bal
                    avail = a.get("available")
                    avail_str = f" (available: ${avail:,.2f})" if avail is not None else ""
                    lines.append(f"  {a['name']} ({a['type']}): ${bal:,.2f}{avail_str}")
                lines.append(f"\nTOTAL: ${total:,.2f}")
                return ToolResult(output="\n".join(lines), success=True)

            else:  # summary
                accounts = mgr.get_all_accounts_summary()
                if not accounts:
                    return ToolResult(output="No linked accounts. Connect via Plaid Link.", success=True)
                lines = ["LINKED ACCOUNTS:"]
                total = 0
                for a in accounts:
                    bal = a.get("current", 0)
                    total += bal
                    avail = a.get("available")
                    avail_str = f" (available: ${avail:,.2f})" if avail is not None else ""
                    lines.append(f"  {a['name']} ({a['type']}): ${bal:,.2f}{avail_str}")
                lines.append(f"\nTOTAL: ${total:,.2f}")
                return ToolResult(output="\n".join(lines), success=True)

        except Exception as e:
            return ToolResult(output="", success=False, error=f"Bank accounts error: {e}")


# ══════════════════════════════════════════════════════════════════
# 2. TRANSACTIONS (read-only)
# ══════════════════════════════════════════════════════════════════

class PlaidTransactionsTool(BaseTool):
    """Search and analyze transaction history."""

    @property
    def name(self) -> str:
        return "transactions"

    @property
    def description(self) -> str:
        return (
            "Get transaction data. Actions: "
            "'history' (default) — transaction list for date range, "
            "'recurring' — subscriptions/bills/income streams, "
            "'sync' — incremental updates via cursor, "
            "'refresh' — trigger real-time transaction refresh, "
            "'categories' — list Plaid's category taxonomy."
        )

    @property
    def parameters(self) -> list[ToolParameter]:
        return [
            ToolParameter("action", "string", "history | recurring | sync | refresh | categories",
                          required=False, default="history",
                          enum=["history", "recurring", "sync", "refresh", "categories"]),
            ToolParameter("days", "integer", "Days of history (default: 30, max: 730)", required=False),
            ToolParameter("cursor", "string", "Sync cursor from previous sync call", required=False),
        ]

    async def execute(self, **kwargs: Any) -> ToolResult:
        err = _check_configured()
        if err:
            return err
        try:
            mgr = _get_mgr()
            action = kwargs.get("action", "history")

            if action == "categories":
                cats = mgr.get_categories()
                return ToolResult(output=json.dumps(cats[:50], indent=2), success=True)

            if action == "refresh":
                for _, token in _iter_tokens():
                    mgr.refresh_transactions(token)
                return ToolResult(output="Transaction refresh initiated for all linked institutions.", success=True)

            if action == "sync":
                cursor = kwargs.get("cursor", "")
                results = []
                for _, token in _iter_tokens():
                    data = mgr.sync_transactions(token, cursor)
                    results.append(data)
                return ToolResult(output=json.dumps(results, indent=2), success=True)

            if action == "recurring":
                for _, token in _iter_tokens():
                    data = mgr.get_recurring_transactions(token)
                    lines = ["RECURRING INFLOWS (income):"]
                    for s in data.get("inflow", []):
                        lines.append(f"  ${s['amount']:,.2f} {s['frequency']} — {s['description']}")
                    lines.append("\nRECURRING OUTFLOWS (bills/subscriptions):")
                    for s in data.get("outflow", []):
                        lines.append(f"  ${s['amount']:,.2f} {s['frequency']} — {s['description']}")
                    return ToolResult(output="\n".join(lines), success=True)
                return ToolResult(output="No linked accounts.", success=True)

            # history (default)
            days = int(kwargs.get("days", 30))
            from datetime import date, timedelta
            start = str(date.today() - timedelta(days=days))
            end = str(date.today())
            all_data = []
            for _, token in _iter_tokens():
                try:
                    all_data.extend(mgr.get_transactions(token, start, end))
                except Exception as e:
                    logger.warning(f"Transaction fetch failed: {e}")

            if not all_data:
                return ToolResult(output="No transactions found.", success=True)

            all_data.sort(key=lambda t: t["date"], reverse=True)
            lines = [f"TRANSACTIONS (last {days} days): {len(all_data)} total"]
            for t in all_data[:50]:
                sign = "-" if t["amount"] > 0 else "+"
                lines.append(f"  {t['date']} {sign}${abs(t['amount']):,.2f} {t['name']}")
            if len(all_data) > 50:
                lines.append(f"  ... and {len(all_data) - 50} more")
            return ToolResult(output="\n".join(lines), success=True)

        except Exception as e:
            return ToolResult(output="", success=False, error=f"Transactions error: {e}")


# ══════════════════════════════════════════════════════════════════
# 3. INVESTMENTS (read-only)
# ══════════════════════════════════════════════════════════════════

class PlaidInvestmentsTool(BaseTool):
    """View investment holdings and portfolio."""

    @property
    def name(self) -> str:
        return "investments"

    @property
    def description(self) -> str:
        return (
            "View investment data. Actions: "
            "'holdings' (default) — current positions with value/cost basis, "
            "'transactions' — recent buys/sells/dividends, "
            "'refresh' — trigger real-time investment data refresh."
        )

    @property
    def parameters(self) -> list[ToolParameter]:
        return [
            ToolParameter("action", "string", "holdings | transactions | refresh",
                          required=False, default="holdings",
                          enum=["holdings", "transactions", "refresh"]),
        ]

    async def execute(self, **kwargs: Any) -> ToolResult:
        err = _check_configured()
        if err:
            return err
        try:
            mgr = _get_mgr()
            action = kwargs.get("action", "holdings")

            if action == "refresh":
                for _, token in _iter_tokens():
                    mgr.refresh_investments(token)
                return ToolResult(output="Investment refresh initiated.", success=True)

            if action == "transactions":
                all_txns = []
                for _, token in _iter_tokens():
                    try:
                        all_txns.extend(mgr.get_investment_transactions(token))
                    except Exception as e:
                        logger.warning(f"Investment txn fetch failed: {e}")
                if not all_txns:
                    return ToolResult(output="No investment transactions found.", success=True)
                lines = [f"INVESTMENT TRANSACTIONS: {len(all_txns)}"]
                for t in all_txns[:30]:
                    lines.append(f"  {t['date']} {t['type']} {t['ticker']} {t['quantity']} @ ${t['price']:,.2f}")
                return ToolResult(output="\n".join(lines), success=True)

            # holdings (default)
            all_holdings = []
            for _, token in _iter_tokens():
                try:
                    all_holdings.extend(mgr.get_holdings(token))
                except Exception as e:
                    logger.warning(f"Holdings fetch failed: {e}")

            if not all_holdings:
                return ToolResult(output="No investment holdings found.", success=True)

            lines = [f"HOLDINGS: {len(all_holdings)} positions"]
            total_value = 0
            for h in sorted(all_holdings, key=lambda x: -x["value"]):
                total_value += h["value"]
                cost = f" (cost: ${h['cost_basis']:,.2f})" if h.get("cost_basis") else ""
                lines.append(f"  {h['ticker'] or h['name']}: {h['quantity']:.4f} @ ${h['price']:,.2f} = ${h['value']:,.2f}{cost}")
            lines.append(f"\nTOTAL PORTFOLIO: ${total_value:,.2f}")
            return ToolResult(output="\n".join(lines), success=True)

        except Exception as e:
            return ToolResult(output="", success=False, error=f"Investments error: {e}")


# ══════════════════════════════════════════════════════════════════
# 4. TRANSFER
# ══════════════════════════════════════════════════════════════════

class PlaidTransferTool(BaseTool):
    """ACH transfers — create, track, manage."""

    @property
    def name(self) -> str:
        return "transfer"

    @property
    def description(self) -> str:
        return (
            "ACH money movement. Actions: "
            "'create' — initiate transfer (requires account_id + amount), "
            "'get' — details of a specific transfer, "
            "'list' — list transfers, "
            "'cancel' — cancel pending transfer, "
            "'events' — transfer event log, "
            "'sweeps' — list sweeps, "
            "'capabilities' — check RTP eligibility, "
            "'ledger' — view Plaid ledger balance, "
            "'ledger_deposit' — deposit into ledger, "
            "'ledger_withdraw' — withdraw from ledger, "
            "'metrics' — transfer usage metrics, "
            "'config' — transfer configuration, "
            "'event_sync' — sync events by cursor."
        )

    @property
    def parameters(self) -> list[ToolParameter]:
        return [
            ToolParameter("action", "string", "create | get | list | cancel | events | event_sync | sweeps | sweep_get | capabilities | ledger | ledger_deposit | ledger_withdraw | metrics | config",
                          required=True, enum=["create", "get", "list", "cancel", "events", "event_sync", "sweeps", "sweep_get", "capabilities", "ledger", "ledger_deposit", "ledger_withdraw", "metrics", "config"]),
            ToolParameter("account_id", "string", "Plaid account ID (for create/capabilities)", required=False),
            ToolParameter("amount", "string", "Dollar amount e.g. '100.00' (for create)", required=False),
            ToolParameter("transfer_id", "string", "Transfer ID (for get/cancel)", required=False),
            ToolParameter("type", "string", "debit (pull) or credit (push)", required=False),
            ToolParameter("description", "string", "Transfer description", required=False),
        ]

    async def execute(self, **kwargs: Any) -> ToolResult:
        err = _check_configured()
        if err:
            return err
        try:
            mgr = _get_mgr()
            action = kwargs["action"]

            if action == "create":
                account_id = kwargs.get("account_id", "")
                amount = kwargs.get("amount", "")
                if not account_id or not amount:
                    return ToolResult(output="", success=False, error="account_id and amount required")
                transfer_type = kwargs.get("type", "debit")
                description = kwargs.get("description", "spider.Web transfer")
                # Find access token for this account
                for _, token in _iter_tokens():
                    accounts = mgr.get_accounts(token)
                    if any(a["id"] == account_id for a in accounts):
                        result = mgr.create_transfer(token, account_id, amount, transfer_type, description)
                        return ToolResult(output=json.dumps(result, indent=2), success=result.get("status") == "ok",
                                          error=result.get("message") if result.get("status") != "ok" else None)
                return ToolResult(output="", success=False, error=f"Account {account_id} not found")

            elif action == "get":
                tid = kwargs.get("transfer_id", "")
                if not tid:
                    return ToolResult(output="", success=False, error="transfer_id required")
                return ToolResult(output=json.dumps(mgr.get_transfer(tid), indent=2), success=True)

            elif action == "list":
                return ToolResult(output=json.dumps(mgr.list_transfers(), indent=2), success=True)

            elif action == "cancel":
                tid = kwargs.get("transfer_id", "")
                if not tid:
                    return ToolResult(output="", success=False, error="transfer_id required")
                return ToolResult(output=json.dumps(mgr.cancel_transfer(tid), indent=2), success=True)

            elif action == "events":
                return ToolResult(output=json.dumps(mgr.get_transfer_events(), indent=2), success=True)

            elif action == "sweeps":
                return ToolResult(output=json.dumps(mgr.list_transfer_sweeps(), indent=2), success=True)

            elif action == "sweep_get":
                sid = kwargs.get("transfer_id", "")  # reuse transfer_id param for sweep_id
                if not sid:
                    return ToolResult(output="", success=False, error="transfer_id (sweep_id) required")
                return ToolResult(output=json.dumps(mgr.get_transfer_sweep(sid), indent=2), success=True)

            elif action == "event_sync":
                return ToolResult(output=json.dumps(mgr.sync_transfer_events(), indent=2), success=True)

            elif action == "capabilities":
                account_id = kwargs.get("account_id", "")
                if not account_id:
                    return ToolResult(output="", success=False, error="account_id required")
                for _, token in _iter_tokens():
                    accounts = mgr.get_accounts(token)
                    if any(a["id"] == account_id for a in accounts):
                        return ToolResult(output=json.dumps(mgr.get_transfer_capabilities(token, account_id), indent=2), success=True)
                return ToolResult(output="", success=False, error=f"Account {account_id} not found")

            elif action == "ledger":
                return ToolResult(output=json.dumps(mgr.get_ledger(), indent=2), success=True)

            elif action == "ledger_deposit":
                amount = kwargs.get("amount", "")
                if not amount:
                    return ToolResult(output="", success=False, error="amount required")
                return ToolResult(output=json.dumps(mgr.deposit_ledger(amount, kwargs.get("description", "")), indent=2), success=True)

            elif action == "ledger_withdraw":
                amount = kwargs.get("amount", "")
                if not amount:
                    return ToolResult(output="", success=False, error="amount required")
                return ToolResult(output=json.dumps(mgr.withdraw_ledger(amount, kwargs.get("description", "")), indent=2), success=True)

            elif action == "metrics":
                return ToolResult(output=json.dumps(mgr.get_transfer_metrics(), indent=2), success=True)

            elif action == "config":
                return ToolResult(output=json.dumps(mgr.get_transfer_config(), indent=2), success=True)

            return ToolResult(output="", success=False, error=f"Unknown action: {action}")
        except Exception as e:
            return ToolResult(output="", success=False, error=f"Transfer error: {e}")


# ══════════════════════════════════════════════════════════════════
# 5. TRANSFER RECURRING
# ══════════════════════════════════════════════════════════════════

class PlaidTransferRecurringTool(BaseTool):
    """Manage recurring ACH transfers."""

    @property
    def name(self) -> str:
        return "transfer_recurring"

    @property
    def description(self) -> str:
        return "Manage recurring transfers. Actions: create, get, list, cancel."

    @property
    def parameters(self) -> list[ToolParameter]:
        return [
            ToolParameter("action", "string", "create | get | list | cancel", required=True,
                          enum=["create", "get", "list", "cancel"]),
            ToolParameter("account_id", "string", "Account ID (for create)", required=False),
            ToolParameter("amount", "string", "Dollar amount (for create)", required=False),
            ToolParameter("interval_unit", "string", "week | month (for create)", required=False),
            ToolParameter("interval_count", "integer", "Every N units (for create)", required=False),
            ToolParameter("start_date", "string", "YYYY-MM-DD start (for create)", required=False),
            ToolParameter("recurring_transfer_id", "string", "ID (for get/cancel)", required=False),
        ]

    async def execute(self, **kwargs: Any) -> ToolResult:
        err = _check_configured()
        if err:
            return err
        try:
            mgr = _get_mgr()
            action = kwargs["action"]

            if action == "create":
                account_id = kwargs.get("account_id", "")
                amount = kwargs.get("amount", "")
                start_date = kwargs.get("start_date", "")
                if not account_id or not amount or not start_date:
                    return ToolResult(output="", success=False, error="account_id, amount, and start_date required")
                schedule = {
                    "interval_unit": kwargs.get("interval_unit", "month"),
                    "interval_count": int(kwargs.get("interval_count", 1)),
                    "start_date": start_date,
                }
                for _, token in _iter_tokens():
                    accounts = mgr.get_accounts(token)
                    if any(a["id"] == account_id for a in accounts):
                        result = mgr.create_recurring_transfer(token, account_id, amount, schedule)
                        return ToolResult(output=json.dumps(result, indent=2), success=True)
                return ToolResult(output="", success=False, error=f"Account {account_id} not found")

            elif action == "get":
                rid = kwargs.get("recurring_transfer_id", "")
                if not rid:
                    return ToolResult(output="", success=False, error="recurring_transfer_id required")
                return ToolResult(output=json.dumps(mgr.get_recurring_transfer(rid), indent=2), success=True)

            elif action == "list":
                return ToolResult(output=json.dumps(mgr.list_recurring_transfers(), indent=2), success=True)

            elif action == "cancel":
                rid = kwargs.get("recurring_transfer_id", "")
                if not rid:
                    return ToolResult(output="", success=False, error="recurring_transfer_id required")
                return ToolResult(output=json.dumps(mgr.cancel_recurring_transfer(rid), indent=2), success=True)

            return ToolResult(output="", success=False, error=f"Unknown action: {action}")
        except Exception as e:
            return ToolResult(output="", success=False, error=f"Recurring transfer error: {e}")


# ══════════════════════════════════════════════════════════════════
# 6. TRANSFER REFUND
# ══════════════════════════════════════════════════════════════════

class PlaidTransferRefundTool(BaseTool):
    """Manage transfer refunds."""

    @property
    def name(self) -> str:
        return "transfer_refund"

    @property
    def description(self) -> str:
        return "Manage refunds for completed transfers. Actions: create, get, cancel."

    @property
    def parameters(self) -> list[ToolParameter]:
        return [
            ToolParameter("action", "string", "create | get | cancel", required=True, enum=["create", "get", "cancel"]),
            ToolParameter("transfer_id", "string", "Transfer to refund (for create)", required=False),
            ToolParameter("refund_id", "string", "Refund ID (for get/cancel)", required=False),
            ToolParameter("amount", "string", "Refund amount (for create)", required=False),
        ]

    async def execute(self, **kwargs: Any) -> ToolResult:
        err = _check_configured()
        if err:
            return err
        try:
            mgr = _get_mgr()
            action = kwargs["action"]

            if action == "create":
                tid = kwargs.get("transfer_id", "")
                amount = kwargs.get("amount", "")
                if not tid or not amount:
                    return ToolResult(output="", success=False, error="transfer_id and amount required")
                return ToolResult(output=json.dumps(mgr.create_transfer_refund(tid, amount), indent=2), success=True)
            elif action == "get":
                rid = kwargs.get("refund_id", "")
                if not rid:
                    return ToolResult(output="", success=False, error="refund_id required")
                return ToolResult(output=json.dumps(mgr.get_transfer_refund(rid), indent=2), success=True)
            elif action == "cancel":
                rid = kwargs.get("refund_id", "")
                if not rid:
                    return ToolResult(output="", success=False, error="refund_id required")
                return ToolResult(output=json.dumps(mgr.cancel_transfer_refund(rid), indent=2), success=True)

            return ToolResult(output="", success=False, error=f"Unknown action: {action}")
        except Exception as e:
            return ToolResult(output="", success=False, error=f"Refund error: {e}")


# ══════════════════════════════════════════════════════════════════
# 7. IDENTITY
# ══════════════════════════════════════════════════════════════════

class PlaidIdentityTool(BaseTool):
    """Access bank-verified identity data."""

    @property
    def name(self) -> str:
        return "identity"

    @property
    def description(self) -> str:
        return "Bank-verified identity. Actions: 'get' — names/emails/phones/addresses, 'match' — verify user data against bank records."

    @property
    def parameters(self) -> list[ToolParameter]:
        return [
            ToolParameter("action", "string", "get | match", required=True, enum=["get", "match"]),
            ToolParameter("legal_name", "string", "Name to verify (for match)", required=False),
            ToolParameter("email", "string", "Email to verify (for match)", required=False),
            ToolParameter("phone", "string", "Phone to verify (for match)", required=False),
        ]

    async def execute(self, **kwargs: Any) -> ToolResult:
        err = _check_configured()
        if err:
            return err
        try:
            mgr = _get_mgr()
            action = kwargs["action"]

            if action == "get":
                all_ids = []
                for _, token in _iter_tokens():
                    try:
                        all_ids.extend(mgr.get_identity(token))
                    except Exception as e:
                        logger.warning(f"Identity fetch failed: {e}")
                return ToolResult(output=json.dumps(all_ids, indent=2), success=True)

            elif action == "match":
                user_data = {k: kwargs[k] for k in ["legal_name", "email", "phone"] if kwargs.get(k)}
                if not user_data:
                    return ToolResult(output="", success=False, error="Provide at least one of: legal_name, email, phone")
                results = []
                for _, token in _iter_tokens():
                    try:
                        results.append(mgr.match_identity(token, user_data))
                    except Exception as e:
                        logger.warning(f"Identity match failed: {e}")
                return ToolResult(output=json.dumps(results, indent=2), success=True)

            return ToolResult(output="", success=False, error=f"Unknown action: {action}")
        except Exception as e:
            return ToolResult(output="", success=False, error=f"Identity error: {e}")


# ══════════════════════════════════════════════════════════════════
# 8. IDENTITY VERIFICATION (KYC)
# ══════════════════════════════════════════════════════════════════

class PlaidIdentityVerificationTool(BaseTool):
    """KYC identity verification flow."""

    @property
    def name(self) -> str:
        return "identity_verification"

    @property
    def description(self) -> str:
        return "KYC identity verification. Actions: create, get, list, retry."

    @property
    def parameters(self) -> list[ToolParameter]:
        return [
            ToolParameter("action", "string", "create | get | list | retry", required=True,
                          enum=["create", "get", "list", "retry"]),
            ToolParameter("template_id", "string", "Verification template ID", required=False),
            ToolParameter("identity_verification_id", "string", "Verification ID (for get)", required=False),
            ToolParameter("client_user_id", "string", "User ID (for create/retry/list)", required=False),
            ToolParameter("email", "string", "Email (for create)", required=False),
        ]

    async def execute(self, **kwargs: Any) -> ToolResult:
        err = _check_configured()
        if err:
            return err
        try:
            mgr = _get_mgr()
            action = kwargs["action"]

            if action == "create":
                tid = kwargs.get("template_id", "")
                if not tid:
                    return ToolResult(output="", success=False, error="template_id required")
                user_data = {"client_user_id": kwargs.get("client_user_id", "spider.bob"), "email": kwargs.get("email", "")}
                return ToolResult(output=json.dumps(mgr.create_identity_verification(tid, user_data), indent=2), success=True)
            elif action == "get":
                vid = kwargs.get("identity_verification_id", "")
                if not vid:
                    return ToolResult(output="", success=False, error="identity_verification_id required")
                return ToolResult(output=json.dumps(mgr.get_identity_verification(vid), indent=2), success=True)
            elif action == "list":
                tid = kwargs.get("template_id", "")
                if not tid:
                    return ToolResult(output="", success=False, error="template_id required")
                return ToolResult(output=json.dumps(mgr.list_identity_verifications(tid, kwargs.get("client_user_id", "")), indent=2), success=True)
            elif action == "retry":
                cuid = kwargs.get("client_user_id", "")
                tid = kwargs.get("template_id", "")
                if not cuid or not tid:
                    return ToolResult(output="", success=False, error="client_user_id and template_id required")
                return ToolResult(output=json.dumps(mgr.retry_identity_verification(cuid, tid), indent=2), success=True)

            return ToolResult(output="", success=False, error=f"Unknown action: {action}")
        except Exception as e:
            return ToolResult(output="", success=False, error=f"Identity verification error: {e}")


# ══════════════════════════════════════════════════════════════════
# 9. ASSETS
# ══════════════════════════════════════════════════════════════════

class PlaidAssetsTool(BaseTool):
    """Asset reports for net worth / underwriting."""

    @property
    def name(self) -> str:
        return "assets"

    @property
    def description(self) -> str:
        return "Asset reports. Actions: create, get, pdf, refresh, filter, remove, audit_create, audit_remove."

    @property
    def parameters(self) -> list[ToolParameter]:
        return [
            ToolParameter("action", "string", "create | get | pdf | refresh | filter | remove | audit_create | audit_remove",
                          required=True, enum=["create", "get", "pdf", "refresh", "filter", "remove", "audit_create", "audit_remove"]),
            ToolParameter("asset_report_token", "string", "Report token", required=False),
            ToolParameter("days", "integer", "Days of history (default: 90)", required=False),
            ToolParameter("account_ids", "string", "Comma-separated account IDs to exclude (for filter)", required=False),
            ToolParameter("auditor_id", "string", "Auditor ID (for audit_create)", required=False),
            ToolParameter("audit_copy_token", "string", "Audit copy token (for audit_remove)", required=False),
        ]

    async def execute(self, **kwargs: Any) -> ToolResult:
        err = _check_configured()
        if err:
            return err
        try:
            mgr = _get_mgr()
            action = kwargs["action"]

            if action == "create":
                tokens = [t for _, t in _iter_tokens()]
                if not tokens:
                    return ToolResult(output="", success=False, error="No linked accounts")
                days = int(kwargs.get("days", 90))
                return ToolResult(output=json.dumps(mgr.create_asset_report(tokens, days), indent=2), success=True)
            elif action == "get":
                token = kwargs.get("asset_report_token", "")
                if not token:
                    return ToolResult(output="", success=False, error="asset_report_token required")
                return ToolResult(output=json.dumps(mgr.get_asset_report(token), indent=2), success=True)
            elif action == "pdf":
                token = kwargs.get("asset_report_token", "")
                if not token:
                    return ToolResult(output="", success=False, error="asset_report_token required")
                result = mgr.get_asset_report_pdf(token)
                return ToolResult(output=f"PDF saved: {result['path']} ({result['size']} bytes)", success=True)
            elif action == "refresh":
                token = kwargs.get("asset_report_token", "")
                if not token:
                    return ToolResult(output="", success=False, error="asset_report_token required")
                return ToolResult(output=json.dumps(mgr.refresh_asset_report(token, int(kwargs.get("days", 90))), indent=2), success=True)
            elif action == "filter":
                token = kwargs.get("asset_report_token", "")
                ids_str = kwargs.get("account_ids", "")
                if not token or not ids_str:
                    return ToolResult(output="", success=False, error="asset_report_token and account_ids required")
                return ToolResult(output=json.dumps(mgr.filter_asset_report(token, ids_str.split(",")), indent=2), success=True)
            elif action == "remove":
                token = kwargs.get("asset_report_token", "")
                if not token:
                    return ToolResult(output="", success=False, error="asset_report_token required")
                removed = mgr.remove_asset_report(token)
                return ToolResult(output=f"Removed: {removed}", success=removed)
            elif action == "audit_create":
                token = kwargs.get("asset_report_token", "")
                auditor = kwargs.get("auditor_id", "")
                if not token or not auditor:
                    return ToolResult(output="", success=False, error="asset_report_token and auditor_id required")
                return ToolResult(output=json.dumps(mgr.create_audit_copy(token, auditor), indent=2), success=True)
            elif action == "audit_remove":
                act = kwargs.get("audit_copy_token", "")
                if not act:
                    return ToolResult(output="", success=False, error="audit_copy_token required")
                removed = mgr.remove_audit_copy(act)
                return ToolResult(output=f"Removed: {removed}", success=removed)

            return ToolResult(output="", success=False, error=f"Unknown action: {action}")
        except Exception as e:
            return ToolResult(output="", success=False, error=f"Assets error: {e}")


# ══════════════════════════════════════════════════════════════════
# 10. INCOME
# ══════════════════════════════════════════════════════════════════

class PlaidIncomeTool(BaseTool):
    """Income verification and employment data."""

    @property
    def name(self) -> str:
        return "income"

    @property
    def description(self) -> str:
        return "Income data. Actions: bank (bank income analysis), bank_pdf, payroll, payroll_risk, employment, sessions."

    @property
    def parameters(self) -> list[ToolParameter]:
        return [
            ToolParameter("action", "string", "bank | bank_pdf | payroll | payroll_risk | employment | sessions",
                          required=True, enum=["bank", "bank_pdf", "payroll", "payroll_risk", "employment", "sessions"]),
        ]

    async def execute(self, **kwargs: Any) -> ToolResult:
        err = _check_configured()
        if err:
            return err
        try:
            mgr = _get_mgr()
            action = kwargs["action"]

            for _, token in _iter_tokens():
                if action == "bank":
                    return ToolResult(output=json.dumps(mgr.get_bank_income(token), indent=2), success=True)
                elif action == "bank_pdf":
                    result = mgr.get_bank_income_pdf(token)
                    return ToolResult(output=f"PDF saved: {result['path']} ({result['size']} bytes)", success=True)
                elif action == "payroll":
                    return ToolResult(output=json.dumps(mgr.get_payroll_income(token), indent=2), success=True)
                elif action == "payroll_risk":
                    return ToolResult(output=json.dumps(mgr.get_payroll_risk_signals(token), indent=2), success=True)
                elif action == "employment":
                    return ToolResult(output=json.dumps(mgr.get_employment(token), indent=2), success=True)
                elif action == "sessions":
                    return ToolResult(output=json.dumps(mgr.get_credit_sessions(token), indent=2), success=True)

            return ToolResult(output="No linked accounts.", success=False, error="No access tokens")
        except Exception as e:
            return ToolResult(output="", success=False, error=f"Income error: {e}")


# ══════════════════════════════════════════════════════════════════
# 11. SIGNAL (RISK SCORING)
# ══════════════════════════════════════════════════════════════════

class PlaidSignalTool(BaseTool):
    """ACH transaction risk scoring."""

    @property
    def name(self) -> str:
        return "signal"

    @property
    def description(self) -> str:
        return "ACH risk scoring. Actions: evaluate (score a transaction), decision (report initiation), return_report (report ACH return), prepare (enable Signal for an Item)."

    @property
    def parameters(self) -> list[ToolParameter]:
        return [
            ToolParameter("action", "string", "evaluate | decision | return_report | prepare", required=True,
                          enum=["evaluate", "decision", "return_report", "prepare"]),
            ToolParameter("account_id", "string", "Account ID (for evaluate)", required=False),
            ToolParameter("amount", "number", "Transaction amount (for evaluate)", required=False),
            ToolParameter("client_transaction_id", "string", "Your transaction ID (for decision/return_report)", required=False),
            ToolParameter("initiated", "boolean", "Did you initiate? (for decision)", required=False),
            ToolParameter("return_code", "string", "ACH return code (for return_report)", required=False),
        ]

    async def execute(self, **kwargs: Any) -> ToolResult:
        err = _check_configured()
        if err:
            return err
        try:
            mgr = _get_mgr()
            action = kwargs["action"]

            if action == "evaluate":
                account_id = kwargs.get("account_id", "")
                amount = float(kwargs.get("amount", 0))
                if not account_id or not amount:
                    return ToolResult(output="", success=False, error="account_id and amount required")
                for _, token in _iter_tokens():
                    accounts = mgr.get_accounts(token)
                    if any(a["id"] == account_id for a in accounts):
                        return ToolResult(output=json.dumps(mgr.evaluate_signal(token, account_id, amount), indent=2), success=True)
                return ToolResult(output="", success=False, error=f"Account {account_id} not found")

            elif action == "decision":
                ctid = kwargs.get("client_transaction_id", "")
                initiated = kwargs.get("initiated", True)
                if not ctid:
                    return ToolResult(output="", success=False, error="client_transaction_id required")
                return ToolResult(output=json.dumps(mgr.report_signal_decision("", ctid, initiated), indent=2), success=True)

            elif action == "return_report":
                ctid = kwargs.get("client_transaction_id", "")
                code = kwargs.get("return_code", "")
                if not ctid or not code:
                    return ToolResult(output="", success=False, error="client_transaction_id and return_code required")
                return ToolResult(output=json.dumps(mgr.report_signal_return("", ctid, code), indent=2), success=True)

            elif action == "prepare":
                for _, token in _iter_tokens():
                    mgr.prepare_signal(token)
                return ToolResult(output="Signal prepared for all linked items.", success=True)

            return ToolResult(output="", success=False, error=f"Unknown action: {action}")
        except Exception as e:
            return ToolResult(output="", success=False, error=f"Signal error: {e}")


# ══════════════════════════════════════════════════════════════════
# 12. LIABILITIES (read-only)
# ══════════════════════════════════════════════════════════════════

class PlaidLiabilitiesTool(BaseTool):
    """View credit card and loan liabilities."""

    @property
    def name(self) -> str:
        return "liabilities"

    @property
    def description(self) -> str:
        return "View credit card balances, APRs, minimums, and student loan details across all linked institutions."

    @property
    def parameters(self) -> list[ToolParameter]:
        return []

    async def execute(self, **kwargs: Any) -> ToolResult:
        err = _check_configured()
        if err:
            return err
        try:
            mgr = _get_mgr()
            all_data: dict[str, list] = {"credit": [], "student": []}
            for _, token in _iter_tokens():
                try:
                    data = mgr.get_liabilities(token)
                    all_data["credit"].extend(data.get("credit", []))
                    all_data["student"].extend(data.get("student", []))
                except Exception as e:
                    logger.warning(f"Liabilities fetch failed: {e}")

            if not all_data["credit"] and not all_data["student"]:
                return ToolResult(output="No liabilities found.", success=True)
            return ToolResult(output=json.dumps(all_data, indent=2), success=True)
        except Exception as e:
            return ToolResult(output="", success=False, error=f"Liabilities error: {e}")


# ══════════════════════════════════════════════════════════════════
# 13. STATEMENTS (read-only for scholar)
# ══════════════════════════════════════════════════════════════════

class PlaidStatementsTool(BaseTool):
    """Download bank statements."""

    @property
    def name(self) -> str:
        return "statements"

    @property
    def description(self) -> str:
        return "Bank statements. Actions: list (available statements), download (get PDF), refresh (trigger extraction)."

    @property
    def parameters(self) -> list[ToolParameter]:
        return [
            ToolParameter("action", "string", "list | download | refresh", required=True,
                          enum=["list", "download", "refresh"]),
            ToolParameter("statement_id", "string", "Statement ID (for download)", required=False),
        ]

    async def execute(self, **kwargs: Any) -> ToolResult:
        err = _check_configured()
        if err:
            return err
        try:
            mgr = _get_mgr()
            action = kwargs["action"]

            if action == "list":
                all_stmts = []
                for _, token in _iter_tokens():
                    try:
                        all_stmts.extend(mgr.list_statements(token))
                    except Exception as e:
                        logger.warning(f"Statements list failed: {e}")
                return ToolResult(output=json.dumps(all_stmts, indent=2), success=True)

            elif action == "download":
                sid = kwargs.get("statement_id", "")
                if not sid:
                    return ToolResult(output="", success=False, error="statement_id required")
                for _, token in _iter_tokens():
                    try:
                        result = mgr.download_statement(token, sid)
                        return ToolResult(output=f"PDF saved: {result['path']} ({result['size']} bytes)", success=True)
                    except Exception:
                        continue
                return ToolResult(output="", success=False, error=f"Statement {sid} not found")

            elif action == "refresh":
                for _, token in _iter_tokens():
                    mgr.refresh_statements(token)
                return ToolResult(output="Statement refresh initiated.", success=True)

            return ToolResult(output="", success=False, error=f"Unknown action: {action}")
        except Exception as e:
            return ToolResult(output="", success=False, error=f"Statements error: {e}")


# ══════════════════════════════════════════════════════════════════
# 14. BEACON (ANTI-FRAUD)
# ══════════════════════════════════════════════════════════════════

class PlaidBeaconTool(BaseTool):
    """Anti-fraud Beacon user and report management."""

    @property
    def name(self) -> str:
        return "beacon"

    @property
    def description(self) -> str:
        return "Fraud detection. Actions: create_user, get_user, update_user, create_report, get_report, list_reports, get_duplicate."

    @property
    def parameters(self) -> list[ToolParameter]:
        return [
            ToolParameter("action", "string", "create_user | get_user | update_user | create_report | get_report | list_reports | get_duplicate",
                          required=True, enum=["create_user", "get_user", "update_user", "create_report", "get_report", "list_reports", "get_duplicate"]),
            ToolParameter("program_id", "string", "Beacon program ID (for create_user)", required=False),
            ToolParameter("beacon_user_id", "string", "Beacon user ID", required=False),
            ToolParameter("beacon_report_id", "string", "Beacon report ID (for get_report)", required=False),
            ToolParameter("beacon_duplicate_id", "string", "Duplicate ID (for get_duplicate)", required=False),
            ToolParameter("first_name", "string", "First name (for create_user)", required=False),
            ToolParameter("last_name", "string", "Last name (for create_user)", required=False),
            ToolParameter("dob", "string", "Date of birth YYYY-MM-DD (for create_user)", required=False),
            ToolParameter("report_type", "string", "Report type (for create_report)", required=False),
            ToolParameter("fraud_date", "string", "Fraud date YYYY-MM-DD (for create_report)", required=False),
        ]

    async def execute(self, **kwargs: Any) -> ToolResult:
        err = _check_configured()
        if err:
            return err
        try:
            mgr = _get_mgr()
            action = kwargs["action"]

            if action == "create_user":
                pid = kwargs.get("program_id", "")
                if not pid:
                    return ToolResult(output="", success=False, error="program_id required")
                user_data = {k: kwargs[k] for k in ["first_name", "last_name", "dob", "email"] if kwargs.get(k)}
                return ToolResult(output=json.dumps(mgr.create_beacon_user(pid, user_data), indent=2), success=True)
            elif action == "get_user":
                buid = kwargs.get("beacon_user_id", "")
                if not buid:
                    return ToolResult(output="", success=False, error="beacon_user_id required")
                return ToolResult(output=json.dumps(mgr.get_beacon_user(buid), indent=2), success=True)
            elif action == "update_user":
                buid = kwargs.get("beacon_user_id", "")
                if not buid:
                    return ToolResult(output="", success=False, error="beacon_user_id required")
                return ToolResult(output=json.dumps(mgr.update_beacon_user(buid, {}), indent=2), success=True)
            elif action == "create_report":
                buid = kwargs.get("beacon_user_id", "")
                rtype = kwargs.get("report_type", "")
                fdate = kwargs.get("fraud_date", "")
                if not buid or not rtype or not fdate:
                    return ToolResult(output="", success=False, error="beacon_user_id, report_type, and fraud_date required")
                return ToolResult(output=json.dumps(mgr.create_beacon_report(buid, rtype, fdate), indent=2), success=True)
            elif action == "get_report":
                brid = kwargs.get("beacon_report_id", "")
                if not brid:
                    return ToolResult(output="", success=False, error="beacon_report_id required")
                return ToolResult(output=json.dumps(mgr.get_beacon_report(brid), indent=2), success=True)
            elif action == "list_reports":
                buid = kwargs.get("beacon_user_id", "")
                if not buid:
                    return ToolResult(output="", success=False, error="beacon_user_id required")
                return ToolResult(output=json.dumps(mgr.list_beacon_reports(buid), indent=2), success=True)
            elif action == "get_duplicate":
                did = kwargs.get("beacon_duplicate_id", "")
                if not did:
                    return ToolResult(output="", success=False, error="beacon_duplicate_id required")
                return ToolResult(output=json.dumps(mgr.get_beacon_duplicate(did), indent=2), success=True)

            return ToolResult(output="", success=False, error=f"Unknown action: {action}")
        except Exception as e:
            return ToolResult(output="", success=False, error=f"Beacon error: {e}")


# ══════════════════════════════════════════════════════════════════
# 15. INSTITUTIONS (read-only)
# ══════════════════════════════════════════════════════════════════

class PlaidInstitutionsTool(BaseTool):
    """Search and lookup financial institutions."""

    @property
    def name(self) -> str:
        return "institutions"

    @property
    def description(self) -> str:
        return "Find banks. Actions: list (browse), get (details by ID), search (by name)."

    @property
    def parameters(self) -> list[ToolParameter]:
        return [
            ToolParameter("action", "string", "list | get | search", required=True, enum=["list", "get", "search"]),
            ToolParameter("institution_id", "string", "Institution ID (for get)", required=False),
            ToolParameter("query", "string", "Search term (for search)", required=False),
        ]

    async def execute(self, **kwargs: Any) -> ToolResult:
        err = _check_configured()
        if err:
            return err
        try:
            mgr = _get_mgr()
            action = kwargs["action"]

            if action == "list":
                return ToolResult(output=json.dumps(mgr.get_institutions(count=20), indent=2), success=True)
            elif action == "get":
                iid = kwargs.get("institution_id", "")
                if not iid:
                    return ToolResult(output="", success=False, error="institution_id required")
                return ToolResult(output=json.dumps(mgr.get_institution_by_id(iid), indent=2), success=True)
            elif action == "search":
                q = kwargs.get("query", "")
                if not q:
                    return ToolResult(output="", success=False, error="query required")
                return ToolResult(output=json.dumps(mgr.search_institutions(q), indent=2), success=True)

            return ToolResult(output="", success=False, error=f"Unknown action: {action}")
        except Exception as e:
            return ToolResult(output="", success=False, error=f"Institutions error: {e}")


# ══════════════════════════════════════════════════════════════════
# 16. ITEM MANAGEMENT
# ══════════════════════════════════════════════════════════════════

class PlaidItemTool(BaseTool):
    """Manage linked bank connections."""

    @property
    def name(self) -> str:
        return "item_management"

    @property
    def description(self) -> str:
        return "Manage linked Items. Actions: get (status), remove (disconnect), update_webhook, invalidate_token (rotate)."

    @property
    def parameters(self) -> list[ToolParameter]:
        return [
            ToolParameter("action", "string", "get | remove | update_webhook | invalidate_token", required=True,
                          enum=["get", "remove", "update_webhook", "invalidate_token"]),
            ToolParameter("webhook_url", "string", "New webhook URL (for update_webhook)", required=False),
        ]

    async def execute(self, **kwargs: Any) -> ToolResult:
        err = _check_configured()
        if err:
            return err
        try:
            mgr = _get_mgr()
            action = kwargs["action"]

            if action == "get":
                items = []
                stored_keys = mgr.get_all_stored_tokens()
                for key, token in _iter_tokens():
                    try:
                        items.append({"vault_key": key, **mgr.get_item(token)})
                    except Exception as e:
                        items.append({"vault_key": key, "error": str(e)})
                return ToolResult(output=json.dumps({"token_count": len(stored_keys), "items": items}, indent=2), success=True)

            elif action == "remove":
                removed = 0
                for _, token in _iter_tokens():
                    if mgr.remove_item(token):
                        removed += 1
                return ToolResult(output=f"Removed {removed} item(s).", success=True)

            elif action == "update_webhook":
                url = kwargs.get("webhook_url", "")
                if not url:
                    return ToolResult(output="", success=False, error="webhook_url required")
                results = []
                for _, token in _iter_tokens():
                    results.append(mgr.update_item_webhook(token, url))
                return ToolResult(output=json.dumps(results, indent=2), success=True)

            elif action == "invalidate_token":
                results = []
                for key, token in _iter_tokens():
                    result = mgr.invalidate_access_token(token)
                    results.append({"vault_key": key, **result})
                return ToolResult(output=json.dumps(results, indent=2), success=True)

            return ToolResult(output="", success=False, error=f"Unknown action: {action}")
        except Exception as e:
            return ToolResult(output="", success=False, error=f"Item management error: {e}")


# ══════════════════════════════════════════════════════════════════
# 17. LINK
# ══════════════════════════════════════════════════════════════════

class PlaidLinkTool(BaseTool):
    """Manage Plaid Link tokens."""

    @property
    def name(self) -> str:
        return "link"

    @property
    def description(self) -> str:
        return "Plaid Link token management. Actions: create (new link token), exchange (public→access token), get (link token metadata)."

    @property
    def parameters(self) -> list[ToolParameter]:
        return [
            ToolParameter("action", "string", "create | exchange | get", required=True, enum=["create", "exchange", "get"]),
            ToolParameter("public_token", "string", "Public token from Link (for exchange)", required=False),
            ToolParameter("link_token", "string", "Link token (for get)", required=False),
            ToolParameter("products", "string", "Comma-separated products (for create)", required=False),
        ]

    async def execute(self, **kwargs: Any) -> ToolResult:
        err = _check_configured()
        if err:
            return err
        try:
            mgr = _get_mgr()
            action = kwargs["action"]

            if action == "create":
                prods = kwargs.get("products", "").split(",") if kwargs.get("products") else None
                token = mgr.create_link_token(products=prods)
                return ToolResult(output=f"Link token: {token}", success=True)
            elif action == "exchange":
                pt = kwargs.get("public_token", "")
                if not pt:
                    return ToolResult(output="", success=False, error="public_token required")
                return ToolResult(output=json.dumps(mgr.exchange_public_token(pt), indent=2), success=True)
            elif action == "get":
                lt = kwargs.get("link_token", "")
                if not lt:
                    return ToolResult(output="", success=False, error="link_token required")
                return ToolResult(output=json.dumps(mgr.get_link_token(lt), indent=2), success=True)

            return ToolResult(output="", success=False, error=f"Unknown action: {action}")
        except Exception as e:
            return ToolResult(output="", success=False, error=f"Link error: {e}")


# ══════════════════════════════════════════════════════════════════
# 18. SANDBOX
# ══════════════════════════════════════════════════════════════════

class PlaidSandboxTool(BaseTool):
    """Sandbox testing and simulation."""

    @property
    def name(self) -> str:
        return "sandbox"

    @property
    def description(self) -> str:
        return (
            "Sandbox testing. Actions: create_token (bypass Link), reset_login (force error state), "
            "fire_webhook, simulate_transfer, create_transactions, set_verification."
        )

    @property
    def parameters(self) -> list[ToolParameter]:
        return [
            ToolParameter("action", "string",
                          "create_token | reset_login | fire_webhook | simulate_transfer | simulate_refund | simulate_sweep | create_transactions | set_verification",
                          required=True,
                          enum=["create_token", "reset_login", "fire_webhook", "simulate_transfer", "simulate_refund", "simulate_sweep", "create_transactions", "set_verification"]),
            ToolParameter("institution_id", "string", "Institution ID (for create_token, default: ins_109508/Chase)", required=False),
            ToolParameter("products", "string", "Comma-separated products (for create_token)", required=False),
            ToolParameter("transfer_id", "string", "Transfer ID (for simulate_transfer)", required=False),
            ToolParameter("event_type", "string", "Event type (for simulate_transfer)", required=False),
            ToolParameter("webhook_type", "string", "Webhook type (for fire_webhook)", required=False),
            ToolParameter("webhook_code", "string", "Webhook code (for fire_webhook)", required=False),
            ToolParameter("account_id", "string", "Account ID (for set_verification)", required=False),
        ]

    async def execute(self, **kwargs: Any) -> ToolResult:
        err = _check_configured()
        if err:
            return err
        try:
            mgr = _get_mgr()
            action = kwargs["action"]

            if action == "create_token":
                inst = kwargs.get("institution_id", "ins_109508")
                prods = kwargs.get("products", "").split(",") if kwargs.get("products") else None
                result = mgr.sandbox_create_public_token(inst, prods)
                return ToolResult(output=json.dumps(result, indent=2), success=True)

            elif action == "reset_login":
                for _, token in _iter_tokens():
                    result = mgr.sandbox_reset_login(token)
                    return ToolResult(output=json.dumps(result, indent=2), success=True)
                return ToolResult(output="No linked items.", success=False)

            elif action == "fire_webhook":
                wtype = kwargs.get("webhook_type", "TRANSACTIONS")
                wcode = kwargs.get("webhook_code", "SYNC_UPDATES_AVAILABLE")
                for _, token in _iter_tokens():
                    result = mgr.sandbox_fire_webhook(token, wtype, wcode)
                    return ToolResult(output=json.dumps(result, indent=2), success=True)
                return ToolResult(output="No linked items.", success=False)

            elif action == "simulate_transfer":
                tid = kwargs.get("transfer_id", "")
                etype = kwargs.get("event_type", "")
                if not tid or not etype:
                    return ToolResult(output="", success=False, error="transfer_id and event_type required")
                return ToolResult(output=json.dumps(mgr.sandbox_simulate_transfer(tid, etype), indent=2), success=True)

            elif action == "simulate_refund":
                rid = kwargs.get("transfer_id", "")  # reuse for refund_id
                etype = kwargs.get("event_type", "")
                if not rid or not etype:
                    return ToolResult(output="", success=False, error="transfer_id (refund_id) and event_type required")
                return ToolResult(output=json.dumps(mgr.sandbox_simulate_refund(rid, etype), indent=2), success=True)

            elif action == "simulate_sweep":
                return ToolResult(output=json.dumps(mgr.sandbox_simulate_sweep(), indent=2), success=True)

            elif action == "create_transactions":
                for _, token in _iter_tokens():
                    result = mgr.sandbox_create_transactions(token)
                    return ToolResult(output=json.dumps(result, indent=2), success=True)
                return ToolResult(output="No linked items.", success=False)

            elif action == "set_verification":
                aid = kwargs.get("account_id", "")
                if not aid:
                    return ToolResult(output="", success=False, error="account_id required")
                for _, token in _iter_tokens():
                    result = mgr.sandbox_set_verification_status(token, aid)
                    return ToolResult(output=json.dumps(result, indent=2), success=True)
                return ToolResult(output="No linked items.", success=False)

            return ToolResult(output="", success=False, error=f"Unknown action: {action}")
        except Exception as e:
            return ToolResult(output="", success=False, error=f"Sandbox error: {e}")


# ══════════════════════════════════════════════════════════════════
# 19. NETWORK STATUS (read-only)
# ══════════════════════════════════════════════════════════════════

class PlaidNetworkTool(BaseTool):
    """Check Plaid Network status."""

    @property
    def name(self) -> str:
        return "network_status"

    @property
    def description(self) -> str:
        return "Check if a user's accounts are in the Plaid Network."

    @property
    def parameters(self) -> list[ToolParameter]:
        return []

    async def execute(self, **kwargs: Any) -> ToolResult:
        err = _check_configured()
        if err:
            return err
        try:
            mgr = _get_mgr()
            results = []
            for key, token in _iter_tokens():
                try:
                    results.append({"vault_key": key, **mgr.get_network_status(token)})
                except Exception as e:
                    results.append({"vault_key": key, "error": str(e)})
            return ToolResult(output=json.dumps(results, indent=2), success=True)
        except Exception as e:
            return ToolResult(output="", success=False, error=f"Network status error: {e}")


# ══════════════════════════════════════════════════════════════════
# 20. ENRICH (read-only)
# ══════════════════════════════════════════════════════════════════

class PlaidEnrichTool(BaseTool):
    """Enrich raw transaction data with merchant info and categories."""

    @property
    def name(self) -> str:
        return "enrich"

    @property
    def description(self) -> str:
        return "Enrich raw transactions with merchant logos, categories, and counterparty data. Provide transactions as JSON array."

    @property
    def parameters(self) -> list[ToolParameter]:
        return [
            ToolParameter("transactions", "string", "JSON array of transactions [{id, description, amount, direction}]", required=True),
        ]

    async def execute(self, **kwargs: Any) -> ToolResult:
        err = _check_configured()
        if err:
            return err
        try:
            mgr = _get_mgr()
            txns_str = kwargs.get("transactions", "[]")
            txns = json.loads(txns_str) if isinstance(txns_str, str) else txns_str
            result = mgr.enrich_transactions(txns)
            return ToolResult(output=json.dumps(result, indent=2), success=True)
        except Exception as e:
            return ToolResult(output="", success=False, error=f"Enrich error: {e}")


# ══════════════════════════════════════════════════════════════════
# 21. WEBHOOK VERIFY
# ══════════════════════════════════════════════════════════════════

class PlaidWebhookTool(BaseTool):
    """Webhook verification key management."""

    @property
    def name(self) -> str:
        return "webhook_verify"

    @property
    def description(self) -> str:
        return "Get webhook verification key for validating Plaid webhook signatures."

    @property
    def parameters(self) -> list[ToolParameter]:
        return [
            ToolParameter("key_id", "string", "The key ID from the webhook JWT header", required=True),
        ]

    async def execute(self, **kwargs: Any) -> ToolResult:
        err = _check_configured()
        if err:
            return err
        try:
            mgr = _get_mgr()
            kid = kwargs.get("key_id", "")
            if not kid:
                return ToolResult(output="", success=False, error="key_id required")
            return ToolResult(output=json.dumps(mgr.get_webhook_verification_key(kid), indent=2), success=True)
        except Exception as e:
            return ToolResult(output="", success=False, error=f"Webhook error: {e}")
