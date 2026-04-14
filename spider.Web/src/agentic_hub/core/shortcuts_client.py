"""Apple Shortcuts integration — outbound notifications via Pushcut + IFTTT.

Spiders can reach the user's iPhone through push notifications that trigger
Shortcuts on the device. Pushcut is primary, IFTTT is fallback.

Flow: Spider event → ShortcutsClient.send() → Pushcut webhook → iPhone notification → Shortcut fires
"""
from __future__ import annotations

import logging
from typing import Any

import httpx

from agentic_hub.config import get_settings

logger = logging.getLogger(__name__)


class ShortcutsClient:
    """Outbound iPhone notification client — Pushcut (primary) + IFTTT (fallback)."""

    def __init__(self):
        settings = get_settings()
        self._pushcut_key = settings.pushcut_api_key or ""
        self._pushcut_url = settings.pushcut_webhook_url or "https://api.pushcut.io"
        self._ifttt_key = getattr(settings, "ifttt_webhook_key", "") or ""

    @property
    def has_pushcut(self) -> bool:
        return bool(self._pushcut_key)

    @property
    def has_ifttt(self) -> bool:
        return bool(self._ifttt_key)

    @property
    def is_configured(self) -> bool:
        return self.has_pushcut or self.has_ifttt

    # ── Pushcut (primary) ─────────────────────────────────────────

    async def _pushcut_send(self, notification_name: str, title: str, text: str, **kwargs) -> dict:
        """Send a Pushcut notification that can trigger a Shortcut on iPhone."""
        if not self.has_pushcut:
            return {"error": "Pushcut not configured"}
        url = f"{self._pushcut_url}/v1/notifications/{notification_name}"
        payload: dict[str, Any] = {"title": title, "text": text}
        if kwargs.get("sound") is not None:
            payload["sound"] = kwargs["sound"]
        if kwargs.get("url"):
            payload["defaultAction"] = {"url": kwargs["url"]}
        if kwargs.get("input"):
            payload["input"] = kwargs["input"]
        try:
            async with httpx.AsyncClient() as client:
                resp = await client.post(
                    url, json=payload,
                    headers={"API-Key": self._pushcut_key},
                    timeout=10,
                )
                return {"status": resp.status_code, "ok": resp.is_success}
        except Exception as e:
            logger.warning(f"Pushcut send failed: {e}")
            return {"error": str(e)}

    # ── IFTTT (fallback) ──────────────────────────────────────────

    async def _ifttt_send(self, event: str, value1: str = "", value2: str = "", value3: str = "") -> dict:
        """Trigger an IFTTT Maker webhook."""
        if not self.has_ifttt:
            return {"error": "IFTTT not configured"}
        url = f"https://maker.ifttt.com/trigger/{event}/with/key/{self._ifttt_key}"
        payload = {}
        if value1:
            payload["value1"] = value1
        if value2:
            payload["value2"] = value2
        if value3:
            payload["value3"] = value3
        try:
            async with httpx.AsyncClient() as client:
                resp = await client.post(url, json=payload, timeout=10)
                return {"status": resp.status_code, "ok": resp.is_success}
        except Exception as e:
            logger.warning(f"IFTTT send failed: {e}")
            return {"error": str(e)}

    # ── Smart routing ─────────────────────────────────────────────

    async def send(self, title: str, text: str, notification_name: str = "spider_alert", **kwargs) -> dict:
        """Send notification — tries Pushcut first, falls back to IFTTT."""
        if self.has_pushcut:
            result = await self._pushcut_send(notification_name, title, text, **kwargs)
            if result.get("ok"):
                return {**result, "provider": "pushcut"}
        if self.has_ifttt:
            result = await self._ifttt_send("spider_alert", title, text)
            if result.get("ok"):
                return {**result, "provider": "ifttt"}
        return {"error": "No notification provider configured", "ok": False}

    # ── Convenience methods ───────────────────────────────────────

    async def notify(self, title: str, text: str, sound: bool = True) -> dict:
        """General notification."""
        return await self.send(title, text, notification_name="spider_alert", sound=sound)

    async def alert_trade(self, action: str, symbol: str, qty: float = 0, price: float = 0) -> dict:
        """Trade execution alert."""
        title = f"Wirelash: {action.upper()} {symbol}"
        text = f"{action} {qty} {symbol} @ ${price:.2f}" if qty else f"{action} {symbol}"
        return await self.send(title, text, notification_name="trade_alert")

    async def alert_spider(self, spider: str, status: str, text: str = "") -> dict:
        """Spider status change alert."""
        title = f"{spider}: {status}"
        return await self.send(title, text or status, notification_name="spider_status")

    async def alert_price(self, symbol: str, price: float, condition: str, threshold: float) -> dict:
        """Price threshold alert."""
        title = f"Price Alert: {symbol} ${price:.2f}"
        text = f"{symbol} {condition} ${threshold:.2f} — now ${price:.2f}"
        return await self.send(title, text, notification_name="price_alert")

    async def alert_briefing(self, summary: str) -> dict:
        """Market briefing notification."""
        return await self.send("Market Briefing", summary[:200], notification_name="daily_briefing")

    # ── IFTTT convenience ─────────────────────────────────────────

    async def ifttt_trigger(self, event: str, value1: str = "", value2: str = "", value3: str = "") -> dict:
        """Direct IFTTT trigger."""
        return await self._ifttt_send(event, value1, value2, value3)


# ── Singleton ─────────────────────────────────────────────────────

_instance: ShortcutsClient | None = None


def get_shortcuts_client() -> ShortcutsClient:
    global _instance
    if _instance is None:
        _instance = ShortcutsClient()
    return _instance
