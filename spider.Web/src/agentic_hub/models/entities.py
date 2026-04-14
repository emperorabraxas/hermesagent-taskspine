"""Entity Memory database models — knowledge graph for cross-session memory."""
from __future__ import annotations

from sqlalchemy import (
    Column, Integer, String, DateTime, Float, Text, ForeignKey, UniqueConstraint,
)
from sqlalchemy.sql import func

from agentic_hub.models.database import Base


class Entity(Base):
    __tablename__ = "entities"

    id = Column(Integer, primary_key=True)
    name = Column(String(200), nullable=False)
    entity_type = Column(String(50), nullable=False)  # project, person, stock, tool, concept, account
    description = Column(Text, default="")
    mention_count = Column(Integer, default=1)
    first_seen = Column(DateTime(timezone=True), server_default=func.now())
    last_seen = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    __table_args__ = (
        UniqueConstraint("name", "entity_type", name="uq_entity_name_type"),
    )


class EntityRelation(Base):
    __tablename__ = "entity_relations"

    id = Column(Integer, primary_key=True)
    source_id = Column(Integer, ForeignKey("entities.id", ondelete="CASCADE"), nullable=False)
    target_id = Column(Integer, ForeignKey("entities.id", ondelete="CASCADE"), nullable=False)
    relation_type = Column(String(50), nullable=False)  # uses, contains, depends_on, trades, deploys_to
    confidence = Column(Float, default=1.0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    __table_args__ = (
        UniqueConstraint("source_id", "target_id", "relation_type", name="uq_entity_relation"),
    )


class EntityMention(Base):
    __tablename__ = "entity_mentions"

    id = Column(Integer, primary_key=True)
    entity_id = Column(Integer, ForeignKey("entities.id", ondelete="CASCADE"), nullable=False)
    conversation_id = Column(String(64), default="")
    context_snippet = Column(Text, default="")  # Surrounding text
    created_at = Column(DateTime(timezone=True), server_default=func.now())
