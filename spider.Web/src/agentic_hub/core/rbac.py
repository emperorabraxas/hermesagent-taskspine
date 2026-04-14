"""RBAC engine — role-based access control for agents, tools, and commands.

Three built-in roles:
  admin    — full access to everything
  operator — all agents + tools, no privileged commands (sudo, systemctl, etc.)
  viewer   — chat only, no tool execution, no shell, read-only

Permissions are stored as JSON lists in the roles table:
  [{"resource": "agent:*", "action": "invoke"},
   {"resource": "tool:read_file", "action": "execute"}, ...]

Wildcard matching: "agent:*" matches "agent:scholar", "agent:oracle", etc.
"""
from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import Any

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from agentic_hub.models.database import get_session_factory

logger = logging.getLogger(__name__)


@dataclass
class Permission:
    resource: str  # "agent:scholar", "tool:shell", "command:sudo", "pipeline:*"
    action: str    # "invoke", "execute", "read", "admin"

    def matches(self, resource: str, action: str) -> bool:
        """Check if this permission grants access to a resource+action."""
        if not self._resource_matches(resource):
            return False
        return self.action == "*" or self.action == action

    def _resource_matches(self, target: str) -> bool:
        if self.resource == "*":
            return True
        if self.resource == target:
            return True
        # Wildcard: "agent:*" matches "agent:scholar"
        if self.resource.endswith(":*"):
            prefix = self.resource[:-1]  # "agent:"
            return target.startswith(prefix)
        return False

    def to_dict(self) -> dict:
        return {"resource": self.resource, "action": self.action}

    @classmethod
    def from_dict(cls, d: dict) -> Permission:
        return cls(resource=d["resource"], action=d["action"])


# ── Built-in role definitions ──────────────────────────────────────

ADMIN_PERMISSIONS = [
    Permission("*", "*"),  # Full access
]

OPERATOR_PERMISSIONS = [
    Permission("agent:*", "invoke"),
    Permission("tool:read_file", "execute"),
    Permission("tool:write_file", "execute"),
    Permission("tool:list_dir", "execute"),
    Permission("tool:shell", "execute"),
    Permission("tool:web_fetch", "execute"),
    Permission("tool:rag_search", "execute"),
    Permission("tool:python_eval", "execute"),
    Permission("tool:entity_search", "execute"),
    Permission("pipeline:*", "execute"),
    Permission("dag:*", "execute"),
    # No command:sudo, command:systemctl, etc.
]

VIEWER_PERMISSIONS = [
    Permission("agent:scholar", "invoke"),
    Permission("agent:oracle", "invoke"),
    Permission("tool:rag_search", "execute"),
    Permission("tool:read_file", "execute"),
    Permission("tool:list_dir", "execute"),
    Permission("tool:entity_search", "execute"),
    # No shell, write, web_fetch, python_eval
]

BUILT_IN_ROLES: dict[str, list[Permission]] = {
    "admin": ADMIN_PERMISSIONS,
    "operator": OPERATOR_PERMISSIONS,
    "viewer": VIEWER_PERMISSIONS,
}


