"""Gamification engine — XP awards, level calculation, streak tracking."""
from __future__ import annotations

import math
import logging
import time
from collections import deque
from datetime import date, datetime, timezone

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from agentic_hub.models.gamification import XPEvent, Streak, User

logger = logging.getLogger(__name__)

# XP multipliers
LOCAL_MULTIPLIER = 1.5   # Bonus for using local models (incentivize privacy)
CLOUD_MULTIPLIER = 1.0
STREAK_DAILY_XP = 25     # Base XP per streak day
COMBO_WINDOW = 60        # Seconds for combo window


def calculate_level(total_xp: int) -> int:
    """Level = floor(sqrt(total_xp / 100)). Level 1 at 100 XP, level 10 at 10k."""
    if total_xp < 100:
        return 0
    return int(math.floor(math.sqrt(total_xp / 100)))


def xp_for_level(level: int) -> int:
    """XP required to reach a given level."""
    return level * level * 100


def xp_to_next_level(total_xp: int) -> tuple[int, int]:
    """Returns (xp_needed, xp_into_current_level)."""
    current = calculate_level(total_xp)
    next_level_xp = xp_for_level(current + 1)
    current_level_xp = xp_for_level(current)
    return next_level_xp - total_xp, total_xp - current_level_xp


class GamificationEngine:
    """Manages XP awards, levels, streaks, and combos."""

    # Combo tracking — per user
    _combo_timestamps: dict[int, deque] = {}

    def _get_combo_multiplier(self, user_id: int) -> float:
        """Calculate combo multiplier based on recent message frequency."""
        now = time.time()
        q = self._combo_timestamps.setdefault(user_id, deque())
        while q and now - q[0] > COMBO_WINDOW:
            q.popleft()
        q.append(now)
        count = len(q)
        if count >= 5:
            return 3.0
        if count >= 3:
            return 2.0
        if count >= 2:
            return 1.5
        return 1.0

    async def award_xp(
        self,
        session: AsyncSession,
        agent: str,
        base_xp: int,
        reason: str,
        source: str,
        model_used: str = "",
        user_id: int = 1,
    ) -> dict:
        """Award XP for an interaction. Returns XP details."""
        source_mult = LOCAL_MULTIPLIER if source == "local" else CLOUD_MULTIPLIER
        combo_mult = self._get_combo_multiplier(user_id)
        multiplier = source_mult * combo_mult
        xp_amount = int(base_xp * multiplier)

        event = XPEvent(
            user_id=user_id,
            agent=agent,
            xp_amount=xp_amount,
            reason=reason,
            source=source,
            model_used=model_used,
        )
        session.add(event)

        # Update streak
        streak_info = await self._update_streak(session, user_id)

        # Add streak bonus
        streak_bonus = 0
        if streak_info["current_streak"] > 0:
            streak_bonus = int(STREAK_DAILY_XP * (1 + streak_info["current_streak"] * 0.1))
            # Only award streak bonus once per day
            if streak_info["streak_just_extended"]:
                streak_event = XPEvent(
                    user_id=user_id,
                    agent="system",
                    xp_amount=streak_bonus,
                    reason=f"streak_day_{streak_info['current_streak']}",
                    source="system",
                )
                session.add(streak_event)

        await session.flush()

        # Get total XP
        total = await self.get_total_xp(session, user_id)
        level = calculate_level(total)
        xp_needed, xp_progress = xp_to_next_level(total)

        return {
            "xp_earned": xp_amount,
            "streak_bonus": streak_bonus if streak_info.get("streak_just_extended") else 0,
            "total_xp": total,
            "level": level,
            "xp_to_next_level": xp_needed,
            "current_streak": streak_info["current_streak"],
            "source": source,
            "multiplier": multiplier,
            "combo_multiplier": combo_mult,
        }

    async def _update_streak(self, session: AsyncSession, user_id: int) -> dict:
        """Update the user's streak. Returns streak info."""
        result = await session.execute(
            select(Streak).where(Streak.user_id == user_id)
        )
        streak = result.scalar_one_or_none()

        if not streak:
            streak = Streak(user_id=user_id, current_streak=0, longest_streak=0)
            session.add(streak)

        today = date.today()
        streak_just_extended = False

        if streak.last_active_date is None:
            # First ever activity
            streak.current_streak = 1
            streak.longest_streak = 1
            streak.last_active_date = today
            streak_just_extended = True
        elif streak.last_active_date == today:
            # Already active today, no change
            pass
        elif (today - streak.last_active_date).days == 1:
            # Consecutive day — extend streak
            streak.current_streak += 1
            streak.longest_streak = max(streak.longest_streak, streak.current_streak)
            streak.last_active_date = today
            streak_just_extended = True
        else:
            # Streak broken — reset
            streak.current_streak = 1
            streak.last_active_date = today
            streak_just_extended = True

        return {
            "current_streak": streak.current_streak,
            "longest_streak": streak.longest_streak,
            "streak_just_extended": streak_just_extended,
        }

    async def get_total_xp(self, session: AsyncSession, user_id: int = 1) -> int:
        """Get total XP for a user."""
        result = await session.execute(
            select(func.coalesce(func.sum(XPEvent.xp_amount), 0)).where(
                XPEvent.user_id == user_id
            )
        )
        return result.scalar()

    async def get_stats(self, session: AsyncSession, user_id: int = 1) -> dict:
        """Get full gamification stats."""
        total_xp = await self.get_total_xp(session, user_id)
        level = calculate_level(total_xp)
        xp_needed, xp_progress = xp_to_next_level(total_xp)

        # Streak
        result = await session.execute(
            select(Streak).where(Streak.user_id == user_id)
        )
        streak = result.scalar_one_or_none()

        # Interaction counts by agent
        agent_counts = await session.execute(
            select(XPEvent.agent, func.count(XPEvent.id), func.sum(XPEvent.xp_amount))
            .where(XPEvent.user_id == user_id)
            .group_by(XPEvent.agent)
        )
        agent_stats = {
            row[0]: {"count": row[1], "total_xp": row[2]}
            for row in agent_counts.all()
        }

        # Local vs cloud
        source_counts = await session.execute(
            select(XPEvent.source, func.count(XPEvent.id))
            .where(XPEvent.user_id == user_id)
            .group_by(XPEvent.source)
        )
        source_stats = {row[0]: row[1] for row in source_counts.all()}

        return {
            "total_xp": total_xp,
            "level": level,
            "xp_to_next_level": xp_needed,
            "xp_progress_in_level": xp_progress,
            "next_level_total_xp": xp_for_level(level + 1),
            "streak": {
                "current": streak.current_streak if streak else 0,
                "longest": streak.longest_streak if streak else 0,
                "last_active": str(streak.last_active_date) if streak and streak.last_active_date else None,
            },
            "agents": agent_stats,
            "sources": source_stats,
        }
