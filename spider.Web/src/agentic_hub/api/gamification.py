"""Gamification API endpoints — XP, achievements, stats."""
from __future__ import annotations

from fastapi import APIRouter

from agentic_hub.gamification.achievements import AchievementChecker, ACHIEVEMENTS
from agentic_hub.gamification.engine import GamificationEngine
from agentic_hub.models.database import get_session_factory

router = APIRouter(prefix="/api/game", tags=["gamification"])


@router.get("/stats")
async def get_stats():
    """Get full gamification stats (XP, level, streak, agent breakdown)."""
    engine = GamificationEngine()
    factory = get_session_factory()
    async with factory() as session:
        stats = await engine.get_stats(session)
    return stats


@router.get("/achievements")
async def get_achievements():
    """Get all achievements with unlock status."""
    checker = AchievementChecker()
    factory = get_session_factory()
    async with factory() as session:
        achievements = await checker.get_all_achievements(session)
    return {"achievements": achievements}


@router.get("/achievements/available")
async def get_available_achievements():
    """Get all achievement definitions."""
    return {
        "achievements": [
            {
                "key": d.key,
                "name": d.name,
                "description": d.description,
                "icon": d.icon,
            }
            for d in ACHIEVEMENTS.values()
        ]
    }
