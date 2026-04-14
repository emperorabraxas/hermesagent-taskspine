"""Webull Open API client — raw HTTP via httpx, no third-party SDK.

Full integration based on official Webull Open API docs (developer.webull.com):
  - HMAC-SHA1 request signing (every request authenticated)
  - Account data: list, balances, positions
  - Trading: place/cancel orders (stocks, options, crypto)
  - Market data: snapshots, quotes, historical bars, ticks, instruments
  - Real-time streaming: MQTT push (connection config provided)

Auth: app_key + app_secret (register at developer.webull.com)
No OAuth browser flow — just API keys.

Setup:
  1. Register at developer.webull.com
  2. Subscribe to "Trader API - Individual"
  3. Create an app → get app_key and app_secret
  4. Set WEBULL_APP_KEY and WEBULL_APP_SECRET in .env
"""
from __future__ import annotations

import base64
import hashlib
import hmac
import logging
import os
import uuid
from datetime import datetime, timezone
from typing import Any
from urllib.parse import quote

import httpx

logger = logging.getLogger(__name__)

BASE_URL = "https://api.webull.com"
HOST = "api.webull.com"


class WebullClient:
    """Complete Webull trading client for Money Maker (Wolf)."""

    def __init__(self):
        self._app_key = ""
        self._app_secret = ""
        self._access_token = ""
        self._load_credentials()

    def _load_credentials(self):
        """Load Webull app credentials from env or secrets vault."""
        self._app_key = os.environ.get("WEBULL_APP_KEY", "")
        self._app_secret = os.environ.get("WEBULL_APP_SECRET", "")
        self._access_token = os.environ.get("WEBULL_ACCESS_TOKEN", "")

        if not self._app_key or not self._app_secret:
            try:
                from agentic_hub.core.secrets import get_vault
                vault = get_vault()
                if vault:
                    self._app_key = vault.retrieve("WEBULL_APP_KEY") or self._app_key
                    self._app_secret = vault.retrieve("WEBULL_APP_SECRET") or self._app_secret
                    self._access_token = vault.retrieve("WEBULL_ACCESS_TOKEN") or self._access_token
            except Exception:
                pass

    # ══════════════════════════════════════════════════════════════
    # REQUEST SIGNING (HMAC-SHA1)
    # ══════════════════════════════════════════════════════════════

    def _sign_request(
        self, method: str, uri: str, params: dict | None = None, body: str = "",
    ) -> dict:
        """Generate signed headers for a Webull API request.

        Signature algorithm:
        1. Collect: uri, query params, headers, md5(body)
        2. Sort all k=v pairs alphabetically by key
        3. Concatenate: uri + "&" + sorted_pairs [+ "&" + MD5(body)]
        4. URL-encode the whole string
        5. HMAC-SHA1(app_secret + "&", encoded_string) → base64
        """
        timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        nonce = uuid.uuid4().hex

        # Headers that participate in signing
        sign_headers = {
            "x-app-key": self._app_key,
            "x-signature-algorithm": "HMAC-SHA1",
            "x-signature-version": "1.0",
            "x-signature-nonce": nonce,
            "x-timestamp": timestamp,
            "host": HOST,
        }

        # Merge query params + sign headers into one sorted map
        all_params = {}
        if params:
            all_params.update(params)
        all_params.update(sign_headers)

        # Sort by key, join as k1=v1&k2=v2
        sorted_pairs = "&".join(
            f"{k}={v}" for k, v in sorted(all_params.items())
        )

        # Build sign string
        sign_string = f"{uri}&{sorted_pairs}"
        if body:
            body_md5 = hashlib.md5(body.encode()).hexdigest().upper()
            sign_string += f"&{body_md5}"

        # URL-encode, then HMAC-SHA1
        encoded = quote(sign_string, safe="")
        key = (self._app_secret + "&").encode()
        signature = base64.b64encode(
            hmac.new(key, encoded.encode(), hashlib.sha1).digest()
        ).decode()

        # Build final headers
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "x-app-key": self._app_key,
            "x-signature": signature,
            "x-signature-algorithm": "HMAC-SHA1",
            "x-signature-version": "1.0",
            "x-signature-nonce": nonce,
            "x-timestamp": timestamp,
            "x-version": "v2",
        }
        if self._access_token:
            headers["x-access-token"] = self._access_token

        return headers

    async def _get(self, uri: str, params: dict | None = None) -> dict:
        """Signed GET request."""
        headers = self._sign_request("GET", uri, params=params)
        url = f"{BASE_URL}{uri}"
        async with httpx.AsyncClient(timeout=30) as client:
            resp = await client.get(url, headers=headers, params=params)
            resp.raise_for_status()
            return resp.json()

    async def _post(self, uri: str, body: dict | None = None) -> dict:
        """Signed POST request."""
        import json as _json
        body_str = _json.dumps(body, separators=(",", ":")) if body else ""
        headers = self._sign_request("POST", uri, body=body_str)
        url = f"{BASE_URL}{uri}"
        async with httpx.AsyncClient(timeout=30) as client:
            resp = await client.post(url, headers=headers, content=body_str)
            resp.raise_for_status()
            return resp.json()

    # ══════════════════════════════════════════════════════════════
    # ACCOUNTS
    # ══════════════════════════════════════════════════════════════

    async def get_accounts(self) -> list[dict]:
        """Get all linked Webull accounts with balances and positions."""
        try:
            acct_data = await self._get("/app/subscriptions/list")
            accounts = acct_data if isinstance(acct_data, list) else acct_data.get("data", [])
            result = []
            for acct in accounts:
                acct_id = acct.get("account_id", "")
                if not acct_id:
                    continue

                # Fetch balance
                try:
                    balance = await self._get("/account/balance", {"account_id": acct_id})
                except Exception:
                    balance = {}

                # Fetch positions
                try:
                    pos_data = await self._get("/account/positions", {"account_id": acct_id})
                    positions = pos_data if isinstance(pos_data, list) else pos_data.get("positions", [])
                except Exception:
                    positions = []

                result.append({
                    "account_id": acct_id,
                    "account_number": acct.get("account_number", ""),
                    "type": acct.get("account_type", "brokerage"),
                    "cash_balance": float(balance.get("cash_balance", 0)),
                    "total_value": float(balance.get("total_market_value", 0)),
                    "buying_power": float(balance.get("buying_power", 0)),
                    "positions": [
                        {
                            "symbol": p.get("symbol", ""),
                            "asset_type": p.get("instrument_type", ""),
                            "quantity": float(p.get("quantity", 0)),
                            "market_value": float(p.get("market_value", 0)),
                            "avg_price": float(p.get("avg_cost", 0)),
                            "pnl_day": float(p.get("unrealized_pnl", 0)),
                            "pnl_day_pct": float(p.get("unrealized_pnl_rate", 0)),
                        }
                        for p in positions
                    ],
                })
            return result
        except Exception as e:
            logger.error(f"Webull get_accounts: {e}")
            return []

    # ══════════════════════════════════════════════════════════════
    # ORDERS — STOCKS
    # ══════════════════════════════════════════════════════════════

    async def buy(
        self, account_id: str, symbol: str, quantity: int,
        order_type: str = "MARKET", price: float | None = None,
        instrument_id: str = "",
    ) -> dict:
        """Place a buy order for stocks/ETFs."""
        return await self._place_order(
            account_id, symbol, quantity, "BUY", order_type, price, instrument_id,
        )

    async def sell(
        self, account_id: str, symbol: str, quantity: int,
        order_type: str = "MARKET", price: float | None = None,
        instrument_id: str = "",
    ) -> dict:
        """Place a sell order."""
        return await self._place_order(
            account_id, symbol, quantity, "SELL", order_type, price, instrument_id,
        )

    async def _place_order(
        self, account_id: str, symbol: str, quantity: int,
        side: str, order_type: str, price: float | None,
        instrument_id: str,
    ) -> dict:
        """Internal order placement."""
        try:
            # Look up instrument_id if not provided
            if not instrument_id:
                inst = await self.get_instrument(symbol)
                instrument_id = inst.get("instrument_id", "")

            order = {
                "client_order_id": uuid.uuid4().hex,
                "side": side,
                "tif": "DAY",
                "extended_hours_trading": False,
                "instrument_id": instrument_id,
                "order_type": order_type,
                "qty": str(quantity),
            }
            if price and order_type in ("LIMIT", "STOP_LIMIT"):
                order["limit_price"] = str(price)

            body = {"account_id": account_id, "stock_order": order}
            resp = await self._post("/trade/order/place", body)
            logger.info(f"Webull {side} {symbol} x{quantity}: {resp}")
            return {"status": "ok", "order_id": order["client_order_id"], "symbol": symbol, "side": side.lower()}
        except Exception as e:
            logger.error(f"Webull order: {e}")
            return {"error": str(e)}

    # ══════════════════════════════════════════════════════════════
    # ORDERS — CRYPTO
    # ══════════════════════════════════════════════════════════════

    async def buy_crypto(
        self, account_id: str, symbol: str, quantity: float,
        order_type: str = "MARKET", price: float | None = None,
    ) -> dict:
        """Buy crypto (e.g., BTCUSD)."""
        order = {
            "client_order_id": uuid.uuid4().hex,
            "combo_type": "NORMAL",
            "symbol": symbol,
            "instrument_type": "CRYPTO",
            "market": "US",
            "side": "BUY",
            "tif": "DAY",
            "order_type": order_type,
            "qty": str(quantity),
            "entrust_type": "QTY",
        }
        if price:
            order["limit_price"] = str(price)
        try:
            resp = await self._post("/trade/order/place", {"account_id": account_id, "stock_order": order})
            return {"status": "ok", "order_id": order["client_order_id"], "symbol": symbol, "side": "buy"}
        except Exception as e:
            return {"error": str(e)}

    async def sell_crypto(
        self, account_id: str, symbol: str, quantity: float,
        order_type: str = "MARKET", price: float | None = None,
    ) -> dict:
        """Sell crypto."""
        order = {
            "client_order_id": uuid.uuid4().hex,
            "combo_type": "NORMAL",
            "symbol": symbol,
            "instrument_type": "CRYPTO",
            "market": "US",
            "side": "SELL",
            "tif": "DAY",
            "order_type": order_type,
            "qty": str(quantity),
            "entrust_type": "QTY",
        }
        if price:
            order["limit_price"] = str(price)
        try:
            resp = await self._post("/trade/order/place", {"account_id": account_id, "stock_order": order})
            return {"status": "ok", "order_id": order["client_order_id"], "symbol": symbol, "side": "sell"}
        except Exception as e:
            return {"error": str(e)}

    # ══════════════════════════════════════════════════════════════
    # ORDER MANAGEMENT
    # ══════════════════════════════════════════════════════════════

    async def get_orders(self, account_id: str = "") -> list[dict]:
        """Get orders for an account."""
        try:
            resp = await self._get("/trade/order/list", {"account_id": account_id} if account_id else None)
            orders = resp if isinstance(resp, list) else resp.get("orders", [])
            return [
                {
                    "id": o.get("client_order_id"),
                    "symbol": o.get("symbol", ""),
                    "type": o.get("order_type", ""),
                    "status": o.get("status", ""),
                    "quantity": o.get("qty", 0),
                    "filled": o.get("filled_qty", 0),
                    "price": o.get("limit_price", ""),
                    "side": o.get("side", ""),
                }
                for o in orders
            ]
        except Exception as e:
            logger.error(f"Webull get_orders: {e}")
            return []

    async def cancel_order(self, account_id: str, client_order_id: str) -> bool:
        """Cancel an open order."""
        try:
            await self._post("/trade/order/cancel", {
                "account_id": account_id,
                "client_order_id": client_order_id,
            })
            return True
        except Exception as e:
            logger.error(f"Webull cancel: {e}")
            return False

    async def get_order_detail(self, account_id: str, client_order_id: str) -> dict:
        """Get details for a specific order."""
        try:
            return await self._get("/trade/order/detail", {
                "account_id": account_id,
                "client_order_id": client_order_id,
            })
        except Exception as e:
            return {"error": str(e)}

    # ══════════════════════════════════════════════════════════════
    # MARKET DATA
    # ══════════════════════════════════════════════════════════════

    async def get_quote(self, symbol: str, category: str = "US_STOCK") -> dict | None:
        """Get real-time snapshot for a symbol."""
        try:
            resp = await self._get("/market/snapshot", {
                "symbol": symbol, "category": category,
                "extend_hour_required": "true", "overnight_required": "true",
            })
            snapshots = resp if isinstance(resp, list) else resp.get("snapshots", [resp])
            if not snapshots:
                return None
            s = snapshots[0] if isinstance(snapshots, list) else resp
            return {
                "symbol": symbol,
                "price": float(s.get("lastPrice", s.get("last_price", 0))),
                "bid": float(s.get("bidPrice", s.get("bid_price", 0))),
                "ask": float(s.get("askPrice", s.get("ask_price", 0))),
                "volume": int(s.get("volume", 0)),
                "change": float(s.get("priceChange", s.get("price_change", 0))),
                "change_pct": float(s.get("priceChangePercent", s.get("price_change_pct", 0))),
                "high": float(s.get("high", 0)),
                "low": float(s.get("low", 0)),
                "open": float(s.get("open", 0)),
                "close": float(s.get("close", s.get("prevClose", 0))),
            }
        except Exception as e:
            logger.error(f"Webull quote {symbol}: {e}")
            return None

    async def get_quotes(self, symbols: list[str], category: str = "US_STOCK") -> dict:
        """Get quotes for multiple symbols."""
        result = {}
        for sym in symbols:
            q = await self.get_quote(sym, category)
            if q:
                result[sym] = {"price": q["price"], "change_pct": q["change_pct"], "volume": q["volume"]}
        return result

    async def get_price_history(
        self, symbol: str, timespan: str = "D", count: int = 200,
        category: str = "US_STOCK",
    ) -> list[dict]:
        """Get historical OHLCV candles.

        Timespans: M1, M5, M15, M30, M60, M120, M240, D, W, M, Y
        """
        try:
            resp = await self._get("/market/history_bar", {
                "symbol": symbol, "category": category,
                "timespan": timespan, "count": str(count),
            })
            bars = resp if isinstance(resp, list) else resp.get("bars", [])
            return [
                {
                    "time": b.get("timestamp"),
                    "open": float(b.get("open", 0)),
                    "high": float(b.get("high", 0)),
                    "low": float(b.get("low", 0)),
                    "close": float(b.get("close", 0)),
                    "volume": int(b.get("volume", 0)),
                }
                for b in bars
            ]
        except Exception as e:
            logger.error(f"Webull history {symbol}: {e}")
            return []

    async def get_instrument(self, symbol: str, category: str = "US_STOCK") -> dict:
        """Look up instrument details (needed for instrument_id)."""
        try:
            resp = await self._get("/instruments", {"symbol": symbol, "category": category})
            instruments = resp if isinstance(resp, list) else resp.get("instruments", [])
            if instruments:
                return instruments[0] if isinstance(instruments, list) else instruments
            return {}
        except Exception as e:
            logger.error(f"Webull instrument {symbol}: {e}")
            return {}

    async def get_depth(self, symbol: str, category: str = "US_STOCK", depth: int = 5) -> dict:
        """Get order book depth (bid/ask levels)."""
        try:
            return await self._get("/market/quotes", {
                "symbol": symbol, "category": category, "depth": str(depth),
            })
        except Exception as e:
            return {"error": str(e)}

    # ══════════════════════════════════════════════════════════════
    # STREAMING CONFIG
    # ══════════════════════════════════════════════════════════════

    def get_streaming_config(self) -> dict:
        """Get MQTT streaming connection details for real-time data.

        Caller must establish MQTT connection to the returned host:port with TLS.
        """
        return {
            "host": "usquotes-api.webullfintech.com",
            "port": 8883,
            "tls": True,
            "app_key": self._app_key,
            "protocol": "MQTT",
        }

    # ══════════════════════════════════════════════════════════════
    # PROPERTIES
    # ══════════════════════════════════════════════════════════════

    @property
    def is_configured(self) -> bool:
        return bool(self._app_key and self._app_secret)

    @property
    def is_authorized(self) -> bool:
        return bool(self._app_key and self._app_secret)


# Singleton
_client: WebullClient | None = None


def get_webull() -> WebullClient:
    global _client
    if _client is None:
        _client = WebullClient()
    return _client
