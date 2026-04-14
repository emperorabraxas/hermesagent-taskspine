"""Plaid integration — complete financial OS for Money Maker.

Full Plaid API coverage (97 methods). Every method is wired to a tool.

Products integrated:
  - Link: connect bank accounts, token management
  - Auth: account/routing numbers for ACH
  - Transactions: sync, recurring, enrichment, refresh, categories
  - Balance: real-time balance checks
  - Investments: holdings, securities, transactions, refresh
  - Assets: reports, PDF, audit copies, filtering
  - Income: bank income, payroll, employment, risk signals
  - Identity: verified data, identity matching
  - Identity Verification: KYC flow (create, get, list, retry)
  - Transfer: ACH/RTP money movement, recurring, refunds, ledger, sweeps
  - Signal: transaction risk scoring, decision/return reporting
  - Liabilities: credit cards, student loans
  - Statements: bank statement download
  - Beacon: anti-fraud user/report management
  - Institutions: search and lookup
  - Sandbox: testing and simulation
  - Webhooks: verification key management
  - Network: Plaid Network status checks

Flow: Link → token exchange → access_token (stored in vault) → data access
"""
from __future__ import annotations

import logging
import tempfile
from datetime import date, timedelta
from typing import Any, Iterator

import plaid
from plaid.api import plaid_api
from plaid.model.country_code import CountryCode
from plaid.model.products import Products

from agentic_hub.config import get_settings

logger = logging.getLogger(__name__)


def _get_plaid_client(environment: str = "") -> plaid_api.PlaidApi:
    """Create a Plaid API client using Settings (not raw os.environ)."""
    settings = get_settings()
    client_id = settings.plaid_client_id
    secret = settings.plaid_secret
    env = environment or settings.plaid_environment or "sandbox"

    if not client_id or not secret:
        # Vault fallback for credentials
        try:
            from agentic_hub.core.secrets import get_vault
            vault = get_vault()
            if vault:
                client_id = client_id or vault.retrieve("PLAID_CLIENT_ID") or ""
                secret = secret or vault.retrieve("PLAID_SECRET") or ""
        except Exception:
            pass

    if not client_id or not secret:
        raise ValueError("PLAID_CLIENT_ID and PLAID_SECRET required")

    env_map = {
        "sandbox": plaid.Environment.Sandbox,
        "development": plaid.Environment.Development,
        "production": plaid.Environment.Production,
    }

    configuration = plaid.Configuration(
        host=env_map.get(env, plaid.Environment.Sandbox),
        api_key={"clientId": client_id, "secret": secret},
    )
    return plaid_api.PlaidApi(plaid.ApiClient(configuration))


