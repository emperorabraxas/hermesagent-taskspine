"""WebSocket transport — bidirectional chat with HITL support.

Runs alongside SSE (backward compat). Enables:
  - Mid-stream cancel
  - Mid-stream approval responses
  - HITL breakpoint responses (Phase 6)
  - Real-time DAG execution status (Phase 11)

Protocol:
  Client→Server:
    {"type": "message", "text": "...", "session_id": "uuid"}
    {"type": "approve", "session_id": "...", "command": "...", "approved": true}
    {"type": "cancel", "session_id": "..."}
    {"type": "hitl_response", "request_id": "...", "action": "...", "user_input": "..."}

  Server→Client:
    {"type": "token", "text": "...", "session_id": "..."}
    {"type": "spider", "spider": "...", "text": "...", "session_id": "..."}
    {"type": "exec", "action": "...", "spider": "...", "detail": "...", "session_id": "..."}
    {"type": "approve_request", "level": "...", "spider": "...", "command": "...", "session_id": "..."}
    {"type": "meta", "key": "...", "value": "...", "session_id": "..."}
    {"type": "done", "full_response": "...", "agent": "...", "xp": {...}, "achievements": [...], "session_id": "..."}
    {"type": "error", "message": "...", "session_id": "..."}
"""
from __future__ import annotations

import asyncio
import json
import logging
import uuid

from fastapi import WebSocket, WebSocketDisconnect

from agentic_hub.core.memory import ConversationMemory, Message
from agentic_hub.core.orchestrator import Orchestrator

logger = logging.getLogger(__name__)


class WSConnectionManager:
    """Track active WebSocket connections per session."""

    def __init__(self):
        self._connections: dict[str, WebSocket] = {}
        self._cancel_events: dict[str, asyncio.Event] = {}

    async def connect(self, ws: WebSocket, session_id: str) -> None:
        await ws.accept()
        self._connections[session_id] = ws
        logger.info(f"WS connected: {session_id}")

    def disconnect(self, session_id: str) -> None:
        self._connections.pop(session_id, None)
        self._cancel_events.pop(session_id, None)
        logger.info(f"WS disconnected: {session_id}")

    async def send(self, session_id: str, event: dict) -> None:
        ws = self._connections.get(session_id)
        if ws:
            try:
                await ws.send_json(event)
            except Exception:
                self.disconnect(session_id)

    def get_cancel_event(self, session_id: str) -> asyncio.Event:
        if session_id not in self._cancel_events:
            self._cancel_events[session_id] = asyncio.Event()
        return self._cancel_events[session_id]

    def cancel(self, session_id: str) -> None:
        if session_id in self._cancel_events:
            self._cancel_events[session_id].set()

    def reset_cancel(self, session_id: str) -> None:
        if session_id in self._cancel_events:
            self._cancel_events[session_id].clear()

    @property
    def active_count(self) -> int:
        return len(self._connections)


# Singleton
_manager: WSConnectionManager | None = None


def get_ws_manager() -> WSConnectionManager:
    global _manager
    if _manager is None:
        _manager = WSConnectionManager()
    return _manager


# ── Session store (shared with SSE endpoint) ───────────────────────
_ws_sessions: dict[str, ConversationMemory] = {}


def _get_or_create_session(session_id: str | None) -> tuple[str, ConversationMemory]:
    sid = session_id or str(uuid.uuid4())
    if sid not in _ws_sessions:
        _ws_sessions[sid] = ConversationMemory(sid)
    return sid, _ws_sessions[sid]


# ── WebSocket endpoint ─────────────────────────────────────────────

async def ws_chat(websocket: WebSocket):
    """Main WebSocket chat handler. Mounted by main.py."""
    manager = get_ws_manager()
    session_id = str(uuid.uuid4())
    await manager.connect(websocket, session_id)

    try:
        while True:
            data = await websocket.receive_json()
            msg_type = data.get("type", "")

            if msg_type == "message":
                await _handle_message(manager, data, session_id)

            elif msg_type == "cancel":
                target_sid = data.get("session_id", session_id)
                manager.cancel(target_sid)
                await manager.send(session_id, {
                    "type": "cancelled",
                    "session_id": target_sid,
                })

            elif msg_type == "approve":
                from agentic_hub.core.hitl import get_hitl_manager, HITLResponse
                hitl_mgr = get_hitl_manager()
                # Convert approve message to HITL response format
                req_id = data.get("request_id", "")
                approved = data.get("approved", False)
                response = HITLResponse(
                    request_id=req_id,
                    action="approve" if approved else "reject",
                )
                await hitl_mgr.receive_response(response)
                logger.info(f"WS approve: {req_id} -> {'approved' if approved else 'rejected'}")

            elif msg_type == "hitl_response":
                from agentic_hub.core.hitl import get_hitl_manager, HITLResponse
                hitl_mgr = get_hitl_manager()
                response = HITLResponse.from_dict(data)
                ok = await hitl_mgr.receive_response(response)
                await manager.send(session_id, {
                    "type": "hitl_ack",
                    "request_id": data.get("request_id", ""),
                    "accepted": ok,
                })

            elif msg_type == "ping":
                await manager.send(session_id, {"type": "pong"})

    except WebSocketDisconnect:
        manager.disconnect(session_id)
    except Exception as e:
        logger.error(f"WS error: {e}")
        manager.disconnect(session_id)


