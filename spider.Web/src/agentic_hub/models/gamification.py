"""Gamification database models — XP, achievements, streaks."""
from __future__ import annotations

from datetime import datetime, date

from sqlalchemy import (
    Column, Integer, String, DateTime, Date, Boolean, Text, ForeignKey, UniqueConstraint
)
from sqlalchemy.sql import func

from agentic_hub.models.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False, default="spider.BOB")
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class XPEvent(Base):
    __tablename__ = "xp_events"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, default=1)
    agent = Column(String(20), nullable=False)      # scholar, automator, oracle, code_team
    xp_amount = Column(Integer, nullable=False)
    reason = Column(String(100), nullable=False)     # chat_completion, code_generation, etc.
    source = Column(String(20), nullable=False)      # local, cloud, council, money_maker, idle, etc.
    model_used = Column(String(50), default="")
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class Achievement(Base):
    __tablename__ = "achievements"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, default=1)
    achievement_key = Column(String(50), nullable=False)
    unlocked_at = Column(DateTime(timezone=True), server_default=func.now())

    __table_args__ = (
        UniqueConstraint("user_id", "achievement_key", name="uq_user_achievement"),
    )


class Streak(Base):
    __tablename__ = "streaks"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, default=1)
    current_streak = Column(Integer, default=0)
    longest_streak = Column(Integer, default=0)
    last_active_date = Column(Date, nullable=True)

    __table_args__ = (
        UniqueConstraint("user_id", name="uq_user_streak"),
    )


class Conversation(Base):
    __tablename__ = "conversations"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, default=1)
    session_id = Column(String(64), unique=True, nullable=False)
    agent = Column(String(20), default="")
    title = Column(String(200), default="")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())


class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True)
    conversation_id = Column(Integer, ForeignKey("conversations.id", ondelete="CASCADE"), nullable=False)
    role = Column(String(10), nullable=False)        # user, assistant, system
    content = Column(Text, nullable=False)
    agent = Column(String(20), default="")
    model_used = Column(String(50), default="")
    source = Column(String(10), default="")          # local or cloud
    tokens_in = Column(Integer, default=0)
    tokens_out = Column(Integer, default=0)
    latency_ms = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
