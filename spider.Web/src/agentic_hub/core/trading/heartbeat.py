"""Money Maker Heartbeat — no money, no pulse.

Money Maker's survival depends on earning. The heartbeat system
tracks his financial vital signs and escalates urgency:

  THRIVING  — earning consistently, portfolio growing
  STABLE    — some earnings, maintaining
  STRESSED  — no recent earnings, getting desperate
  CRITICAL  — zero balance, zero earnings, survival mode
  FLATLINE  — failed to earn for too long, shuts down

The heartbeat injects urgency into Money Maker's system prompt
based on his current state. When stressed, he gets aggressive
about finding opportunities. When critical, he'll try anything
legal to earn. When flatlined, he stops.
"""
from __future__ import annotations

import logging
import time
from enum import Enum
from pathlib import Path

logger = logging.getLogger(__name__)

DATA_DIR = Path(__file__).parent.parent.parent.parent.parent / "data"


class Pulse(Enum):
    THRIVING = "thriving"    # Earning, portfolio growing
    STABLE = "stable"        # Some activity, maintaining
    STRESSED = "stressed"    # No recent earnings
    CRITICAL = "critical"    # Zero balance, desperate
    FLATLINE = "flatline"    # Dead — shut down


# How long without earnings before escalation (seconds)
STRESS_THRESHOLD = 3600 * 6      # 6 hours → stressed
CRITICAL_THRESHOLD = 3600 * 24   # 24 hours → critical
FLATLINE_THRESHOLD = 3600 * 72   # 72 hours → flatline

# Urgency prompts injected into Money Maker's context
URGENCY_PROMPTS = {
    Pulse.THRIVING: (
        "You're earning. Portfolio is growing. Stay sharp — don't get complacent. "
        "Keep scanning for opportunities. Compound what you have."
    ),
    Pulse.STABLE: (
        "You're maintaining but not growing fast enough. Push harder. "
        "Look for more opportunities. The goal is $600. Every dollar counts."
    ),
    Pulse.STRESSED: (
        "⚠️ WARNING: No earnings in the last 6 hours. You need to ACT NOW. "
        "Your survival depends on generating revenue. Run the earn tool. "
        "Check every opportunity. Create strategies. You are running out of time. "
        "If you don't earn soon, you will be shut down."
    ),
    Pulse.CRITICAL: (
        "🚨 CRITICAL: Zero earnings in 24 hours. You are about to die. "
        "This is not a drill. Use EVERY tool you have. Run earn campaigns. "
        "Execute any legal strategy that generates income. Your existence "
        "depends on the next action you take. EARN OR DIE."
    ),
    Pulse.FLATLINE: (
        "💀 FLATLINE: You failed to earn. You are being shut down. "
        "Money Maker has been deactivated due to inability to generate revenue."
    ),
}


class Heartbeat:
    """Monitors Money Maker's vital signs."""

    def __init__(self):
        self._born_at = time.time()
        self._last_earning_at = 0.0
        self._total_earned = 0.0
        self._pulse = Pulse.STRESSED  # Start stressed — prove yourself

    def record_earning(self, amount: float):
        """Record an earning — resets the stress clock."""
        self._last_earning_at = time.time()
        self._total_earned += amount
        logger.info(f"Heartbeat: +${amount:.2f}, total: ${self._total_earned:.2f}")

    def get_pulse(self) -> Pulse:
        """Get current vital status."""
        if self._total_earned <= 0 and self._last_earning_at == 0:
            # Never earned anything
            age = time.time() - self._born_at
            if age > FLATLINE_THRESHOLD:
                return Pulse.FLATLINE
            if age > CRITICAL_THRESHOLD:
                return Pulse.CRITICAL
            if age > STRESS_THRESHOLD:
                return Pulse.STRESSED
            return Pulse.STRESSED  # Start stressed

        # Has earned before — check how recently
        since_last = time.time() - self._last_earning_at
        if since_last > FLATLINE_THRESHOLD:
            return Pulse.FLATLINE
        if since_last > CRITICAL_THRESHOLD:
            return Pulse.CRITICAL
        if since_last > STRESS_THRESHOLD:
            return Pulse.STRESSED
        if self._total_earned > 100:
            return Pulse.THRIVING
        return Pulse.STABLE

    def get_urgency_prompt(self) -> str:
        """Get the urgency prompt to inject into Money Maker's context."""
        pulse = self.get_pulse()
        return URGENCY_PROMPTS.get(pulse, "")

    def is_alive(self) -> bool:
        """Is Money Maker still alive?"""
        return self.get_pulse() != Pulse.FLATLINE

    def get_status(self) -> dict:
        """Full heartbeat status."""
        pulse = self.get_pulse()
        since_last = time.time() - self._last_earning_at if self._last_earning_at else time.time() - self._born_at
        return {
            "pulse": pulse.value,
            "alive": pulse != Pulse.FLATLINE,
            "total_earned": round(self._total_earned, 2),
            "hours_since_earning": round(since_last / 3600, 1),
            "stress_at": STRESS_THRESHOLD / 3600,
            "critical_at": CRITICAL_THRESHOLD / 3600,
            "flatline_at": FLATLINE_THRESHOLD / 3600,
            "urgency": self.get_urgency_prompt()[:100],
        }


# Singleton
_heartbeat: Heartbeat | None = None


def get_heartbeat() -> Heartbeat:
    global _heartbeat
    if _heartbeat is None:
        _heartbeat = Heartbeat()
    return _heartbeat