async def _handle_message(
    manager: WSConnectionManager, data: dict, ws_session_id: str
) -> None:
    """Process a chat message received over WebSocket."""
    from agentic_hub.config import load_models_config
    from agentic_hub.api.chat import _resolve_agent_xp, _award_gamification
    from agentic_hub.core.idle_daemon import mark_active

    text = data.get("text", "").replace("\x00", "")[:10000]
    if not text.strip():
        await manager.send(ws_session_id, {"type": "error", "message": "Empty message"})
        return

    # Use provided session_id or the WS connection's own
    req_session_id = data.get("session_id") or ws_session_id
    sid, memory = _get_or_create_session(req_session_id)

    mark_active()
    manager.reset_cancel(sid)
    cancel_event = manager.get_cancel_event(sid)

    orchestrator = Orchestrator()
    await memory.add(Message(role="user", content=text))

    full_response = []
    agent_name = "oracle"
    achievement_ctx: dict = {"memory_messages": len(memory.get_history())}

    try:
        async for chunk in orchestrator.process(
            text,
            conversation_history=memory.get_history(last_n=10),
        ):
            # Check for cancellation
            if cancel_event.is_set():
                await manager.send(sid, {
                    "type": "cancelled",
                    "session_id": sid,
                    "partial_response": "".join(full_response),
                })
                break

            # §META markers — consumed, forwarded as meta events
            if chunk.startswith("§META:"):
                parts = chunk[6:].split(":", 1)
                if len(parts) == 2:
                    key, value = parts
                    if value in ("true", "True"):
                        achievement_ctx[key] = True
                    elif value in ("false", "False"):
                        achievement_ctx[key] = False
                    else:
                        try:
                            achievement_ctx[key] = int(value)
                        except ValueError:
                            achievement_ctx[key] = value
                    await manager.send(sid, {
                        "type": "meta",
                        "key": key,
                        "value": achievement_ctx[key],
                        "session_id": sid,
                    })
                continue

            # §SPIDER markers
            if chunk.startswith("§SPIDER:"):
                parts = chunk[8:].split(":", 1)
                if len(parts) == 2:
                    await manager.send(sid, {
                        "type": "spider",
                        "spider": parts[0],
                        "text": parts[1],
                        "session_id": sid,
                    })
                continue

            # §APPROVE markers
            if chunk.startswith("§APPROVE:"):
                parts = chunk[9:].split(":", 2)
                if len(parts) >= 3:
                    await manager.send(sid, {
                        "type": "approve_request",
                        "level": parts[0],
                        "spider": parts[1],
                        "command": parts[2],
                        "session_id": sid,
                    })
                continue

            # §EXEC markers
            if chunk.startswith("§EXEC:"):
                parts = chunk[6:].split(":", 2)
                if len(parts) >= 3:
                    await manager.send(sid, {
                        "type": "exec",
                        "action": parts[0],
                        "spider": parts[1],
                        "detail": parts[2],
                        "session_id": sid,
                    })
                continue

            # Regular text
            full_response.append(chunk)
            if chunk.startswith("*[") and "·" in chunk:
                agent_name = chunk.split("[")[1].split("·")[0].strip()
            await manager.send(sid, {
                "type": "token",
                "text": chunk,
                "session_id": sid,
            })

        if not cancel_event.is_set():
            response_text = "".join(full_response)
            await memory.add(Message(role="assistant", content=response_text))

            # Gamification
            reason = "chat_completion"
            if achievement_ctx.get("r1_validated"):
                reason = "r1_validated"
            elif achievement_ctx.get("rag_chunks"):
                reason = "rag_query"

            base_xp, source = _resolve_agent_xp(agent_name)
            xp_info, new_achievements = await _award_gamification(
                agent_name, source, base_xp, reason=reason, context=achievement_ctx,
            )

            await manager.send(sid, {
                "type": "done",
                "session_id": sid,
                "full_response": response_text,
                "agent": agent_name,
                "xp": xp_info,
                "achievements": [
                    {"key": a["key"], "name": a["name"], "icon": a["icon"]}
                    for a in new_achievements
                ],
            })

    except Exception as e:
        logger.error(f"WS message processing error: {e}")
        await manager.send(sid, {
            "type": "error",
            "message": str(e),
            "session_id": sid,
        })
