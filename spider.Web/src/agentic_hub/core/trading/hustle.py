"""Money Maker Hustle Engine — zero-capital revenue streams.

Tracks and coordinates all bootstrap income sources:
  1. Crypto airdrops / Coinbase Earn / testnet rewards
  2. Free-entry DFS contests (DraftKings, FanDuel, PrizePicks)
  3. Sportsbook sign-up bonuses (free bets)
  4. Referral programs (Coinbase, Cash App, Webull, etc.)
  5. Credit card sign-up bonuses (cashback churning)

Every dollar tracked. Goal: earn $600 for Series 65.
"""
from __future__ import annotations

import json
import logging
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)

DATA_DIR = Path(__file__).parent.parent.parent.parent.parent / "data"
EARNINGS_LOG = DATA_DIR / "earnings_log.jsonl"
OPPORTUNITIES_FILE = DATA_DIR / "opportunities.json"
GOAL = 600.0  # Series 65 exam + registration


@dataclass
class Opportunity:
    """A zero-cost money-making opportunity."""
    source: str          # airdrop, dfs, sportsbook, referral, credit_card
    name: str            # "Coinbase Earn - NEAR", "DK Free Contest - NFL"
    potential_value: float
    url: str = ""
    status: str = "open"  # open, claimed, completed, expired
    notes: str = ""
    found_at: float = 0.0

    def to_dict(self) -> dict:
        return {
            "source": self.source, "name": self.name,
            "potential_value": self.potential_value, "url": self.url,
            "status": self.status, "notes": self.notes,
            "found_at": self.found_at or time.time(),
        }