class RBACEngine:
    """Evaluate permissions for users based on their assigned roles."""

    def __init__(self):
        self._role_cache: dict[str, list[Permission]] = {}
        self._user_role_cache: dict[int, str] = {}

    async def ensure_built_in_roles(self) -> None:
        """Create built-in roles in DB if they don't exist."""
        from agentic_hub.models.rbac import Role

        factory = get_session_factory()
        async with factory() as session:
            for role_name, perms in BUILT_IN_ROLES.items():
                result = await session.execute(
                    select(Role).where(Role.name == role_name)
                )
                if result.scalar_one_or_none() is None:
                    role = Role(
                        name=role_name,
                        description=f"Built-in {role_name} role",
                        permissions=[p.to_dict() for p in perms],
                    )
                    session.add(role)
            await session.commit()
        logger.info("Built-in RBAC roles ensured")

    async def get_user_role(self, user_id: int = 1) -> str:
        """Get the role name for a user. Defaults to 'admin' if none assigned."""
        if user_id in self._user_role_cache:
            return self._user_role_cache[user_id]

        from agentic_hub.models.rbac import UserRole, Role

        factory = get_session_factory()
        async with factory() as session:
            result = await session.execute(
                select(Role.name)
                .join(UserRole, UserRole.role_id == Role.id)
                .where(UserRole.user_id == user_id)
            )
            role_name = result.scalar_one_or_none()

        if role_name is None:
            role_name = "admin"  # Default: single user gets admin

        self._user_role_cache[user_id] = role_name
        return role_name

    async def get_permissions(self, role_name: str) -> list[Permission]:
        """Get permissions for a role. Uses built-in definitions first, then DB."""
        if role_name in self._role_cache:
            return self._role_cache[role_name]

        if role_name in BUILT_IN_ROLES:
            perms = BUILT_IN_ROLES[role_name]
            self._role_cache[role_name] = perms
            return perms

        # Custom role from DB
        from agentic_hub.models.rbac import Role

        factory = get_session_factory()
        async with factory() as session:
            result = await session.execute(
                select(Role.permissions).where(Role.name == role_name)
            )
            perms_json = result.scalar_one_or_none()

        if perms_json is None:
            logger.warning(f"Role '{role_name}' not found, defaulting to admin")
            return BUILT_IN_ROLES["admin"]

        perms = [Permission.from_dict(p) for p in perms_json]
        self._role_cache[role_name] = perms
        return perms

    async def check_permission(
        self, user_id: int, resource: str, action: str
    ) -> bool:
        """Check if a user has permission for resource+action."""
        role_name = await self.get_user_role(user_id)
        permissions = await self.get_permissions(role_name)
        return any(p.matches(resource, action) for p in permissions)

    async def get_allowed_tools(self, user_id: int = 1) -> set[str] | None:
        """Get set of tool names allowed for a user. None = all tools allowed."""
        role_name = await self.get_user_role(user_id)
        permissions = await self.get_permissions(role_name)

        # Admin with wildcard = all tools
        if any(p.resource == "*" and p.action == "*" for p in permissions):
            return None  # No restriction

        allowed = set()
        for p in permissions:
            if p.action in ("execute", "*") and p.resource.startswith("tool:"):
                tool_name = p.resource.split(":", 1)[1]
                if tool_name == "*":
                    return None  # All tools
                allowed.add(tool_name)
        return allowed

    async def get_allowed_agents(self, user_id: int = 1) -> set[str] | None:
        """Get set of agent names allowed for a user. None = all agents allowed."""
        role_name = await self.get_user_role(user_id)
        permissions = await self.get_permissions(role_name)

        if any(p.resource == "*" and p.action == "*" for p in permissions):
            return None

        allowed = set()
        for p in permissions:
            if p.action in ("invoke", "*") and p.resource.startswith("agent:"):
                agent_name = p.resource.split(":", 1)[1]
                if agent_name == "*":
                    return None
                allowed.add(agent_name)
        return allowed

    async def assign_role(self, user_id: int, role_name: str) -> bool:
        """Assign a role to a user. Returns True if successful."""
        from agentic_hub.models.rbac import Role, UserRole

        factory = get_session_factory()
        async with factory() as session:
            # Find role
            result = await session.execute(
                select(Role.id).where(Role.name == role_name)
            )
            role_id = result.scalar_one_or_none()
            if role_id is None:
                return False

            # Remove existing role assignment
            from sqlalchemy import delete
            await session.execute(
                delete(UserRole).where(UserRole.user_id == user_id)
            )

            # Assign new role
            session.add(UserRole(user_id=user_id, role_id=role_id))
            await session.commit()

        # Clear cache
        self._user_role_cache.pop(user_id, None)
        logger.info(f"User {user_id} assigned role: {role_name}")
        return True

    def clear_cache(self) -> None:
        """Clear permission caches (call after role/permission changes)."""
        self._role_cache.clear()
        self._user_role_cache.clear()


# Singleton
_engine: RBACEngine | None = None


def get_rbac() -> RBACEngine:
    global _engine
    if _engine is None:
        _engine = RBACEngine()
    return _engine