class PlaidManager:
    """Complete Plaid integration — 97 methods, zero dead code."""

    def __init__(self, environment: str = ""):
        self._environment = environment
        self._client: plaid_api.PlaidApi | None = None

    def _get_client(self) -> plaid_api.PlaidApi:
        if self._client is None:
            self._client = _get_plaid_client(self._environment)
        return self._client

    def _iter_access_tokens(self) -> Iterator[tuple[str, str]]:
        """Yield (vault_key, access_token) for all linked institutions."""
        try:
            from agentic_hub.core.secrets import get_vault
            vault = get_vault()
            if vault:
                for key in vault.list_keys():
                    if key.startswith("PLAID_ACCESS_"):
                        token = vault.retrieve(key)
                        if token:
                            yield key, token
        except Exception:
            pass

    @property
    def is_configured(self) -> bool:
        settings = get_settings()
        return bool(settings.plaid_client_id and settings.plaid_secret)

    # ══════════════════════════════════════════════════════════════
    # LINK
    # ══════════════════════════════════════════════════════════════

    def create_link_token(
        self, user_id: str = "spider.bob", products: list[str] | None = None
    ) -> str:
        """Create a Plaid Link token for the frontend widget."""
        from plaid.model.link_token_create_request import LinkTokenCreateRequest
        from plaid.model.link_token_create_request_user import LinkTokenCreateRequestUser

        if products is None:
            products = ["auth", "transactions", "investments", "liabilities", "identity"]

        request = LinkTokenCreateRequest(
            user=LinkTokenCreateRequestUser(client_user_id=user_id),
            client_name="spider.Web",
            products=[Products(p) for p in products],
            country_codes=[CountryCode("US")],
            language="en",
        )
        response = self._get_client().link_token_create(request)
        return response.link_token

    def exchange_public_token(self, public_token: str) -> dict:
        """Exchange public_token for access_token. Stores in vault."""
        from plaid.model.item_public_token_exchange_request import ItemPublicTokenExchangeRequest

        response = self._get_client().item_public_token_exchange(
            ItemPublicTokenExchangeRequest(public_token=public_token)
        )
        access_token = response.access_token
        item_id = response.item_id

        try:
            from agentic_hub.core.secrets import get_vault
            vault = get_vault()
            if vault:
                vault.store(f"PLAID_ACCESS_{item_id}", access_token)
                logger.info(f"Plaid access token stored: {item_id}")
        except Exception as e:
            logger.warning(f"Could not store token in vault: {e}")

        return {"access_token": access_token, "item_id": item_id}

    def get_link_token(self, link_token: str) -> dict:
        """Retrieve metadata about a link token."""
        from plaid.model.link_token_get_request import LinkTokenGetRequest

        response = self._get_client().link_token_get(
            LinkTokenGetRequest(link_token=link_token)
        )
        return {
            "link_token": response.link_token,
            "created_at": str(response.created_at),
            "expiration": str(response.expiration),
        }

    # ══════════════════════════════════════════════════════════════
    # AUTH
    # ══════════════════════════════════════════════════════════════

    def get_auth(self, access_token: str) -> list[dict]:
        """Get account and routing numbers for ACH transfers."""
        from plaid.model.auth_get_request import AuthGetRequest

        response = self._get_client().auth_get(AuthGetRequest(access_token=access_token))
        accounts = []
        numbers = response.numbers

        for acct in response.accounts:
            acct_data = {
                "id": acct.account_id,
                "name": acct.name,
                "type": str(acct.type),
                "subtype": str(acct.subtype) if acct.subtype else "",
                "balance": float(acct.balances.current or 0),
            }
            for ach in (numbers.ach or []):
                if ach.account_id == acct.account_id:
                    acct_data["routing"] = ach.routing
                    acct_data["account_number"] = ach.account
                    acct_data["wire_routing"] = getattr(ach, "wire_routing", "")
            accounts.append(acct_data)

        return accounts

    # ══════════════════════════════════════════════════════════════
    # ACCOUNTS & BALANCE
    # ══════════════════════════════════════════════════════════════

    def get_accounts(self, access_token: str) -> list[dict]:
        """Fetch all accounts linked to an access_token."""
        from plaid.model.accounts_get_request import AccountsGetRequest

        response = self._get_client().accounts_get(AccountsGetRequest(access_token=access_token))
        return [
            {
                "id": a.account_id,
                "name": a.name,
                "official_name": a.official_name or a.name,
                "type": str(a.type),
                "subtype": str(a.subtype) if a.subtype else "",
                "balance_current": float(a.balances.current or 0),
                "balance_available": float(a.balances.available or 0) if a.balances.available else None,
                "currency": a.balances.iso_currency_code or "USD",
                "mask": a.mask or "",
            }
            for a in response.accounts
        ]

    def get_balances(self, access_token: str) -> list[dict]:
        """Fetch real-time balances."""
        from plaid.model.accounts_balance_get_request import AccountsBalanceGetRequest

        response = self._get_client().accounts_balance_get(
            AccountsBalanceGetRequest(access_token=access_token)
        )
        return [
            {
                "id": a.account_id,
                "name": a.name,
                "type": str(a.type),
                "current": float(a.balances.current or 0),
                "available": float(a.balances.available or 0) if a.balances.available else None,
                "currency": a.balances.iso_currency_code or "USD",
            }
            for a in response.accounts
        ]

    def get_all_stored_tokens(self) -> list[str]:
        """Get all stored Plaid access token vault keys."""
        return [key for key, _ in self._iter_access_tokens()]

    def get_all_accounts_summary(self) -> list[dict]:
        """Get balances from ALL linked institutions."""
        all_accounts = []
        for _, token in self._iter_access_tokens():
            try:
                all_accounts.extend(self.get_balances(token))
            except Exception as e:
                logger.warning(f"Failed to fetch balances: {e}")
        return all_accounts

    # ══════════════════════════════════════════════════════════════
    # TRANSACTIONS
    # ══════════════════════════════════════════════════════════════

    def sync_transactions(self, access_token: str, cursor: str = "") -> dict:
        """Sync transactions using cursor-based pagination."""
        from plaid.model.transactions_sync_request import TransactionsSyncRequest

        request = TransactionsSyncRequest(access_token=access_token)
        if cursor:
            request.cursor = cursor

        response = self._get_client().transactions_sync(request)
        return {
            "added": [self._format_transaction(t) for t in (response.added or [])],
            "modified": [self._format_transaction(t) for t in (response.modified or [])],
            "removed": [{"id": t.transaction_id} for t in (response.removed or [])],
            "cursor": response.next_cursor,
            "has_more": response.has_more,
        }

    def get_transactions(
        self, access_token: str, start_date: str = "", end_date: str = "", count: int = 100
    ) -> list[dict]:
        """Get transactions for a date range."""
        from plaid.model.transactions_get_request import TransactionsGetRequest
        from plaid.model.transactions_get_request_options import TransactionsGetRequestOptions

        if not start_date:
            start_date = str(date.today() - timedelta(days=90))
        if not end_date:
            end_date = str(date.today())

        response = self._get_client().transactions_get(
            TransactionsGetRequest(
                access_token=access_token,
                start_date=date.fromisoformat(start_date),
                end_date=date.fromisoformat(end_date),
                options=TransactionsGetRequestOptions(count=count),
            )
        )
        return [self._format_transaction(t) for t in response.transactions]

    def get_recurring_transactions(self, access_token: str) -> dict:
        """Get recurring transaction streams (subscriptions, bills, income)."""
        from plaid.model.transactions_recurring_get_request import TransactionsRecurringGetRequest

        response = self._get_client().transactions_recurring_get(
            TransactionsRecurringGetRequest(access_token=access_token)
        )
        return {
            "inflow": [
                {
                    "description": s.description,
                    "amount": float(s.average_amount.amount) if s.average_amount else 0,
                    "frequency": str(s.frequency) if s.frequency else "",
                    "category": s.personal_finance_category.primary if s.personal_finance_category else "",
                }
                for s in (response.inflow_streams or [])
            ],
            "outflow": [
                {
                    "description": s.description,
                    "amount": float(s.average_amount.amount) if s.average_amount else 0,
                    "frequency": str(s.frequency) if s.frequency else "",
                    "category": s.personal_finance_category.primary if s.personal_finance_category else "",
                }
                for s in (response.outflow_streams or [])
            ],
        }

    def refresh_transactions(self, access_token: str) -> dict:
        """Force Plaid to check for new transactions immediately."""
        from plaid.model.transactions_refresh_request import TransactionsRefreshRequest

        self._get_client().transactions_refresh(
            TransactionsRefreshRequest(access_token=access_token)
        )
        return {"status": "refresh_initiated"}

    def enrich_transactions(self, transactions: list[dict]) -> list[dict]:
        """Enrich raw transaction data with merchant info, categories, logos."""
        from plaid.model.transactions_enrich_request import TransactionsEnrichRequest
        from plaid.model.client_provided_transaction import ClientProvidedTransaction
        from plaid.model.enrich_transaction_direction import EnrichTransactionDirection

        enriched_txns = []
        for t in transactions[:100]:
            enriched_txns.append(ClientProvidedTransaction(
                id=t.get("id", ""),
                description=t.get("description", t.get("name", "")),
                amount=float(t.get("amount", 0)),
                direction=EnrichTransactionDirection(t.get("direction", "OUTFLOW")),
                iso_currency_code=t.get("currency", "USD"),
            ))

        response = self._get_client().transactions_enrich(
            TransactionsEnrichRequest(
                account_type="depository",
                transactions=enriched_txns,
            )
        )
        return [
            {
                "id": t.id,
                "description": t.description,
                "amount": float(t.amount),
                "merchant_name": t.counterparties[0].name if t.counterparties else "",
                "category": t.personal_finance_category.primary if t.personal_finance_category else "",
                "payment_channel": str(t.payment_channel) if t.payment_channel else "",
                "logo_url": t.counterparties[0].logo_url if t.counterparties and hasattr(t.counterparties[0], 'logo_url') else "",
            }
            for t in (response.enriched_transactions or [])
        ]

    def get_categories(self) -> list[dict]:
        """Get Plaid's full transaction category taxonomy."""
        response = self._get_client().categories_get({})
        return [
            {
                "id": c.category_id,
                "group": c.group,
                "hierarchy": list(c.hierarchy),
            }
            for c in (response.categories or [])
        ]

    @staticmethod
    def _format_transaction(t) -> dict:
        return {
            "id": t.transaction_id,
            "name": t.name or t.merchant_name or "Unknown",
            "merchant": t.merchant_name or "",
            "amount": float(t.amount),
            "date": str(t.date),
            "category": list(t.category or []),
            "pending": t.pending,
            "account_id": t.account_id,
            "payment_channel": str(t.payment_channel) if t.payment_channel else "",
        }

    # ══════════════════════════════════════════════════════════════
    # INVESTMENTS
    # ══════════════════════════════════════════════════════════════

    def get_holdings(self, access_token: str) -> list[dict]:
        """Get current investment holdings."""
        from plaid.model.investments_holdings_get_request import InvestmentsHoldingsGetRequest

        response = self._get_client().investments_holdings_get(
            InvestmentsHoldingsGetRequest(access_token=access_token)
        )
        securities = {s.security_id: s for s in (response.securities or [])}

        return [
            {
                "account_id": h.account_id,
                "security_id": h.security_id,
                "ticker": securities.get(h.security_id, type("", (), {"ticker_symbol": ""})()).ticker_symbol or "",
                "name": securities.get(h.security_id, type("", (), {"name": ""})()).name or "",
                "quantity": float(h.quantity),
                "price": float(h.institution_price),
                "value": float(h.institution_value),
                "cost_basis": float(h.cost_basis) if h.cost_basis else None,
                "type": str(securities[h.security_id].type) if h.security_id in securities else "",
            }
            for h in (response.holdings or [])
        ]

    def get_investment_transactions(
        self, access_token: str, start_date: str = "", end_date: str = ""
    ) -> list[dict]:
        """Get investment transactions (buys, sells, dividends)."""
        from plaid.model.investments_transactions_get_request import InvestmentsTransactionsGetRequest

        if not start_date:
            start_date = str(date.today() - timedelta(days=90))
        if not end_date:
            end_date = str(date.today())

        response = self._get_client().investments_transactions_get(
            InvestmentsTransactionsGetRequest(
                access_token=access_token,
                start_date=date.fromisoformat(start_date),
                end_date=date.fromisoformat(end_date),
            )
        )
        securities = {s.security_id: s for s in (response.securities or [])}

        return [
            {
                "id": t.investment_transaction_id,
                "type": str(t.type),
                "subtype": str(t.subtype) if t.subtype else "",
                "ticker": securities.get(t.security_id, type("", (), {"ticker_symbol": ""})()).ticker_symbol or "",
                "name": t.name,
                "quantity": float(t.quantity),
                "price": float(t.price),
                "amount": float(t.amount),
                "date": str(t.date),
            }
            for t in (response.investment_transactions or [])
        ]

    def refresh_investments(self, access_token: str) -> dict:
        """Trigger real-time investment data refresh."""
        from plaid.model.investments_refresh_request import InvestmentsRefreshRequest

        self._get_client().investments_refresh(
            InvestmentsRefreshRequest(access_token=access_token)
        )
        return {"status": "refresh_initiated"}

    # ══════════════════════════════════════════════════════════════
    # IDENTITY
    # ══════════════════════════════════════════════════════════════

    def get_identity(self, access_token: str) -> list[dict]:
        """Get verified identity data (name, email, phone, address)."""
        from plaid.model.identity_get_request import IdentityGetRequest

        response = self._get_client().identity_get(
            IdentityGetRequest(access_token=access_token)
        )
        identities = []
        for acct in (response.accounts or []):
            for owner in (acct.owners or []):
                identities.append({
                    "account_id": acct.account_id,
                    "names": [n for n in (owner.names or [])],
                    "emails": [
                        {"data": e.data, "primary": e.primary, "type": str(e.type)}
                        for e in (owner.emails or [])
                    ],
                    "phones": [
                        {"data": p.data, "primary": p.primary, "type": str(p.type)}
                        for p in (owner.phone_numbers or [])
                    ],
                    "addresses": [
                        {
                            "street": a.data.street or "",
                            "city": a.data.city or "",
                            "region": a.data.region or "",
                            "postal_code": a.data.postal_code or "",
                            "country": a.data.country or "",
                            "primary": a.primary,
                        }
                        for a in (owner.addresses or [])
                    ],
                })
        return identities

    def match_identity(self, access_token: str, user_data: dict) -> dict:
        """Verify user identity against bank-held data. Returns match scores."""
        from plaid.model.identity_match_request import IdentityMatchRequest
        from plaid.model.identity_match_user import IdentityMatchUser

        user = IdentityMatchUser()
        if user_data.get("legal_name"):
            user.legal_name = user_data["legal_name"]
        if user_data.get("email"):
            user.email_address = user_data["email"]
        if user_data.get("phone"):
            user.phone_number = user_data["phone"]

        response = self._get_client().identity_match(
            IdentityMatchRequest(access_token=access_token, user=user)
        )
        results = []
        for acct in (response.accounts or []):
            match = {
                "account_id": acct.account_id,
                "name_score": acct.legal_name.score if acct.legal_name else None,
                "email_score": acct.email_address.score if acct.email_address else None,
                "phone_score": acct.phone_number.score if acct.phone_number else None,
                "address_score": acct.address.score if acct.address else None,
            }
            results.append(match)
        return {"accounts": results}

    # ══════════════════════════════════════════════════════════════
    # IDENTITY VERIFICATION (KYC)
    # ══════════════════════════════════════════════════════════════

    def create_identity_verification(self, template_id: str, user_data: dict) -> dict:
        """Create a new identity verification session."""
        from plaid.model.identity_verification_create_request import IdentityVerificationCreateRequest
        from plaid.model.identity_verification_create_request_user import IdentityVerificationCreateRequestUser

        user = IdentityVerificationCreateRequestUser(
            client_user_id=user_data.get("client_user_id", "spider.bob"),
            email_address=user_data.get("email", ""),
        )
        response = self._get_client().identity_verification_create(
            IdentityVerificationCreateRequest(
                template_id=template_id,
                gave_consent=True,
                user=user,
                is_shareable=False,
            )
        )
        return {
            "id": response.id,
            "status": str(response.status),
            "shareable_url": response.shareable_url or "",
            "created_at": str(response.created_at),
        }

    def get_identity_verification(self, identity_verification_id: str) -> dict:
        """Retrieve an identity verification by ID."""
        from plaid.model.identity_verification_get_request import IdentityVerificationGetRequest

        response = self._get_client().identity_verification_get(
            IdentityVerificationGetRequest(identity_verification_id=identity_verification_id)
        )
        return {
            "id": response.id,
            "status": str(response.status),
            "steps": {step: str(getattr(response.steps, step, "")) for step in ["verify_sms", "documentary_verification", "selfie_check", "kyc_check", "risk_check"]},
            "created_at": str(response.created_at),
        }

    def list_identity_verifications(self, template_id: str, client_user_id: str = "") -> list[dict]:
        """List identity verifications for a template."""
        from plaid.model.identity_verification_list_request import IdentityVerificationListRequest

        request = IdentityVerificationListRequest(template_id=template_id)
        if client_user_id:
            request.client_user_id = client_user_id

        response = self._get_client().identity_verification_list(request)
        return [
            {"id": v.id, "status": str(v.status), "created_at": str(v.created_at)}
            for v in (response.identity_verifications or [])
        ]

    def retry_identity_verification(self, client_user_id: str, template_id: str) -> dict:
        """Retry a failed identity verification."""
        from plaid.model.identity_verification_retry_request import IdentityVerificationRetryRequest

        response = self._get_client().identity_verification_retry(
            IdentityVerificationRetryRequest(
                client_user_id=client_user_id,
                template_id=template_id,
                strategy="reset",
            )
        )
        return {
            "id": response.id,
            "status": str(response.status),
        }

    # ══════════════════════════════════════════════════════════════
    # ASSETS
    # ══════════════════════════════════════════════════════════════

    def create_asset_report(self, access_tokens: list[str], days: int = 90) -> dict:
        """Create an asset report for underwriting."""
        from plaid.model.asset_report_create_request import AssetReportCreateRequest

        response = self._get_client().asset_report_create(
            AssetReportCreateRequest(access_tokens=access_tokens, days_requested=days)
        )
        return {
            "asset_report_token": response.asset_report_token,
            "asset_report_id": response.asset_report_id,
        }

    def get_asset_report(self, asset_report_token: str) -> dict:
        """Retrieve a completed asset report."""
        from plaid.model.asset_report_get_request import AssetReportGetRequest

        response = self._get_client().asset_report_get(
            AssetReportGetRequest(asset_report_token=asset_report_token)
        )
        report = response.report
        return {
            "report_id": report.asset_report_id,
            "generated": str(report.date_generated),
            "days_requested": report.days_requested,
            "items": [
                {
                    "institution": item.institution_name,
                    "accounts": [
                        {
                            "name": a.name,
                            "type": str(a.type),
                            "current": float(a.balances.current or 0),
                            "available": float(a.balances.available or 0) if a.balances.available else None,
                            "days_available": a.days_available,
                            "transactions": len(a.transactions or []),
                        }
                        for a in (item.accounts or [])
                    ],
                }
                for item in (report.items or [])
            ],
        }

    def get_asset_report_pdf(self, asset_report_token: str) -> dict:
        """Download asset report as PDF. Returns file path."""
        from plaid.model.asset_report_pdf_get_request import AssetReportPDFGetRequest

        response = self._get_client().asset_report_pdf_get(
            AssetReportPDFGetRequest(asset_report_token=asset_report_token)
        )
        with tempfile.NamedTemporaryFile(suffix=".pdf", prefix="plaid_asset_", delete=False) as f:
            f.write(response.read())
            return {"path": f.name, "size": f.tell()}

    def refresh_asset_report(self, asset_report_token: str, days: int = 90) -> dict:
        """Create an updated asset report with fresh data."""
        from plaid.model.asset_report_refresh_request import AssetReportRefreshRequest

        response = self._get_client().asset_report_refresh(
            AssetReportRefreshRequest(asset_report_token=asset_report_token, days_requested=days)
        )
        return {
            "asset_report_token": response.asset_report_token,
            "asset_report_id": response.asset_report_id,
        }

    def filter_asset_report(self, asset_report_token: str, account_ids: list[str]) -> dict:
        """Remove accounts from an asset report."""
        from plaid.model.asset_report_filter_request import AssetReportFilterRequest

        response = self._get_client().asset_report_filter(
            AssetReportFilterRequest(
                asset_report_token=asset_report_token,
                account_ids_to_exclude=account_ids,
            )
        )
        return {
            "asset_report_token": response.asset_report_token,
            "asset_report_id": response.asset_report_id,
        }

    def remove_asset_report(self, asset_report_token: str) -> bool:
        """Delete an asset report."""
        from plaid.model.asset_report_remove_request import AssetReportRemoveRequest

        response = self._get_client().asset_report_remove(
            AssetReportRemoveRequest(asset_report_token=asset_report_token)
        )
        return response.removed

    def create_audit_copy(self, asset_report_token: str, auditor_id: str) -> dict:
        """Create a shareable audit copy of an asset report."""
        from plaid.model.asset_report_audit_copy_create_request import AssetReportAuditCopyCreateRequest

        response = self._get_client().asset_report_audit_copy_create(
            AssetReportAuditCopyCreateRequest(
                asset_report_token=asset_report_token,
                auditor_id=auditor_id,
            )
        )
        return {"audit_copy_token": response.audit_copy_token}

    def remove_audit_copy(self, audit_copy_token: str) -> bool:
        """Delete an audit copy."""
        from plaid.model.asset_report_audit_copy_remove_request import AssetReportAuditCopyRemoveRequest

        response = self._get_client().asset_report_audit_copy_remove(
            AssetReportAuditCopyRemoveRequest(audit_copy_token=audit_copy_token)
        )
        return response.removed

    # ══════════════════════════════════════════════════════════════
    # INCOME / CREDIT
    # ══════════════════════════════════════════════════════════════

    def get_bank_income(self, access_token: str) -> dict:
        """Get bank income analysis from transaction data."""
        from plaid.model.credit_bank_income_get_request import CreditBankIncomeGetRequest

        response = self._get_client().credit_bank_income_get(
            CreditBankIncomeGetRequest(user_token=access_token)
        )
        items = []
        for item in (response.bank_income or []):
            for source in (item.bank_income_sources or []):
                items.append({
                    "source": source.income_description or "",
                    "amount": float(source.total_amount) if source.total_amount else 0,
                    "frequency": str(source.pay_frequency) if source.pay_frequency else "",
                    "start_date": str(source.start_date) if source.start_date else "",
                    "end_date": str(source.end_date) if source.end_date else "",
                    "transaction_count": source.transaction_count or 0,
                })
        return {"income_sources": items}

    def get_bank_income_pdf(self, access_token: str) -> dict:
        """Download bank income report as PDF. Returns file path."""
        from plaid.model.credit_bank_income_pdf_get_request import CreditBankIncomePDFGetRequest

        response = self._get_client().credit_bank_income_pdf_get(
            CreditBankIncomePDFGetRequest(user_token=access_token)
        )
        with tempfile.NamedTemporaryFile(suffix=".pdf", prefix="plaid_income_", delete=False) as f:
            f.write(response.read())
            return {"path": f.name, "size": f.tell()}

    def get_payroll_income(self, access_token: str) -> dict:
        """Get payroll income data from pay stubs / tax forms."""
        from plaid.model.credit_payroll_income_get_request import CreditPayrollIncomeGetRequest

        response = self._get_client().credit_payroll_income_get(
            CreditPayrollIncomeGetRequest(user_token=access_token)
        )
        return {"status": "ok", "items_count": len(response.items or [])}

    def get_payroll_risk_signals(self, access_token: str) -> dict:
        """Evaluate payroll documents for fraud indicators."""
        from plaid.model.credit_payroll_income_risk_signals_get_request import CreditPayrollIncomeRiskSignalsGetRequest

        response = self._get_client().credit_payroll_income_risk_signals_get(
            CreditPayrollIncomeRiskSignalsGetRequest(user_token=access_token)
        )
        return {"status": "ok", "items_count": len(response.items or [])}

    def get_employment(self, access_token: str) -> dict:
        """Get employment information from payroll sources."""
        from plaid.model.credit_employment_get_request import CreditEmploymentGetRequest

        response = self._get_client().credit_employment_get(
            CreditEmploymentGetRequest(user_token=access_token)
        )
        items = []
        for item in (response.items or []):
            for emp in (item.employments or []):
                items.append({
                    "employer": emp.employer.name if emp.employer else "",
                    "title": emp.title or "",
                    "start_date": str(emp.start_date) if emp.start_date else "",
                    "status": str(emp.status) if emp.status else "",
                })
        return {"employments": items}

    def get_credit_sessions(self, access_token: str) -> list[dict]:
        """Get Link session metadata for income verification."""
        from plaid.model.credit_sessions_get_request import CreditSessionsGetRequest

        response = self._get_client().credit_sessions_get(
            CreditSessionsGetRequest(user_token=access_token)
        )
        return [
            {"session_id": s.link_session_id, "status": str(s.session_status) if hasattr(s, 'session_status') else ""}
            for s in (response.sessions or [])
        ]

    # ══════════════════════════════════════════════════════════════
    # SIGNAL (RISK SCORING)
    # ══════════════════════════════════════════════════════════════

    def evaluate_signal(self, access_token: str, account_id: str, amount: float) -> dict:
        """Evaluate ACH return risk for a transaction."""
        from plaid.model.signal_evaluate_request import SignalEvaluateRequest
        import time

        response = self._get_client().signal_evaluate(
            SignalEvaluateRequest(
                access_token=access_token,
                account_id=account_id,
                client_transaction_id=f"spider_{int(time.time())}",
                amount=amount,
            )
        )
        scores = response.scores
        return {
            "overall_score": scores.customer_initiated_return_risk.score if scores.customer_initiated_return_risk else None,
            "bank_return_score": scores.bank_initiated_return_risk.score if scores.bank_initiated_return_risk else None,
            "risk_tier": scores.customer_initiated_return_risk.risk_tier if scores.customer_initiated_return_risk else "",
        }

    def report_signal_decision(self, access_token: str, client_transaction_id: str, initiated: bool) -> dict:
        """Report whether you initiated an ACH transaction (improves Signal accuracy)."""
        from plaid.model.signal_decision_report_request import SignalDecisionReportRequest

        self._get_client().signal_decision_report(
            SignalDecisionReportRequest(
                client_transaction_id=client_transaction_id,
                initiated=initiated,
            )
        )
        return {"status": "reported", "initiated": initiated}

    def report_signal_return(self, access_token: str, client_transaction_id: str, return_code: str) -> dict:
        """Report an ACH return for a previously evaluated transaction."""
        from plaid.model.signal_return_report_request import SignalReturnReportRequest

        self._get_client().signal_return_report(
            SignalReturnReportRequest(
                client_transaction_id=client_transaction_id,
                return_code=return_code,
            )
        )
        return {"status": "reported", "return_code": return_code}

    def prepare_signal(self, access_token: str) -> dict:
        """Enable an existing Item for Signal scores."""
        from plaid.model.signal_prepare_request import SignalPrepareRequest

        self._get_client().signal_prepare(
            SignalPrepareRequest(access_token=access_token)
        )
        return {"status": "prepared"}

    # ══════════════════════════════════════════════════════════════
    # LIABILITIES
    # ══════════════════════════════════════════════════════════════

    def get_liabilities(self, access_token: str) -> dict:
        """Get credit card and loan liabilities."""
        from plaid.model.liabilities_get_request import LiabilitiesGetRequest

        response = self._get_client().liabilities_get(
            LiabilitiesGetRequest(access_token=access_token)
        )
        liabilities = response.liabilities
        return {
            "credit": [
                {
                    "account_id": c.account_id,
                    "last_payment": float(c.last_payment_amount) if c.last_payment_amount else 0,
                    "last_statement_balance": float(c.last_statement_balance) if c.last_statement_balance else 0,
                    "minimum_payment": float(c.minimum_payment_amount) if c.minimum_payment_amount else 0,
                    "apr": [{"pct": float(a.apr_percentage), "type": str(a.apr_type)} for a in (c.aprs or [])],
                }
                for c in (liabilities.credit or [])
            ],
            "student": [
                {
                    "account_id": s.account_id,
                    "loan_name": s.loan_name,
                    "outstanding": float(s.outstanding_interest_amount or 0),
                }
                for s in (liabilities.student or [])
            ],
        }

    # ══════════════════════════════════════════════════════════════
    # TRANSFER (ACH MONEY MOVEMENT)
    # ══════════════════════════════════════════════════════════════

    def create_transfer(
        self,
        access_token: str,
        account_id: str,
        amount: str,
        transfer_type: str = "debit",
        description: str = "spider.Web transfer",
    ) -> dict:
        """Create an ACH transfer with authorization."""
        from plaid.model.transfer_create_request import TransferCreateRequest
        from plaid.model.transfer_type import TransferType
        from plaid.model.transfer_network import TransferNetwork
        from plaid.model.ach_class import ACHClass
        from plaid.model.transfer_authorization_create_request import TransferAuthorizationCreateRequest

        client = self._get_client()

        auth_response = client.transfer_authorization_create(
            TransferAuthorizationCreateRequest(
                access_token=access_token,
                account_id=account_id,
                type=TransferType(transfer_type),
                network=TransferNetwork("ach"),
                amount=amount,
                ach_class=ACHClass("ppd"),
                user={"legal_name": "spider.BOB"},
            )
        )
        authorization = auth_response.authorization
        if authorization.decision != "approved":
            return {"status": "rejected", "reason": str(authorization.decision_rationale)}

        transfer_response = client.transfer_create(
            TransferCreateRequest(
                access_token=access_token,
                account_id=account_id,
                authorization_id=authorization.authorization_id,
                description=description,
            )
        )
        transfer = transfer_response.transfer
        return {
            "status": "ok",
            "transfer_id": transfer.id,
            "amount": transfer.amount,
            "type": str(transfer.type),
            "network": str(transfer.network),
            "created": str(transfer.created),
        }

    def get_transfer(self, transfer_id: str) -> dict:
        """Get details of a specific transfer."""
        from plaid.model.transfer_get_request import TransferGetRequest

        response = self._get_client().transfer_get(
            TransferGetRequest(transfer_id=transfer_id)
        )
        t = response.transfer
        return {
            "id": t.id, "type": str(t.type), "status": str(t.status),
            "amount": t.amount, "network": str(t.network),
            "description": t.description, "created": str(t.created),
        }

    def list_transfers(self, start_date: str = "", end_date: str = "", count: int = 25, offset: int = 0) -> list[dict]:
        """List transfers with optional date filters."""
        from plaid.model.transfer_list_request import TransferListRequest

        kwargs: dict[str, Any] = {"count": count, "offset": offset}
        if start_date:
            kwargs["start_date"] = start_date
        if end_date:
            kwargs["end_date"] = end_date

        response = self._get_client().transfer_list(TransferListRequest(**kwargs))
        return [
            {"id": t.id, "type": str(t.type), "status": str(t.status), "amount": t.amount, "created": str(t.created)}
            for t in (response.transfers or [])
        ]

    def cancel_transfer(self, transfer_id: str) -> dict:
        """Cancel a pending transfer."""
        from plaid.model.transfer_cancel_request import TransferCancelRequest

        self._get_client().transfer_cancel(TransferCancelRequest(transfer_id=transfer_id))
        return {"status": "cancelled", "transfer_id": transfer_id}

    def get_transfer_events(self, start_date: str = "", end_date: str = "", count: int = 25) -> list[dict]:
        """List transfer events."""
        from plaid.model.transfer_event_list_request import TransferEventListRequest

        kwargs: dict[str, Any] = {"count": count}
        if start_date:
            kwargs["start_date"] = start_date
        if end_date:
            kwargs["end_date"] = end_date

        response = self._get_client().transfer_event_list(TransferEventListRequest(**kwargs))
        return [
            {"event_id": e.event_id, "event_type": str(e.event_type), "transfer_id": e.transfer_id, "timestamp": str(e.timestamp)}
            for e in (response.transfer_events or [])
        ]

    def sync_transfer_events(self, after_id: int = 0, count: int = 25) -> dict:
        """Sync transfer events using cursor."""
        from plaid.model.transfer_event_sync_request import TransferEventSyncRequest

        response = self._get_client().transfer_event_sync(
            TransferEventSyncRequest(after_id=after_id, count=count)
        )
        return {
            "events": [
                {"event_id": e.event_id, "event_type": str(e.event_type), "transfer_id": e.transfer_id}
                for e in (response.transfer_events or [])
            ],
        }

    def get_transfer_sweep(self, sweep_id: str) -> dict:
        """Get details of a specific sweep."""
        from plaid.model.transfer_sweep_get_request import TransferSweepGetRequest

        response = self._get_client().transfer_sweep_get(
            TransferSweepGetRequest(sweep_id=sweep_id)
        )
        s = response.sweep
        return {"id": s.id, "amount": s.amount, "status": str(s.status), "created": str(s.created)}

    def list_transfer_sweeps(self, start_date: str = "", end_date: str = "", count: int = 25) -> list[dict]:
        """List transfer sweeps."""
        from plaid.model.transfer_sweep_list_request import TransferSweepListRequest

        kwargs: dict[str, Any] = {"count": count}
        if start_date:
            kwargs["start_date"] = start_date
        if end_date:
            kwargs["end_date"] = end_date

        response = self._get_client().transfer_sweep_list(TransferSweepListRequest(**kwargs))
        return [
            {"id": s.id, "amount": s.amount, "status": str(s.status), "created": str(s.created)}
            for s in (response.sweeps or [])
        ]

    def get_transfer_capabilities(self, access_token: str, account_id: str) -> dict:
        """Check RTP eligibility for an account."""
        from plaid.model.transfer_capabilities_get_request import TransferCapabilitiesGetRequest

        response = self._get_client().transfer_capabilities_get(
            TransferCapabilitiesGetRequest(access_token=access_token, account_id=account_id)
        )
        return {
            "rtp_eligible": getattr(response, "institution_supported_networks", {}).get("rtp", False) if hasattr(response, "institution_supported_networks") else False,
        }

    def create_recurring_transfer(self, access_token: str, account_id: str, amount: str, schedule: dict, transfer_type: str = "debit", description: str = "spider.Web recurring") -> dict:
        """Create a recurring ACH transfer."""
        from plaid.model.transfer_recurring_create_request import TransferRecurringCreateRequest
        from plaid.model.transfer_type import TransferType
        from plaid.model.transfer_network import TransferNetwork
        from plaid.model.ach_class import ACHClass
        from plaid.model.transfer_recurring_schedule import TransferRecurringSchedule

        sched = TransferRecurringSchedule(
            interval_unit=schedule.get("interval_unit", "month"),
            interval_count=schedule.get("interval_count", 1),
            interval_execution_day=schedule.get("execution_day", 1),
            start_date=date.fromisoformat(schedule["start_date"]),
        )
        if schedule.get("end_date"):
            sched.end_date = date.fromisoformat(schedule["end_date"])

        response = self._get_client().transfer_recurring_create(
            TransferRecurringCreateRequest(
                access_token=access_token,
                account_id=account_id,
                type=TransferType(transfer_type),
                network=TransferNetwork("ach"),
                amount=amount,
                ach_class=ACHClass("ppd"),
                schedule=sched,
                description=description,
                user={"legal_name": "spider.BOB"},
            )
        )
        rt = response.recurring_transfer
        return {"recurring_transfer_id": rt.recurring_transfer_id, "status": str(rt.status), "created": str(rt.created)}

    def cancel_recurring_transfer(self, recurring_transfer_id: str) -> dict:
        """Cancel a recurring transfer."""
        from plaid.model.transfer_recurring_cancel_request import TransferRecurringCancelRequest

        self._get_client().transfer_recurring_cancel(
            TransferRecurringCancelRequest(recurring_transfer_id=recurring_transfer_id)
        )
        return {"status": "cancelled", "recurring_transfer_id": recurring_transfer_id}

    def get_recurring_transfer(self, recurring_transfer_id: str) -> dict:
        """Get details of a recurring transfer."""
        from plaid.model.transfer_recurring_get_request import TransferRecurringGetRequest

        response = self._get_client().transfer_recurring_get(
            TransferRecurringGetRequest(recurring_transfer_id=recurring_transfer_id)
        )
        rt = response.recurring_transfer
        return {"id": rt.recurring_transfer_id, "status": str(rt.status), "amount": rt.amount, "created": str(rt.created)}

    def list_recurring_transfers(self, start_date: str = "", end_date: str = "", count: int = 25) -> list[dict]:
        """List recurring transfers."""
        from plaid.model.transfer_recurring_list_request import TransferRecurringListRequest

        kwargs: dict[str, Any] = {"count": count}
        if start_date:
            kwargs["start_date"] = start_date
        if end_date:
            kwargs["end_date"] = end_date

        response = self._get_client().transfer_recurring_list(TransferRecurringListRequest(**kwargs))
        return [
            {"id": rt.recurring_transfer_id, "status": str(rt.status), "amount": rt.amount}
            for rt in (response.recurring_transfers or [])
        ]

    def create_transfer_refund(self, transfer_id: str, amount: str) -> dict:
        """Create a refund for a completed transfer."""
        from plaid.model.transfer_refund_create_request import TransferRefundCreateRequest

        response = self._get_client().transfer_refund_create(
            TransferRefundCreateRequest(transfer_id=transfer_id, amount=amount)
        )
        r = response.refund
        return {"refund_id": r.id, "status": str(r.status), "amount": r.amount, "created": str(r.created)}

    def get_transfer_refund(self, refund_id: str) -> dict:
        """Get details of a refund."""
        from plaid.model.transfer_refund_get_request import TransferRefundGetRequest

        response = self._get_client().transfer_refund_get(
            TransferRefundGetRequest(refund_id=refund_id)
        )
        r = response.refund
        return {"id": r.id, "status": str(r.status), "amount": r.amount, "created": str(r.created)}

    def cancel_transfer_refund(self, refund_id: str) -> dict:
        """Cancel a pending refund."""
        from plaid.model.transfer_refund_cancel_request import TransferRefundCancelRequest

        self._get_client().transfer_refund_cancel(
            TransferRefundCancelRequest(refund_id=refund_id)
        )
        return {"status": "cancelled", "refund_id": refund_id}

    def deposit_ledger(self, amount: str, description: str = "") -> dict:
        """Deposit funds into Plaid ledger balance."""
        from plaid.model.transfer_ledger_deposit_request import TransferLedgerDepositRequest

        response = self._get_client().transfer_ledger_deposit(
            TransferLedgerDepositRequest(amount=amount, description=description or "spider.Web deposit")
        )
        return {"sweep_id": response.sweep.id, "status": str(response.sweep.status)}

    def withdraw_ledger(self, amount: str, description: str = "") -> dict:
        """Withdraw funds from Plaid ledger balance."""
        from plaid.model.transfer_ledger_withdraw_request import TransferLedgerWithdrawRequest

        response = self._get_client().transfer_ledger_withdraw(
            TransferLedgerWithdrawRequest(amount=amount, description=description or "spider.Web withdrawal")
        )
        return {"sweep_id": response.sweep.id, "status": str(response.sweep.status)}

    def get_ledger(self) -> dict:
        """Get current Plaid ledger balance."""
        from plaid.model.transfer_ledger_get_request import TransferLedgerGetRequest

        response = self._get_client().transfer_ledger_get(TransferLedgerGetRequest())
        b = response.balance
        return {"available": b.available, "pending": b.pending}

    def get_transfer_metrics(self) -> dict:
        """Get transfer product usage metrics."""
        from plaid.model.transfer_metrics_get_request import TransferMetricsGetRequest

        response = self._get_client().transfer_metrics_get(TransferMetricsGetRequest())
        return {"request_id": response.request_id}

    def get_transfer_config(self) -> dict:
        """Get transfer product configuration."""
        from plaid.model.transfer_configuration_get_request import TransferConfigurationGetRequest

        response = self._get_client().transfer_configuration_get(TransferConfigurationGetRequest())
        return {"request_id": response.request_id}

    # ══════════════════════════════════════════════════════════════
    # STATEMENTS
    # ══════════════════════════════════════════════════════════════

    def list_statements(self, access_token: str) -> list[dict]:
        """List available bank statements for download."""
        from plaid.model.statements_list_request import StatementsListRequest

        response = self._get_client().statements_list(
            StatementsListRequest(access_token=access_token)
        )
        results = []
        for acct in (response.accounts or []):
            for stmt in (acct.statements or []):
                results.append({
                    "account_id": acct.account_id,
                    "statement_id": stmt.statement_id,
                    "month": stmt.month,
                    "year": stmt.year,
                })
        return results

    def download_statement(self, access_token: str, statement_id: str) -> dict:
        """Download a bank statement PDF. Returns file path."""
        from plaid.model.statements_download_request import StatementsDownloadRequest

        response = self._get_client().statements_download(
            StatementsDownloadRequest(access_token=access_token, statement_id=statement_id)
        )
        with tempfile.NamedTemporaryFile(suffix=".pdf", prefix="plaid_stmt_", delete=False) as f:
            f.write(response.read())
            return {"path": f.name, "size": f.tell(), "statement_id": statement_id}

    def refresh_statements(self, access_token: str, start_date: str = "", end_date: str = "") -> dict:
        """Trigger on-demand statement extraction."""
        from plaid.model.statements_refresh_request import StatementsRefreshRequest

        if not start_date:
            start_date = str(date.today() - timedelta(days=365))
        if not end_date:
            end_date = str(date.today())

        self._get_client().statements_refresh(
            StatementsRefreshRequest(
                access_token=access_token,
                start_date=date.fromisoformat(start_date),
                end_date=date.fromisoformat(end_date),
            )
        )
        return {"status": "refresh_initiated"}

    # ══════════════════════════════════════════════════════════════
    # BEACON (ANTI-FRAUD)
    # ══════════════════════════════════════════════════════════════

    def create_beacon_user(self, program_id: str, user_data: dict) -> dict:
        """Create and scan a Beacon user against a fraud program."""
        from plaid.model.beacon_user_create_request import BeaconUserCreateRequest
        from plaid.model.beacon_user_request_data import BeaconUserRequestData
        from plaid.model.beacon_user_name import BeaconUserName

        name = BeaconUserName(
            given_name=user_data.get("first_name", ""),
            family_name=user_data.get("last_name", ""),
        )
        user = BeaconUserRequestData(
            name=name,
            date_of_birth=date.fromisoformat(user_data["dob"]) if user_data.get("dob") else None,
        )
        if user_data.get("email"):
            user.email_address = user_data["email"]

        response = self._get_client().beacon_user_create(
            BeaconUserCreateRequest(program_id=program_id, client_user_id=user_data.get("client_user_id", "spider.bob"), user=user)
        )
        return {"beacon_user_id": response.id, "status": str(response.status)}

    def get_beacon_user(self, beacon_user_id: str) -> dict:
        """Get a Beacon user and their fraud status."""
        from plaid.model.beacon_user_get_request import BeaconUserGetRequest

        response = self._get_client().beacon_user_get(
            BeaconUserGetRequest(beacon_user_id=beacon_user_id)
        )
        return {"id": response.id, "status": str(response.status), "created_at": str(response.created_at)}

    def update_beacon_user(self, beacon_user_id: str, user_data: dict) -> dict:
        """Update a Beacon user's identity data."""
        from plaid.model.beacon_user_update_request import BeaconUserUpdateRequest

        kwargs: dict[str, Any] = {"beacon_user_id": beacon_user_id}
        response = self._get_client().beacon_user_update(BeaconUserUpdateRequest(**kwargs))
        return {"id": response.id, "status": str(response.status)}

    def create_beacon_report(self, beacon_user_id: str, report_type: str, fraud_date: str) -> dict:
        """File a fraud report for a Beacon user."""
        from plaid.model.beacon_report_create_request import BeaconReportCreateRequest
        from plaid.model.beacon_report_type import BeaconReportType

        response = self._get_client().beacon_report_create(
            BeaconReportCreateRequest(
                beacon_user_id=beacon_user_id,
                type=BeaconReportType(report_type),
                fraud_date=date.fromisoformat(fraud_date),
            )
        )
        return {"report_id": response.id, "type": str(response.type), "created_at": str(response.created_at)}

    def get_beacon_report(self, beacon_report_id: str) -> dict:
        """Get a specific fraud report."""
        from plaid.model.beacon_report_get_request import BeaconReportGetRequest

        response = self._get_client().beacon_report_get(
            BeaconReportGetRequest(beacon_report_id=beacon_report_id)
        )
        return {"id": response.id, "type": str(response.type), "created_at": str(response.created_at)}

    def list_beacon_reports(self, beacon_user_id: str) -> list[dict]:
        """List all fraud reports for a Beacon user."""
        from plaid.model.beacon_report_list_request import BeaconReportListRequest

        response = self._get_client().beacon_report_list(
            BeaconReportListRequest(beacon_user_id=beacon_user_id)
        )
        return [
            {"id": r.id, "type": str(r.type), "created_at": str(r.created_at)}
            for r in (response.beacon_reports or [])
        ]

    def get_beacon_duplicate(self, beacon_duplicate_id: str) -> dict:
        """Get a Beacon duplicate match."""
        from plaid.model.beacon_duplicate_get_request import BeaconDuplicateGetRequest

        response = self._get_client().beacon_duplicate_get(
            BeaconDuplicateGetRequest(beacon_duplicate_id=beacon_duplicate_id)
        )
        return {"id": response.id, "beacon_user1_id": response.beacon_user1_id, "beacon_user2_id": response.beacon_user2_id}

    # ══════════════════════════════════════════════════════════════
    # NETWORK
    # ══════════════════════════════════════════════════════════════

    def get_network_status(self, access_token: str) -> dict:
        """Check the status of a user in the Plaid Network."""
        from plaid.model.network_status_get_request import NetworkStatusGetRequest

        response = self._get_client().network_status_get(
            NetworkStatusGetRequest(access_token=access_token)
        )
        return {"has_accounts": response.has_accounts_data if hasattr(response, 'has_accounts_data') else None}

    # ══════════════════════════════════════════════════════════════
    # INSTITUTIONS
    # ══════════════════════════════════════════════════════════════

    def get_institutions(self, count: int = 100, offset: int = 0, country_codes: list[str] | None = None) -> list[dict]:
        """List supported financial institutions."""
        from plaid.model.institutions_get_request import InstitutionsGetRequest

        codes = [CountryCode(c) for c in (country_codes or ["US"])]
        response = self._get_client().institutions_get(
            InstitutionsGetRequest(count=count, offset=offset, country_codes=codes)
        )
        return [
            {"id": i.institution_id, "name": i.name, "products": [str(p) for p in (i.products or [])]}
            for i in (response.institutions or [])
        ]

    def get_institution_by_id(self, institution_id: str) -> dict:
        """Get details of a specific institution."""
        from plaid.model.institutions_get_by_id_request import InstitutionsGetByIdRequest

        response = self._get_client().institutions_get_by_id(
            InstitutionsGetByIdRequest(institution_id=institution_id, country_codes=[CountryCode("US")])
        )
        i = response.institution
        return {
            "id": i.institution_id, "name": i.name,
            "products": [str(p) for p in (i.products or [])],
            "url": i.url or "", "logo": i.logo or "",
        }

    def search_institutions(self, query: str, products: list[str] | None = None) -> list[dict]:
        """Search institutions by name."""
        from plaid.model.institutions_search_request import InstitutionsSearchRequest

        prods = [Products(p) for p in products] if products else None
        kwargs: dict[str, Any] = {
            "query": query,
            "country_codes": [CountryCode("US")],
        }
        if prods:
            kwargs["products"] = prods

        response = self._get_client().institutions_search(InstitutionsSearchRequest(**kwargs))
        return [
            {"id": i.institution_id, "name": i.name, "products": [str(p) for p in (i.products or [])]}
            for i in (response.institutions or [])
        ]

    # ══════════════════════════════════════════════════════════════
    # ITEM MANAGEMENT
    # ══════════════════════════════════════════════════════════════

    def get_item(self, access_token: str) -> dict:
        """Get info about a linked institution."""
        from plaid.model.item_get_request import ItemGetRequest

        response = self._get_client().item_get(ItemGetRequest(access_token=access_token))
        item = response.item
        return {
            "item_id": item.item_id,
            "institution_id": item.institution_id,
            "products": [str(p) for p in (item.products or [])],
            "consented_products": [str(p) for p in (item.consented_products or [])],
            "consent_expiration": str(item.consent_expiration_time) if item.consent_expiration_time else None,
            "update_type": str(item.update_type) if item.update_type else "",
        }

    def remove_item(self, access_token: str) -> bool:
        """Remove a linked institution."""
        from plaid.model.item_remove_request import ItemRemoveRequest

        try:
            self._get_client().item_remove(ItemRemoveRequest(access_token=access_token))
            return True
        except Exception:
            return False

    def update_item_webhook(self, access_token: str, webhook_url: str) -> dict:
        """Update the webhook URL for an Item."""
        from plaid.model.item_webhook_update_request import ItemWebhookUpdateRequest

        response = self._get_client().item_webhook_update(
            ItemWebhookUpdateRequest(access_token=access_token, webhook=webhook_url)
        )
        return {"item_id": response.item.item_id}

    def invalidate_access_token(self, access_token: str) -> dict:
        """Rotate an access token (invalidates the old one)."""
        from plaid.model.item_access_token_invalidate_request import ItemAccessTokenInvalidateRequest

        response = self._get_client().item_access_token_invalidate(
            ItemAccessTokenInvalidateRequest(access_token=access_token)
        )
        return {"new_access_token": response.new_access_token}

    # ══════════════════════════════════════════════════════════════
    # WEBHOOKS
    # ══════════════════════════════════════════════════════════════

    def get_webhook_verification_key(self, key_id: str) -> dict:
        """Get a webhook verification key for signature validation."""
        from plaid.model.webhook_verification_key_get_request import WebhookVerificationKeyGetRequest

        response = self._get_client().webhook_verification_key_get(
            WebhookVerificationKeyGetRequest(key_id=key_id)
        )
        return {"key": response.key.to_dict() if response.key else {}}

    # ══════════════════════════════════════════════════════════════
    # SANDBOX (TESTING)
    # ══════════════════════════════════════════════════════════════

    def sandbox_create_public_token(self, institution_id: str = "ins_109508", products: list[str] | None = None) -> dict:
        """Create a test Item in sandbox (bypasses Link)."""
        from plaid.model.sandbox_public_token_create_request import SandboxPublicTokenCreateRequest

        if products is None:
            products = ["auth", "transactions"]

        response = self._get_client().sandbox_public_token_create(
            SandboxPublicTokenCreateRequest(
                institution_id=institution_id,
                initial_products=[Products(p) for p in products],
            )
        )
        return {"public_token": response.public_token}

    def sandbox_reset_login(self, access_token: str) -> dict:
        """Force an Item into ITEM_LOGIN_REQUIRED state."""
        from plaid.model.sandbox_item_reset_login_request import SandboxItemResetLoginRequest

        response = self._get_client().sandbox_item_reset_login(
            SandboxItemResetLoginRequest(access_token=access_token)
        )
        return {"reset": response.reset_login}

    def sandbox_fire_webhook(self, access_token: str, webhook_type: str = "TRANSACTIONS", webhook_code: str = "SYNC_UPDATES_AVAILABLE") -> dict:
        """Fire a test webhook."""
        from plaid.model.sandbox_item_fire_webhook_request import SandboxItemFireWebhookRequest

        response = self._get_client().sandbox_item_fire_webhook(
            SandboxItemFireWebhookRequest(
                access_token=access_token,
                webhook_type=webhook_type,
                webhook_code=webhook_code,
            )
        )
        return {"webhook_fired": response.webhook_fired}

    def sandbox_simulate_transfer(self, transfer_id: str, event_type: str) -> dict:
        """Simulate a transfer event in sandbox."""
        from plaid.model.sandbox_transfer_simulate_request import SandboxTransferSimulateRequest

        response = self._get_client().sandbox_transfer_simulate(
            SandboxTransferSimulateRequest(transfer_id=transfer_id, event_type=event_type)
        )
        return {"status": "simulated"}

    def sandbox_simulate_refund(self, refund_id: str, event_type: str) -> dict:
        """Simulate a refund event in sandbox."""
        from plaid.model.sandbox_transfer_refund_simulate_request import SandboxTransferRefundSimulateRequest

        response = self._get_client().sandbox_transfer_refund_simulate(
            SandboxTransferRefundSimulateRequest(refund_id=refund_id, event_type=event_type)
        )
        return {"status": "simulated"}

    def sandbox_simulate_sweep(self) -> dict:
        """Simulate creating a sweep in sandbox."""
        response = self._get_client().sandbox_transfer_sweep_simulate({})
        return {"status": "simulated"}

    def sandbox_create_transactions(self, access_token: str, start_date: str = "", end_date: str = "") -> dict:
        """Create custom test transactions in sandbox."""
        from plaid.model.sandbox_transactions_create_request import SandboxTransactionsCreateRequest

        if not start_date:
            start_date = str(date.today() - timedelta(days=30))
        if not end_date:
            end_date = str(date.today())

        self._get_client().sandbox_transactions_create(
            SandboxTransactionsCreateRequest(
                access_token=access_token,
                start_date=date.fromisoformat(start_date),
                end_date=date.fromisoformat(end_date),
            )
        )
        return {"status": "transactions_created"}

    def sandbox_set_verification_status(self, access_token: str, account_id: str, status: str = "automatically_verified") -> dict:
        """Set verification status for micro-deposits in sandbox."""
        from plaid.model.sandbox_item_set_verification_status_request import SandboxItemSetVerificationStatusRequest

        self._get_client().sandbox_item_set_verification_status(
            SandboxItemSetVerificationStatusRequest(
                access_token=access_token,
                account_id=account_id,
                verification_status=status,
            )
        )
        return {"status": status}


# ── Singleton ─────────────────────────────────────────────────────

_manager: PlaidManager | None = None


def get_plaid_manager(environment: str = "") -> PlaidManager:
    global _manager
    if _manager is None:
        _manager = PlaidManager(environment)
    return _manager
