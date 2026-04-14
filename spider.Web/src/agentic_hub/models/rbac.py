"""RBAC database models — roles and user-role assignments."""
from __future__ import annotations

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, UniqueConstraint, JSON
from sqlalchemy.sql import func

from agentic_hub.models.database import Base


class Role(Base):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True, nullable=False)
    description = Column(String(200), default="")
    permissions = Column(JSON, nullable=False, default=list)  # list of permission dicts
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class UserRole(Base):
    __tablename__ = "user_roles"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    role_id = Column(Integer, ForeignKey("roles.id"), nullable=False)
    granted_at = Column(DateTime(timezone=True), server_default=func.now())

    __table_args__ = (
        UniqueConstraint("user_id", "role_id", name="uq_user_role"),
    )