class HustleEngine:
    """Tracks zero-capital earnings and opportunities."""

    def __init__(self):
        self._opportunities: list[dict] = []
        self._load_opportunities()

    def _load_opportunities(self):
        if OPPORTUNITIES_FILE.exists():
            try:
                self._opportunities = json.loads(OPPORTUNITIES_FILE.read_text())
            except Exception:
                self._opportunities = []

    def _save_opportunities(self):
        OPPORTUNITIES_FILE.parent.mkdir(parents=True, exist_ok=True)
        OPPORTUNITIES_FILE.write_text(json.dumps(self._opportunities, indent=2))

    def add_opportunity(self, opp: Opportunity) -> None:
        """Track a new opportunity."""
        self._opportunities.append(opp.to_dict())
        self._save_opportunities()
        logger.info(f"Opportunity added: {opp.name} (${opp.potential_value})")

    def log_earning(
        self, source: str, amount: float, description: str, platform: str = ""
    ) -> dict:
        """Log actual money earned."""
        entry = {
            "timestamp": time.time(),
            "source": source,
            "amount": amount,
            "description": description,
            "platform": platform,
        }
        EARNINGS_LOG.parent.mkdir(parents=True, exist_ok=True)
        with open(EARNINGS_LOG, "a") as f:
            f.write(json.dumps(entry) + "\n")
        logger.info(f"Earned ${amount:.2f} from {source}: {description}")
        return entry

    def get_total_earnings(self) -> float:
        """Get total earned across all sources."""
        if not EARNINGS_LOG.exists():
            return 0.0
        total = 0.0
        for line in EARNINGS_LOG.read_text().strip().split("\n"):
            if line:
                try:
                    total += json.loads(line).get("amount", 0)
                except Exception:
                    pass
        return total

    def get_earnings_by_source(self) -> dict[str, float]:
        """Break down earnings by source."""
        breakdown: dict[str, float] = {}
        if not EARNINGS_LOG.exists():
            return breakdown
        for line in EARNINGS_LOG.read_text().strip().split("\n"):
            if line:
                try:
                    entry = json.loads(line)
                    src = entry.get("source", "other")
                    breakdown[src] = breakdown.get(src, 0) + entry.get("amount", 0)
                except Exception:
                    pass
        return breakdown

    def get_earnings_log(self, limit: int = 50) -> list[dict]:
        """Get recent earnings."""
        if not EARNINGS_LOG.exists():
            return []
        entries = []
        for line in EARNINGS_LOG.read_text().strip().split("\n"):
            if line:
                try:
                    entries.append(json.loads(line))
                except Exception:
                    pass
        return entries[-limit:]

    def get_progress(self) -> dict:
        """Get progress toward the $600 goal."""
        total = self.get_total_earnings()
        breakdown = self.get_earnings_by_source()
        return {
            "goal": GOAL,
            "earned": round(total, 2),
            "remaining": round(max(0, GOAL - total), 2),
            "progress_pct": round(min(100, total / GOAL * 100), 1),
            "breakdown": breakdown,
            "opportunities": len(self._opportunities),
            "active_opportunities": len([o for o in self._opportunities if o.get("status") == "open"]),
        }

    def get_opportunities(self, source: str = "", status: str = "") -> list[dict]:
        """Get tracked opportunities, optionally filtered."""
        opps = self._opportunities
        if source:
            opps = [o for o in opps if o.get("source") == source]
        if status:
            opps = [o for o in opps if o.get("status") == status]
        return opps

    def update_opportunity(self, name: str, status: str) -> bool:
        """Update an opportunity's status."""
        for opp in self._opportunities:
            if opp.get("name") == name:
                opp["status"] = status
                self._save_opportunities()
                return True
        return False

    def seed_opportunities(self) -> int:
        """Seed initial zero-cost opportunities."""
        seeds = [
            # Crypto
            Opportunity("airdrop", "Coinbase Earn - Learning Rewards", 30.0,
                       "https://www.coinbase.com/earn", notes="Watch videos, earn crypto. ~$3-5 per course."),
            Opportunity("airdrop", "Layer3 Quests", 20.0,
                       "https://layer3.xyz", notes="Complete onchain quests for token rewards."),
            Opportunity("airdrop", "Galxe Campaigns", 15.0,
                       "https://galxe.com", notes="Social + onchain tasks for NFTs/tokens."),
            Opportunity("airdrop", "Testnet Farming", 50.0,
                       notes="Interact with testnets (Monad, Berachain, etc.) for potential airdrops."),

            # DFS
            Opportunity("dfs", "DraftKings Free Contests", 25.0,
                       "https://www.draftkings.com", notes="Free-entry contests daily. NFL/NBA/MLB."),
            Opportunity("dfs", "FanDuel Free Contests", 25.0,
                       "https://www.fanduel.com", notes="Free-entry contests with real prizes."),
            Opportunity("dfs", "PrizePicks Free Entries", 15.0,
                       "https://www.prizepicks.com", notes="Free pick'em entries periodically."),
            Opportunity("dfs", "Underdog Fantasy Free", 15.0,
                       "https://underdogfantasy.com", notes="Free best-ball and pick'em contests."),

            # Sportsbook bonuses
            Opportunity("sportsbook", "DraftKings Sportsbook Signup", 200.0,
                       "https://sportsbook.draftkings.com", notes="Bet $5 get $200 in bonus bets. Free money."),
            Opportunity("sportsbook", "FanDuel Sportsbook Signup", 200.0,
                       "https://sportsbook.fanduel.com", notes="Bet $5 get $200 in bonus bets."),
            Opportunity("sportsbook", "BetMGM Signup Bonus", 158.0,
                       "https://sports.betmgm.com", notes="$158 bonus bet on signup."),
            Opportunity("sportsbook", "Caesars First Bet", 100.0,
                       "https://www.caesars.com/sportsbook-and-casino", notes="First bet insurance up to $1000."),

            # Referrals
            Opportunity("referral", "Coinbase Referrals", 50.0,
                       notes="$10 per referral. 5 friends = $50."),
            Opportunity("referral", "Cash App Referrals", 25.0,
                       notes="$5 per referral."),
            Opportunity("referral", "Webull Signup + Referral", 75.0,
                       "https://www.webull.com", notes="Free stocks on signup + referral bonuses."),

            # Credit cards
            Opportunity("credit_card", "Discover It Cashback Match", 150.0,
                       notes="All cashback doubled first year. $0 annual fee."),
            Opportunity("credit_card", "Chase Freedom Flex", 200.0,
                       notes="$200 bonus after $500 spend in 3 months. $0 annual fee."),
            Opportunity("credit_card", "Capital One Quicksilver", 200.0,
                       notes="$200 bonus after $500 spend. 1.5% unlimited cashback."),
        ]

        added = 0
        existing_names = {o.get("name") for o in self._opportunities}
        for seed in seeds:
            if seed.name not in existing_names:
                self.add_opportunity(seed)
                added += 1
        return added


# Singleton
_engine: HustleEngine | None = None


def get_hustle_engine() -> HustleEngine:
    global _engine
    if _engine is None:
        _engine = HustleEngine()
    return _engine
