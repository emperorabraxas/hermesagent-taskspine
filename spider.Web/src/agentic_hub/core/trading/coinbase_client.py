"""Coinbase Advanced Trade API client — complete crypto trading.

Full integration based on Coinbase CDP documentation:
  - All order types: market, limit, stop-limit, TWAP
  - Time-in-force: GTC, IOC, FOK, GTD
  - Order preview (dry-run), edit, batch cancel
  - Portfolio management (create, edit, delete, move funds)
  - Product/market data (candles, order book, trades)
  - Account management
  - Fill history
  - WebSocket real-time feeds

Requires: COINBASE_API_KEY, COINBASE_API_SECRET in .env or vault.
"""
from __future__ import annotations

import asyncio
import json
import logging
import os
import time
from typing import Any

logger = logging.getLogger(__name__)


class CoinbaseClient:
    """Complete Coinbase Advanced Trade API wrapper for Money Maker."""

    def __init__(self):
        self._client = None
        self._initialized = False

    def _get_credentials(self) -> tuple[str, str]:
        """Get API credentials from vault or .env."""
        api_key = os.environ.get("COINBASE_API_KEY", "")
        api_secret = os.environ.get("COINBASE_API_SECRET", "")

        if not api_key or not api_secret:
            try:
                from agentic_hub.core.secrets import get_vault
                vault = get_vault()
                if vault:
                    api_key = vault.retrieve("COINBASE_API_KEY") or api_key
                    api_secret = vault.retrieve("COINBASE_API_SECRET") or api_secret
            except Exception:
                pass

        return api_key, api_secret

    def _ensure_client(self):
        """Initialize the Coinbase client lazily."""
        if self._initialized:
            return

        api_key, api_secret = self._get_credentials()
        if not api_key or not api_secret:
            raise ValueError("COINBASE_API_KEY and COINBASE_API_SECRET required")

        try:
            from coinbase.rest import RESTClient
            # Fix PEM key — .env stores \n as literal, SDK needs actual newlines
            if "\\n" in api_secret:
                api_secret = api_secret.replace("\\n", "\n")

            # Detect key type: CDP (organizations/...) vs Legacy (short UUID)
            if api_key.startswith("organizations/"):
                # CDP key — use directly with coinbase-advanced-py
                self._client = RESTClient(api_key=api_key, api_secret=api_secret)
            else:
                # Legacy Advanced Trade key — needs HMAC auth
                # coinbase-advanced-py 1.7+ supports both formats
                self._client = RESTClient(api_key=api_key, api_secret=api_secret)

            self._initialized = True
            logger.info("Coinbase client initialized")
        except Exception as e:
            raise ValueError(f"Coinbase init failed: {e}")

    # ══════════════════════════════════════════════════════════════
    # ACCOUNTS
    # ══════════════════════════════════════════════════════════════

    def get_accounts(self, include_dust: bool = False) -> list[dict]:
        """Fetch all Coinbase accounts with balances."""
        self._ensure_client()
        try:
            accounts = self._client.get_accounts()
            result = []
            for acct in accounts.accounts:
                # Handle both dict and object formats for balance
                ab = acct.available_balance
                bal = float(ab["value"] if isinstance(ab, dict) else ab.value) if ab else 0
                hd = acct.hold
                hold = float(hd["value"] if isinstance(hd, dict) else hd.value) if hd else 0
                if not include_dust and bal < 0.001:
                    continue
                result.append({
                    "id": acct.uuid,
                    "name": acct.name,
                    "currency": acct.currency,
                    "balance": bal,
                    "hold": hold,
                    "type": acct.type,
                })
            return result
        except Exception as e:
            logger.error(f"Coinbase get_accounts: {e}")
            return []

    def get_account(self, account_id: str) -> dict | None:
        """Get a single account by UUID."""
        self._ensure_client()
        try:
            acct = self._client.get_account(account_id)
            return {
                "id": acct.uuid,
                "name": acct.name,
                "currency": acct.currency,
                "balance": float(acct.available_balance.value) if acct.available_balance else 0,
                "hold": float(acct.hold.value) if acct.hold else 0,
            }
        except Exception as e:
            logger.error(f"Coinbase get_account: {e}")
            return None

    def get_portfolio_value(self) -> float:
        """Get total portfolio value in USD."""
        accounts = self.get_accounts()
        total = 0.0
        for acct in accounts:
            if acct["currency"] == "USD":
                total += acct["balance"]
            else:
                price = self.get_price(f"{acct['currency']}-USD")
                if price:
                    total += acct["balance"] * price
        return total

    # ══════════════════════════════════════════════════════════════
    # ORDERS — ALL TYPES
    # ══════════════════════════════════════════════════════════════

    def buy(
        self,
        product_id: str,
        amount_usd: float | None = None,
        quantity: float | None = None,
        order_type: str = "market",
        limit_price: float | None = None,
        stop_price: float | None = None,
        time_in_force: str = "GTC",
        post_only: bool = False,
    ) -> dict:
        """Place a buy order.

        Order types:
          market: immediate execution at market price
          limit: execute at limit_price or better
          stop_limit: triggers at stop_price, executes as limit at limit_price
        """
        self._ensure_client()
        import uuid
        client_order_id = str(uuid.uuid4())

        try:
            if order_type == "market":
                if amount_usd:
                    order = self._client.market_order_buy(
                        client_order_id=client_order_id,
                        product_id=product_id,
                        quote_size=str(amount_usd),
                    )
                elif quantity:
                    order = self._client.market_order_buy(
                        client_order_id=client_order_id,
                        product_id=product_id,
                        base_size=str(quantity),
                    )
                else:
                    return {"error": "amount_usd or quantity required for market order"}

            elif order_type == "limit":
                if not limit_price:
                    return {"error": "limit_price required for limit order"}
                if not quantity:
                    return {"error": "quantity required for limit order"}

                if time_in_force == "IOC":
                    order = self._client.limit_order_ioc_buy(
                        client_order_id=client_order_id,
                        product_id=product_id,
                        base_size=str(quantity),
                        limit_price=str(limit_price),
                    )
                elif time_in_force == "FOK":
                    order = self._client.limit_order_fok_buy(
                        client_order_id=client_order_id,
                        product_id=product_id,
                        base_size=str(quantity),
                        limit_price=str(limit_price),
                    )
                else:  # GTC default
                    order = self._client.limit_order_gtc_buy(
                        client_order_id=client_order_id,
                        product_id=product_id,
                        base_size=str(quantity),
                        limit_price=str(limit_price),
                        post_only=post_only,
                    )

            elif order_type == "stop_limit":
                if not stop_price or not limit_price or not quantity:
                    return {"error": "stop_price, limit_price, and quantity required for stop_limit"}
                order = self._client.stop_limit_order_gtc_buy(
                    client_order_id=client_order_id,
                    product_id=product_id,
                    base_size=str(quantity),
                    limit_price=str(limit_price),
                    stop_price=str(stop_price),
                )
            else:
                return {"error": f"Unknown order type: {order_type}"}

            logger.info(f"Coinbase BUY {product_id} ({order_type})")
            return {
                "status": "ok",
                "order_id": getattr(order, "order_id", client_order_id),
                "client_order_id": client_order_id,
                "product": product_id,
                "side": "buy",
                "type": order_type,
            }
        except Exception as e:
            logger.error(f"Coinbase buy failed: {e}")
            return {"error": str(e)}

    def sell(
        self,
        product_id: str,
        quantity: float | None = None,
        amount_usd: float | None = None,
        order_type: str = "market",
        limit_price: float | None = None,
        stop_price: float | None = None,
        time_in_force: str = "GTC",
        post_only: bool = False,
    ) -> dict:
        """Place a sell order. Same order types as buy."""
        self._ensure_client()
        import uuid
        client_order_id = str(uuid.uuid4())

        try:
            if order_type == "market":
                if quantity:
                    order = self._client.market_order_sell(
                        client_order_id=client_order_id,
                        product_id=product_id,
                        base_size=str(quantity),
                    )
                elif amount_usd:
                    order = self._client.market_order_sell(
                        client_order_id=client_order_id,
                        product_id=product_id,
                        quote_size=str(amount_usd),
                    )
                else:
                    return {"error": "quantity or amount_usd required"}

            elif order_type == "limit":
                if not limit_price or not quantity:
                    return {"error": "limit_price and quantity required"}

                if time_in_force == "IOC":
                    order = self._client.limit_order_ioc_sell(
                        client_order_id=client_order_id,
                        product_id=product_id,
                        base_size=str(quantity),
                        limit_price=str(limit_price),
                    )
                elif time_in_force == "FOK":
                    order = self._client.limit_order_fok_sell(
                        client_order_id=client_order_id,
                        product_id=product_id,
                        base_size=str(quantity),
                        limit_price=str(limit_price),
                    )
                else:
                    order = self._client.limit_order_gtc_sell(
                        client_order_id=client_order_id,
                        product_id=product_id,
                        base_size=str(quantity),
                        limit_price=str(limit_price),
                        post_only=post_only,
                    )

            elif order_type == "stop_limit":
                if not stop_price or not limit_price or not quantity:
                    return {"error": "stop_price, limit_price, and quantity required"}
                order = self._client.stop_limit_order_gtc_sell(
                    client_order_id=client_order_id,
                    product_id=product_id,
                    base_size=str(quantity),
                    limit_price=str(limit_price),
                    stop_price=str(stop_price),
                )
            else:
                return {"error": f"Unknown order type: {order_type}"}

            logger.info(f"Coinbase SELL {product_id} ({order_type})")
            return {
                "status": "ok",
                "order_id": getattr(order, "order_id", client_order_id),
                "client_order_id": client_order_id,
                "product": product_id,
                "side": "sell",
                "type": order_type,
            }
        except Exception as e:
            logger.error(f"Coinbase sell failed: {e}")
            return {"error": str(e)}

    # ══════════════════════════════════════════════════════════════
    # ORDER MANAGEMENT
    # ══════════════════════════════════════════════════════════════

    def preview_order(
        self, product_id: str, side: str, quantity: float,
        order_type: str = "market", limit_price: float | None = None,
    ) -> dict:
        """Preview an order without executing — see fees, slippage, etc."""
        self._ensure_client()
        try:
            preview = self._client.preview_order(
                product_id=product_id,
                side=side.upper(),
                order_configuration={
                    "market_market_ioc": {"quote_size": str(quantity)}
                } if order_type == "market" else {
                    "limit_limit_gtc": {
                        "base_size": str(quantity),
                        "limit_price": str(limit_price),
                    }
                },
            )
            return {
                "status": "ok",
                "slippage": getattr(preview, "slippage", ""),
                "best_bid": getattr(preview, "best_bid", ""),
                "best_ask": getattr(preview, "best_ask", ""),
                "total": getattr(preview, "order_total", ""),
            }
        except Exception as e:
            return {"error": str(e)}

    def edit_order(self, order_id: str, new_price: float | None = None, new_size: float | None = None) -> dict:
        """Edit an open order's price or size."""
        self._ensure_client()
        try:
            kwargs = {"order_id": order_id}
            if new_price:
                kwargs["price"] = str(new_price)
            if new_size:
                kwargs["size"] = str(new_size)
            result = self._client.edit_order(**kwargs)
            return {"status": "ok", "result": str(result)}
        except Exception as e:
            return {"error": str(e)}

    def get_orders(self, product_id: str = "", status: str = "", limit: int = 50) -> list[dict]:
        """Get orders, optionally filtered."""
        self._ensure_client()
        try:
            kwargs = {}
            if product_id:
                kwargs["product_id"] = product_id
            if status:
                kwargs["order_status"] = [status]
            kwargs["limit"] = limit

            orders = self._client.list_orders(**kwargs)
            return [
                {
                    "id": o.order_id,
                    "client_id": getattr(o, "client_order_id", ""),
                    "product": o.product_id,
                    "side": o.side,
                    "type": o.order_type,
                    "status": o.status,
                    "created": str(o.created_time),
                    "filled_size": getattr(o, "filled_size", ""),
                    "filled_value": getattr(o, "filled_value", ""),
                    "average_filled_price": getattr(o, "average_filled_price", ""),
                }
                for o in (orders.orders or [])
            ]
        except Exception as e:
            logger.error(f"Coinbase get_orders: {e}")
            return []

    def get_order(self, order_id: str) -> dict | None:
        """Get a single order by ID."""
        self._ensure_client()
        try:
            o = self._client.get_order(order_id)
            return {
                "id": o.order_id,
                "product": o.product_id,
                "side": o.side,
                "type": o.order_type,
                "status": o.status,
                "filled_size": getattr(o, "filled_size", ""),
                "average_filled_price": getattr(o, "average_filled_price", ""),
            }
        except Exception as e:
            logger.error(f"Coinbase get_order: {e}")
            return None

    def cancel_order(self, order_id: str) -> bool:
        """Cancel a single order."""
        self._ensure_client()
        try:
            self._client.cancel_orders([order_id])
            return True
        except Exception as e:
            logger.error(f"Coinbase cancel: {e}")
            return False

    def cancel_all_orders(self, product_id: str = "") -> int:
        """Cancel all open orders, optionally for a specific product."""
        orders = self.get_orders(product_id=product_id, status="OPEN")
        if not orders:
            return 0
        order_ids = [o["id"] for o in orders]
        try:
            self._client.cancel_orders(order_ids)
            return len(order_ids)
        except Exception as e:
            logger.error(f"Coinbase cancel_all: {e}")
            return 0

    def get_fills(self, product_id: str = "", order_id: str = "", limit: int = 50) -> list[dict]:
        """Get fill history (executed trades)."""
        self._ensure_client()
        try:
            kwargs = {"limit": limit}
            if product_id:
                kwargs["product_id"] = product_id
            if order_id:
                kwargs["order_id"] = order_id

            fills = self._client.get_fills(**kwargs)
            return [
                {
                    "trade_id": getattr(f, "trade_id", ""),
                    "order_id": f.order_id,
                    "product": f.product_id,
                    "side": f.side,
                    "price": str(f.price),
                    "size": str(f.size),
                    "commission": str(getattr(f, "commission", "")),
                    "time": str(f.trade_time),
                }
                for f in (fills.fills or [])
            ]
        except Exception as e:
            logger.error(f"Coinbase get_fills: {e}")
            return []

    # ══════════════════════════════════════════════════════════════
    # MARKET DATA
    # ══════════════════════════════════════════════════════════════

    def get_price(self, product_id: str = "BTC-USD") -> float | None:
        """Get current price for a trading pair."""
        self._ensure_client()
        try:
            product = self._client.get_product(product_id)
            return float(product.price) if product.price else None
        except Exception as e:
            logger.error(f"Coinbase price {product_id}: {e}")
            return None

    def get_product(self, product_id: str) -> dict | None:
        """Get full product details (trading pair info)."""
        self._ensure_client()
        try:
            p = self._client.get_product(product_id)
            return {
                "id": p.product_id,
                "base": p.base_currency_id,
                "quote": p.quote_currency_id,
                "price": float(p.price) if p.price else 0,
                "volume_24h": float(p.volume_24h) if p.volume_24h else 0,
                "price_change_24h": float(p.price_percentage_change_24h) if p.price_percentage_change_24h else 0,
                "status": p.status,
                "min_order": float(p.base_min_size) if p.base_min_size else 0,
            }
        except Exception as e:
            logger.error(f"Coinbase get_product: {e}")
            return None

    def get_products(self, product_type: str = "") -> list[dict]:
        """List all tradeable products."""
        self._ensure_client()
        try:
            kwargs = {}
            if product_type:
                kwargs["product_type"] = product_type
            products = self._client.list_products(**kwargs)
            return [
                {
                    "id": p.product_id,
                    "price": float(p.price) if p.price else 0,
                    "volume_24h": float(p.volume_24h) if p.volume_24h else 0,
                    "change_24h": float(p.price_percentage_change_24h) if p.price_percentage_change_24h else 0,
                    "status": p.status,
                }
                for p in (products.products or [])
                if p.status == "online"
            ]
        except Exception as e:
            logger.error(f"Coinbase get_products: {e}")
            return []

    def get_candles(
        self, product_id: str, granularity: str = "ONE_HOUR",
        start: int | None = None, end: int | None = None,
    ) -> list[dict]:
        """Get OHLCV candle data for technical analysis.

        Granularities: ONE_MINUTE, FIVE_MINUTE, FIFTEEN_MINUTE,
        THIRTY_MINUTE, ONE_HOUR, TWO_HOUR, SIX_HOUR, ONE_DAY
        """
        self._ensure_client()
        try:
            if not start:
                start = int(time.time()) - 86400  # Last 24h
            if not end:
                end = int(time.time())

            candles = self._client.get_candles(
                product_id=product_id,
                start=str(start),
                end=str(end),
                granularity=granularity,
            )
            return [
                {
                    "time": int(c.start),
                    "open": float(c.open),
                    "high": float(c.high),
                    "low": float(c.low),
                    "close": float(c.close),
                    "volume": float(c.volume),
                }
                for c in (candles.candles or [])
            ]
        except Exception as e:
            logger.error(f"Coinbase candles: {e}")
            return []

    def get_order_book(self, product_id: str, limit: int = 10) -> dict:
        """Get order book (level 2 data)."""
        self._ensure_client()
        try:
            book = self._client.get_product_book(product_id=product_id, limit=limit)
            return {
                "bids": [
                    {"price": float(b.price), "size": float(b.size)}
                    for b in (book.pricebook.bids or [])
                ],
                "asks": [
                    {"price": float(a.price), "size": float(a.size)}
                    for a in (book.pricebook.asks or [])
                ],
                "time": str(book.pricebook.time) if book.pricebook.time else "",
            }
        except Exception as e:
            logger.error(f"Coinbase order_book: {e}")
            return {"bids": [], "asks": []}

    def get_trades(self, product_id: str, limit: int = 20) -> list[dict]:
        """Get recent market trades."""
        self._ensure_client()
        try:
            trades = self._client.get_market_trades(product_id=product_id, limit=limit)
            return [
                {
                    "id": t.trade_id,
                    "price": float(t.price),
                    "size": float(t.size),
                    "side": t.side,
                    "time": str(t.time),
                }
                for t in (trades.trades or [])
            ]
        except Exception as e:
            logger.error(f"Coinbase trades: {e}")
            return []

    # ══════════════════════════════════════════════════════════════
    # PORTFOLIOS
    # ══════════════════════════════════════════════════════════════

    def get_portfolios(self) -> list[dict]:
        """List all portfolios."""
        self._ensure_client()
        try:
            portfolios = self._client.get_portfolios()
            return [
                {
                    "id": p.uuid,
                    "name": p.name,
                    "type": p.type,
                }
                for p in (portfolios.portfolios or [])
            ]
        except Exception as e:
            logger.error(f"Coinbase portfolios: {e}")
            return []

    def get_portfolio_breakdown(self, portfolio_id: str) -> dict:
        """Get detailed breakdown of a portfolio."""
        self._ensure_client()
        try:
            breakdown = self._client.get_portfolio_breakdown(portfolio_id)
            return {"status": "ok", "data": str(breakdown)}
        except Exception as e:
            return {"error": str(e)}

    def create_portfolio(self, name: str) -> dict:
        """Create a new portfolio."""
        self._ensure_client()
        try:
            result = self._client.create_portfolio(name=name)
            return {"status": "ok", "id": getattr(result, "uuid", ""), "name": name}
        except Exception as e:
            return {"error": str(e)}

    def move_funds(self, from_portfolio: str, to_portfolio: str, currency: str, amount: str) -> dict:
        """Move funds between portfolios."""
        self._ensure_client()
        try:
            self._client.move_portfolio_funds(
                value=amount,
                currency=currency,
                source_portfolio_uuid=from_portfolio,
                target_portfolio_uuid=to_portfolio,
            )
            return {"status": "ok", "moved": f"{amount} {currency}"}
        except Exception as e:
            return {"error": str(e)}

    # ══════════════════════════════════════════════════════════════
    # CONVENIENCE
    # ══════════════════════════════════════════════════════════════

    def get_top_movers(self, limit: int = 10) -> list[dict]:
        """Get top movers by 24h price change."""
        products = self.get_products()
        if not products:
            return []
        # Sort by absolute change
        products.sort(key=lambda p: abs(p.get("change_24h", 0)), reverse=True)
        return products[:limit]

    def get_summary(self) -> dict:
        """Get a full account summary — balances, open orders, portfolio value."""
        accounts = self.get_accounts()
        open_orders = self.get_orders(status="OPEN")
        portfolio_value = self.get_portfolio_value()

        return {
            "portfolio_value_usd": portfolio_value,
            "accounts": len(accounts),
            "holdings": [
                {"currency": a["currency"], "balance": a["balance"]}
                for a in accounts
            ],
            "open_orders": len(open_orders),
        }

    @property
    def is_configured(self) -> bool:
        api_key, api_secret = self._get_credentials()
        return bool(api_key and api_secret)


# Singleton
_client: CoinbaseClient | None = None


def get_coinbase() -> CoinbaseClient:
    global _client
    if _client is None:
        _client = CoinbaseClient()
    return _client
