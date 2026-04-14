"""Human-in-the-Loop (HITL) breakpoint manager.

Enables agents to pause mid-workflow and request user input:
  - APPROVAL: Yes/No decision
  - CHOICE: Pick from multiple options
  - TEXT_INPUT: Free-form text response
  - REVIEW: Review and optionally edit content
  - CONFIRMATION: Proceed/Abort before destructive action

Works via WebSocket (Phase 3):
  1. Agent creates HITLRequest → HITLManager sends over WS
  2. DAG executor blocks on asyncio.Event
  3. User responds via WS → HITLManager signals event
  4. Execution resumes with user's response
"""
from __future__ import annotations

import asyncio
import json
import logging
import uuid
from dataclasses import dataclass, field
from enum import Enum
from typing import Any

logger = logging.getLogger(__name__)


class HITLType(Enum):
    APPROVAL = "approval"           # Yes/No
    CHOICE = "choice"               # Pick from options
    TEXT_INPUT = "text_input"        # Free-form text
    REVIEW = "review"               # Review + edit content
    CONFIRMATION = "confirmation"   # Proceed/Abort


@dataclass
class HITLRequest:
    request_id: str
    type: HITLType
    prompt: str                                     # What to ask the user
    options: list[str] = field(default_factory=list) # For CHOICE type
    context: str = ""                               # Additional context/content to review
    timeout_seconds: int = 300                      # Auto-proceed after 5 min
    default_action: str = "timeout"                 # What happens on timeout
    agent: str = ""                                 # Which agent is asking
    node_id: str = ""                               # DAG node that triggered this

    def to_dict(self) -> dict:
        return {
            "request_id": self.request_id,
            "type": self.type.value,
            "prompt": self.prompt,
            "options": self.options,
            "context": self.context,
            "timeout_seconds": self.timeout_seconds,
            "default_action": self.default_action,
            "agent": self.agent,
            "node_id": self.node_id,
        }


@dataclass
class HITLResponse:
    request_id: str
    action: str          # "approve", "reject", option text, user text, etc.
    user_input: str = "" # For TEXT_INPUT and REVIEW types

    @classmethod
    def from_dict(cls, d: dict) -> HITLResponse:
        return cls(
            request_id=d.get("request_id", ""),
            action=d.get("action", ""),
            user_input=d.get("user_input", ""),
        )


class HITLManager:
    """Manages human-in-the-loop breakpoints.

    When an agent needs user input, it creates an HITLRequest.
    The manager sends the request over WebSocket and blocks until
    the user responds or times out.
    """

    def __init__(self):
        self._pending: dict[str, asyncio.Event] = {}
        self._responses: dict[str, HITLResponse] = {}
        self._requests: dict[str, HITLRequest] = {}

    async def request_input(self, request: HITLRequest) -> HITLResponse:
        """Send HITL request and wait for user response.

        This is called by the DAG executor or orchestrator when an agent
        needs user input. It blocks until the user responds or times out.
        """
        event = asyncio.Event()
        self._pending[request.request_id] = event
        self._requests[request.request_id] = request

        logger.info(f"HITL request: {request.type.value} from {request.agent} — {request.prompt[:80]}")

        # Send to connected WebSocket clients
        await self._broadcast_request(request)

        # Wait for response with timeout
        try:
            await asyncio.wait_for(event.wait(), timeout=request.timeout_seconds)
        except asyncio.TimeoutError:
            logger.info(f"HITL timeout for {request.request_id} — using default: {request.default_action}")
            return HITLResponse(
                request_id=request.request_id,
                action=request.default_action,
            )

        response = self._responses.pop(request.request_id, None)
        self._pending.pop(request.request_id, None)
        self._requests.pop(request.request_id, None)

        if response is None:
            return HITLResponse(request_id=request.request_id, action=request.default_action)

        logger.info(f"HITL response: {response.action}")
        return response

    async def receive_response(self, response: HITLResponse) -> bool:
        """Called when user responds via WebSocket. Returns True if request was pending."""
        if response.request_id not in self._pending:
            logger.warning(f"HITL response for unknown request: {response.request_id}")
            return False

        self._responses[response.request_id] = response
        self._pending[response.request_id].set()
        return True

    async def _broadcast_request(self, request: HITLRequest) -> None:
        """Send HITL request to all connected WebSocket clients."""
        try:
            from agentic_hub.api.ws import get_ws_manager
            manager = get_ws_manager()
            # Broadcast to all active connections
            for session_id in list(manager._connections.keys()):
                await manager.send(session_id, {
                    "type": "hitl_request",
                    **request.to_dict(),
                })
        except Exception as e:
            logger.warning(f"HITL broadcast failed: {e}")

    def get_pending_requests(self) -> list[dict]:
        """Get all pending HITL requests (for API status)."""
        return [req.to_dict() for req in self._requests.values()]

    @staticmethod
    def create_request(
        hitl_type: HITLType,
        prompt: str,
        agent: str = "",
        node_id: str = "",
        options: list[str] | None = None,
        context: str = "",
        timeout: int = 300,
        default: str = "timeout",
    ) -> HITLRequest:
        """Convenience factory for creating HITL requests."""
        return HITLRequest(
            request_id=str(uuid.uuid4()),
            type=hitl_type,
            prompt=prompt,
            options=options or [],
            context=context,
            timeout_seconds=timeout,
            default_action=default,
            agent=agent,
            node_id=node_id,
        )


# Singleton
_manager: HITLManager | None = None


def get_hitl_manager() -> HITLManager:
    global _manager
    if _manager is None:
        _manager = HITLManager()
    return _manager
