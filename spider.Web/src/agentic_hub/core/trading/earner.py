"""Money Maker Earner — automated Coinbase Earn via CamoufFox.

Navigates coinbase.com/earn, finds available learn & earn campaigns,
watches videos, answers quizzes, claims free crypto.

This is Coinbase's own educational rewards program — they pay you
to learn about crypto projects. We're just automating it.

Uses CamoufFox (anti-detection Firefox) + Playwright for automation.
"""
from __future__ import annotations

import asyncio
import json
import logging
import time
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)

DATA_DIR = Path(__file__).parent.parent.parent.parent.parent / "data"
EARN_LOG = DATA_DIR / "earn_log.jsonl"


class CoinbaseEarner:
    """Automates Coinbase Earn campaigns."""

    def __init__(self):
        self._browser = None
        self._page = None

    async def run_earn(self) -> list[dict]:
        """Run through all available Coinbase Earn campaigns.

        Returns list of earned rewards.
        """
        from camoufox.async_api import AsyncCamoufox

        earned = []
        logger.info("Starting Coinbase Earn automation...")

        async with AsyncCamoufox(headless=False) as browser:
            page = await browser.new_page()

            # Navigate to Coinbase Earn
            await page.goto("https://www.coinbase.com/earn", wait_until="networkidle", timeout=30000)
            await asyncio.sleep(3)

            # Check if logged in
            current_url = page.url
            if "signin" in current_url or "login" in current_url:
                logger.info("Not logged in — need to authenticate first")
                # Wait for user to log in manually
                logger.info("Please log into Coinbase in the browser window...")
                # Wait up to 5 minutes for login
                for _ in range(60):
                    await asyncio.sleep(5)
                    if "earn" in page.url:
                        break
                if "earn" not in page.url:
                    logger.error("Login timeout — user didn't authenticate")
                    return []

            logger.info("Logged in — scanning for earn campaigns...")

            # Find available earn campaigns
            campaigns = await self._find_campaigns(page)
            logger.info(f"Found {len(campaigns)} available campaigns")

            for campaign in campaigns:
                try:
                    result = await self._complete_campaign(page, campaign)
                    if result:
                        earned.append(result)
                        self._log_earning(result)
                        logger.info(f"Earned: {result}")
                except Exception as e:
                    logger.warning(f"Campaign failed: {campaign.get('name', '?')}: {e}")

            await page.close()

        return earned

    async def _find_campaigns(self, page) -> list[dict]:
        """Find available earn campaigns on the page."""
        campaigns = []
        try:
            # Look for earn campaign cards
            # Coinbase uses various selectors — try common patterns
            cards = await page.query_selector_all('[data-testid*="earn"], .earn-card, [href*="/earn/"]')

            if not cards:
                # Try broader search
                cards = await page.query_selector_all('a[href*="/earn/"]')

            for card in cards:
                try:
                    href = await card.get_attribute("href") or ""
                    text = await card.inner_text()
                    if "/earn/" in href and text:
                        campaigns.append({
                            "name": text.split("\n")[0][:50],
                            "url": href if href.startswith("http") else f"https://www.coinbase.com{href}",
                        })
                except Exception:
                    pass

            # Deduplicate
            seen = set()
            unique = []
            for c in campaigns:
                if c["url"] not in seen:
                    seen.add(c["url"])
                    unique.append(c)
            campaigns = unique

        except Exception as e:
            logger.warning(f"Campaign scan failed: {e}")

        return campaigns

    async def _complete_campaign(self, page, campaign: dict) -> dict | None:
        """Navigate to a campaign, watch video, answer quiz."""
        name = campaign.get("name", "Unknown")
        url = campaign.get("url", "")
        if not url:
            return None

        logger.info(f"Starting campaign: {name}")
        await page.goto(url, wait_until="networkidle", timeout=30000)
        await asyncio.sleep(3)

        # Look for "Start" or "Begin" button
        start_btn = await page.query_selector(
            'button:has-text("Start"), button:has-text("Begin"), '
            'button:has-text("Watch video"), button:has-text("Start lesson")'
        )
        if start_btn:
            await start_btn.click()
            await asyncio.sleep(5)

        # Wait for video to play (if any)
        video = await page.query_selector("video")
        if video:
            logger.info(f"  Watching video for {name}...")
            # Wait for video to finish (max 3 min)
            for _ in range(36):
                await asyncio.sleep(5)
                ended = await page.evaluate("() => { const v = document.querySelector('video'); return v ? v.ended : true; }")
                if ended:
                    break

        # Look for quiz / questions
        answered = 0
        for attempt in range(5):
            # Find quiz options
            options = await page.query_selector_all(
                '[data-testid*="answer"], [data-testid*="option"], '
                '.quiz-option, button[class*="answer"]'
            )
            if not options:
                break

            # Click first option (many Coinbase quizzes accept any answer)
            for opt in options:
                try:
                    await opt.click()
                    answered += 1
                    await asyncio.sleep(2)
                    break
                except Exception:
                    continue

            # Look for "Next" or "Continue" button
            next_btn = await page.query_selector(
                'button:has-text("Next"), button:has-text("Continue"), '
                'button:has-text("Submit"), button:has-text("Claim")'
            )
            if next_btn:
                await next_btn.click()
                await asyncio.sleep(3)

        # Check for reward claim
        claim_btn = await page.query_selector(
            'button:has-text("Claim"), button:has-text("Done"), '
            'button:has-text("Complete")'
        )
        if claim_btn:
            await claim_btn.click()
            await asyncio.sleep(3)
            logger.info(f"  Claimed reward for {name}")
            return {
                "campaign": name,
                "url": url,
                "answered": answered,
                "timestamp": time.time(),
                "status": "claimed",
            }

        if answered > 0:
            return {
                "campaign": name,
                "url": url,
                "answered": answered,
                "timestamp": time.time(),
                "status": "completed",
            }

        return None

    def _log_earning(self, result: dict):
        """Log earning to JSONL."""
        EARN_LOG.parent.mkdir(parents=True, exist_ok=True)
        with open(EARN_LOG, "a") as f:
            f.write(json.dumps(result) + "\n")

        # Also log to hustle engine
        try:
            from agentic_hub.core.trading.hustle import get_hustle_engine
            engine = get_hustle_engine()
            engine.log_earning(
                source="coinbase_earn",
                amount=3.0,  # Estimate — actual amount varies per campaign
                description=f"Coinbase Earn: {result.get('campaign', '?')}",
                platform="coinbase",
            )
        except Exception:
            pass

    async def check_available(self) -> int:
        """Quick check how many earn campaigns are available (headless)."""
        from camoufox.async_api import AsyncCamoufox

        try:
            async with AsyncCamoufox(headless=True) as browser:
                page = await browser.new_page()
                await page.goto("https://www.coinbase.com/earn", timeout=15000)
                await asyncio.sleep(3)
                cards = await page.query_selector_all('a[href*="/earn/"]')
                await page.close()
                return len(cards)
        except Exception:
            return -1


async def run_coinbase_earn() -> list[dict]:
    """Convenience function to run Coinbase Earn automation."""
    earner = CoinbaseEarner()
    return await earner.run_earn()
