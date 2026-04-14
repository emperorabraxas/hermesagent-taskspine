"""Chat API endpoints with gamification integration."""
from __future__ import annotations

import asyncio
import json
import logging
import uuid
from datetime import datetime

from fastapi import APIRouter, Request
from pydantic import BaseModel
from sse_starlette.sse import EventSourceResponse

from agentic_hub.config import load_models_config
from agentic_hub.core.memory import ConversationMemory, Message
from agentic_hub.core.orchestrator import Orchestrator, AGENT_MAP
from agentic_hub.gamification.achievements import AchievementChecker
from agentic_hub.gamification.engine import GamificationEngine
from agentic_hub.models.database import get_session_factory

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api", tags=["chat"])

_sessions: dict[str, ConversationMemory] = {}
_cancel_tokens: dict[str, asyncio.Event] = {}  # session_id -> cancel event


class ChatRequest(BaseModel):
    message: str
    session_id: str | None = None
    temperature: float | None = None  # Per-interaction temperature override


class ChatResponse(BaseModel):
    session_id: str
    response: str
    route: str = ""
    agent: str = ""
    xp: dict | None = None
    achievements: list[dict] | None = None


def _get_or_create_session(session_id: str | None) -> tuple[str, ConversationMemory]:
    if session_id and session_id in _sessions:
        return session_id, _sessions[session_id]
    sid = session_id or str(uuid.uuid4())
    mem = ConversationMemory(sid)
    _sessions[sid] = mem
    return sid, mem


def _resolve_agent_xp(agent_name: str) -> tuple[int, str]:
    """Get base XP and source for an agent."""
    config = load_models_config()
    if agent_name == "code_team":
        ct = config.get("code_team", {})
        return ct.get("xp_base", 20), "cloud"
    if agent_name == "opus":
        return 10, "cloud"
    agent_cfg = config.get("agents", {}).get(agent_name, {})
    return agent_cfg.get("xp_base", 5), "local"


async def _award_gamification(
    agent_name: str, source: str, base_xp: int,
    reason: str = "chat_completion",
    context: dict | None = None,
) -> tuple[dict, list[dict]]:
    """Award XP and check achievements. Returns (xp_info, new_achievements)."""
    try:
        engine = GamificationEngine()
        checker = AchievementChecker()
        factory = get_session_factory()

        async with factory() as session:
            xp_info = await engine.award_xp(
                session=session,
                agent=agent_name,
                base_xp=base_xp,
                reason=reason,
                source=source,
            )

            # Inject combo multiplier from XP award into context for achievements
            if context is not None and "combo_multiplier" not in context:
                context["combo_multiplier"] = xp_info.get("combo_multiplier", 1.0)

            new_achievements = await checker.check_and_unlock(
                session=session,
                agent=agent_name,
                source=source,
                total_xp=xp_info["total_xp"],
                level=xp_info["level"],
                current_streak=xp_info["current_streak"],
                hour=datetime.now().hour,
                context=context,
            )

            await session.commit()

        return xp_info, [
            {"key": a.key, "name": a.name, "description": a.description, "icon": a.icon}
            for a in new_achievements
        ]
    except Exception as e:
        logger.warning(f"Gamification error (non-fatal): {e}")
        return {}, []


@router.post("/chat")
async def chat(req: ChatRequest):
    """Non-streaming chat endpoint with gamification."""
    sid, memory = _get_or_create_session(req.session_id)
    orchestrator = Orchestrator()

    await memory.add(Message(role="user", content=req.message))

    full_response = []
    agent_name = "oracle"
    achievement_ctx: dict = {"memory_messages": len(memory.get_history())}
    async for chunk in orchestrator.process(
        req.message,
        conversation_history=memory.get_history(last_n=10),
    ):
        # Parse §META markers
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
            continue
        if chunk.startswith(("§SPIDER:", "§APPROVE:", "§EXEC:")):
            continue
        full_response.append(chunk)
        # Detect agent from routing indicator
        if chunk.startswith("*[") and "·" in chunk:
            agent_name = chunk.split("[")[1].split("·")[0].strip()

    response_text = "".join(full_response)
    await memory.add(Message(role="assistant", content=response_text))

    # Award XP
    reason = "rag_query" if achievement_ctx.get("rag_chunks") else "chat_completion"
    base_xp, source = _resolve_agent_xp(agent_name)
    xp_info, new_achievements = await _award_gamification(
        agent_name, source, base_xp, reason=reason, context=achievement_ctx,
    )

    return ChatResponse(
        session_id=sid,
        response=response_text,
        agent=agent_name,
        xp=xp_info,
        achievements=new_achievements,
    )


@router.get("/chat/stream")
async def chat_stream(request: Request, message: str, session_id: str | None = None, force_agent: str | None = None):
    """SSE streaming chat endpoint with gamification."""
    import re as _re
    # Input validation
    message = message.replace("\x00", "")[:10000]  # strip null bytes, cap at 10K chars
    if not message.strip():
        return EventSourceResponse(iter([]))
    if session_id and not _re.match(r"^[a-f0-9-]{36}$", session_id):
        session_id = None
    VALID_AGENTS = {"money_maker", "scholar", "oracle", "automator", "code_team", "warroom", None}
    if force_agent not in VALID_AGENTS:
        force_agent = None

    # Mark user as active — pauses idle research, frees GPU
    from agentic_hub.core.idle_daemon import mark_active
    mark_active()

    sid, memory = _get_or_create_session(session_id)
    orchestrator = Orchestrator()

    await memory.add(Message(role="user", content=message))

    async def event_generator():
        full_response = []
        agent_name = "oracle"

        # Forced agent routing (e.g., Money Maker mode — click the Vault)
        if force_agent == "money_maker":
            agent_name = "money_maker"
            from agentic_hub.core.money_maker import MoneyMaker
            mm = MoneyMaker()
            # Publish activity
            try:
                from agentic_hub.main import _spider_activity
                import time as _t
                _spider_activity["money_maker"] = {"status": "working", "text": "🐺 Money Maker activated", "timestamp": _t.time()}
            except Exception:
                pass
            yield {"event": "token", "data": json.dumps({"text": "*[money_maker · local]*\n\n", "session_id": sid})}
            async for chunk in mm.process(message, conversation_history=memory.get_history(last_n=10)):
                if chunk.startswith("§SPIDER:"):
                    parts = chunk[8:].split(":", 1)
                    if len(parts) == 2:
                        yield {"event": "spider", "data": json.dumps({"spider": parts[0], "text": parts[1], "session_id": sid})}
                        try:
                            _spider_activity[parts[0]] = {"status": "working", "text": parts[1], "timestamp": _t.time()}
                        except Exception:
                            pass
                    continue
                full_response.append(chunk)
                yield {"event": "token", "data": json.dumps({"text": chunk, "session_id": sid})}

            response_text = "".join(full_response)
            await memory.add(Message(role="assistant", content=response_text))
            mm_ctx = {"memory_messages": len(memory.get_history())}
            xp_info, new_achievements = await _award_gamification("money_maker", "money_maker", 15, context=mm_ctx)
            yield {"event": "done", "data": json.dumps({"session_id": sid, "full_response": response_text, "agent": "money_maker", "xp": xp_info, "achievements": [{"key": a["key"], "name": a["name"], "icon": a["icon"]} for a in new_achievements]})}
            return

        # /run command — execute directly, bypass agents
        if message.startswith("/run "):
            cmd = message[5:].strip()
            agent_name = "automator"
            from agentic_hub.core.sandbox import execute
            yield {"event": "token", "data": json.dumps({"text": f"*[automator · local]*\n\n> 🔧 `{cmd}`\n", "session_id": sid})}
            result = await execute(cmd)
            output = ""
            if result.stdout:
                output += f"```\n{result.stdout}\n```\n"
            if result.stderr and result.returncode != 0:
                output += f"⚠️ `{result.stderr[:500]}`\n"
            if result.timed_out:
                output += "⏱️ Timed out.\n"
            if not output:
                output = "*No output*\n"
            full_response.append(output)
            yield {"event": "token", "data": json.dumps({"text": output, "session_id": sid})}

            response_text = "".join(full_response)
            await memory.add(Message(role="assistant", content=response_text))
            base_xp, source = _resolve_agent_xp(agent_name)
            run_ctx = {
                "sandbox_used": True,
                "exec_count": 1,
                "exec_all_success": result.returncode == 0,
                "memory_messages": len(memory.get_history()),
            }
            xp_info, new_achievements = await _award_gamification(agent_name, source, base_xp, reason="sandbox_exec", context=run_ctx)
            yield {"event": "done", "data": json.dumps({"session_id": sid, "full_response": response_text, "agent": agent_name, "xp": xp_info, "achievements": [{"key": a["key"], "name": a["name"], "icon": a["icon"]} for a in new_achievements]})}
            return

        # /read command — read a file (path-restricted)
        if message.startswith("/read "):
            path = message[6:].strip()
            agent_name = "scholar"
            # SECURITY: restrict to project directories only
            from pathlib import Path as P
            allowed_roots = [P.home() / d for d in ["spider.Web", "project", "uwm-integration",
                             "salesforce-backup", "archive_sentinel_anime", "ai-dotfiles", "test"]]
            resolved = P(path).resolve()
            if not any(resolved.is_relative_to(r) for r in allowed_roots if r.exists()):
                yield {"event": "token", "data": json.dumps({"text": f"*[scholar · local]*\n\n⛔ Access denied: `{path}` is outside allowed project directories.\n", "session_id": sid})}
                response_text = f"Access denied: {path}"
                await memory.add(Message(role="assistant", content=response_text))
                base_xp, source = _resolve_agent_xp(agent_name)
                xp_info, new_achievements = await _award_gamification(agent_name, source, base_xp)
                yield {"event": "done", "data": json.dumps({"session_id": sid, "full_response": response_text, "agent": agent_name, "xp": xp_info, "achievements": []})}
                return
            from agentic_hub.core.sandbox import read_file
            yield {"event": "token", "data": json.dumps({"text": f"*[scholar · local]*\n\n📄 `{path}`\n", "session_id": sid})}
            content = await read_file(path)
            output = f"```\n{content[:10000]}\n```\n"
            full_response.append(output)
            yield {"event": "token", "data": json.dumps({"text": output, "session_id": sid})}

            response_text = "".join(full_response)
            await memory.add(Message(role="assistant", content=response_text))
            base_xp, source = _resolve_agent_xp(agent_name)
            read_ctx = {"file_read": True, "memory_messages": len(memory.get_history())}
            xp_info, new_achievements = await _award_gamification(agent_name, source, base_xp, reason="file_read", context=read_ctx)
            yield {"event": "done", "data": json.dumps({"session_id": sid, "full_response": response_text, "agent": agent_name, "xp": xp_info, "achievements": [{"key": a["key"], "name": a["name"], "icon": a["icon"]} for a in new_achievements]})}
            return

        # /scholar command — search papers, lookup by ID, find authors, get recommendations
        if message.startswith("/scholar "):
            import re as _scholar_re
            query = message[9:].strip()
            agent_name = "scholar"
            yield {"event": "token", "data": json.dumps({"text": f"*[scholar · api]*\n\n📚 *{query}*\n\n", "session_id": sid})}
            try:
                from agentic_hub.core.scholar_client import get_scholar
                scholar = get_scholar()

                # Intent detection: DOI/ArXiv → get_paper
                doi_match = _scholar_re.match(r"^(10\.\d{4,}/\S+)$", query)
                arxiv_match = _scholar_re.match(r"^(\d{4}\.\d{4,})(v\d+)?$", query)
                if doi_match:
                    paper = await scholar.get_paper(f"DOI:{doi_match.group(1)}")
                    output = scholar.format_search_results([paper]) if paper else "No paper found for that DOI.\n"
                elif arxiv_match:
                    paper = await scholar.get_paper(f"ARXIV:{arxiv_match.group(1)}")
                    output = scholar.format_search_results([paper]) if paper else "No paper found for that ArXiv ID.\n"

                # Intent detection: "author <name>" → search_authors + get_author
                elif query.lower().startswith("author "):
                    author_query = query[7:].strip()
                    authors = await scholar.search_authors(author_query, limit=5)
                    if authors:
                        # Get full details for top result
                        top = authors[0]
                        detail = await scholar.get_author(top["authorId"]) if top.get("authorId") else top
                        lines = [f"**Found {len(authors)} author(s):**\n"]
                        for i, a in enumerate(authors, 1):
                            name = a.get("name", "Unknown")
                            h = a.get("hIndex", "?")
                            papers = a.get("paperCount", "?")
                            cites = a.get("citationCount", 0)
                            affiliations = ", ".join(a.get("affiliations") or []) or "—"
                            marker = " ← top result" if i == 1 else ""
                            lines.append(f"### {i}. {name}{marker}")
                            lines.append(f"📊 h-index: **{h}** | Papers: **{papers}** | Citations: **{cites:,}**")
                            lines.append(f"🏛️ {affiliations}")
                            lines.append("---")
                        if detail and detail.get("hIndex"):
                            lines.insert(1, f"*Top result detail — h-index: {detail.get('hIndex')}, {detail.get('paperCount', '?')} papers*\n")
                        output = "\n".join(lines)
                    else:
                        output = f"No authors found for \"{author_query}\".\n"

                # Intent detection: "similar <paper_id>" → recommend_papers
                elif query.lower().startswith("similar "):
                    seed_id = query[8:].strip()
                    recs = await scholar.recommend_papers([seed_id], limit=5)
                    if recs:
                        output = f"**Papers similar to `{seed_id}`:**\n\n" + scholar.format_search_results(recs)
                    else:
                        output = f"No recommendations found for `{seed_id}`. Try a Semantic Scholar paper ID.\n"

                # Default: exact title match → fallback to keyword search
                else:
                    paper = await scholar.match_paper(query)
                    if paper:
                        output = scholar.format_search_results([paper])
                    else:
                        results = await scholar.search_papers(query, limit=5)
                        output = scholar.format_search_results(results)
            except Exception as e:
                output = f"⚠️ Scholar API error: {e}\n"
            full_response.append(output)
            yield {"event": "token", "data": json.dumps({"text": output, "session_id": sid})}

            response_text = "".join(full_response)
            await memory.add(Message(role="assistant", content=response_text))
            base_xp, source = _resolve_agent_xp(agent_name)
            scholar_ctx = {"scholar_search": True, "memory_messages": len(memory.get_history())}
            xp_info, new_achievements = await _award_gamification(agent_name, source, base_xp, reason="scholar_search", context=scholar_ctx)
            yield {"event": "done", "data": json.dumps({"session_id": sid, "full_response": response_text, "agent": agent_name, "xp": xp_info, "achievements": [{"key": a["key"], "name": a["name"], "icon": a["icon"]} for a in new_achievements]})}
            return

        # /council command — War Room: all spiders debate
        if message.startswith("/council"):
            topic = message[8:].strip() or "What should we work on next?"
            agent_name = "warroom"
            yield {"event": "token", "data": json.dumps({"text": "*[war room · all spiders]*\n\n", "session_id": sid})}
            # Publish war room activation
            try:
                from agentic_hub.main import _spider_activity
                import time as _t
                _spider_activity["warroom"] = {"status": "working", "text": "⚔️ Council session active", "timestamp": _t.time()}
            except Exception:
                pass

            async for chunk in orchestrator.council(topic, conversation_history=memory.get_history(last_n=10)):
                if chunk.startswith("§SPIDER:"):
                    parts = chunk[8:].split(":", 1)
                    if len(parts) == 2:
                        yield {"event": "spider", "data": json.dumps({"spider": parts[0], "text": parts[1], "session_id": sid})}
                        # Publish each spider's contribution to activity feed
                        try:
                            _spider_activity[parts[0]] = {"status": "working", "text": parts[1], "timestamp": _t.time()}
                        except Exception:
                            pass
                    continue
                full_response.append(chunk)
                yield {"event": "token", "data": json.dumps({"text": chunk, "session_id": sid})}

            response_text = "".join(full_response)
            await memory.add(Message(role="assistant", content=response_text))
            base_xp, source = 25, "council"
            council_ctx = {"council_spiders": 5, "memory_messages": len(memory.get_history())}
            xp_info, new_achievements = await _award_gamification(agent_name, source, base_xp, reason="council_session", context=council_ctx)
            yield {"event": "done", "data": json.dumps({"session_id": sid, "full_response": response_text, "agent": agent_name, "xp": xp_info, "achievements": [{"key": a["key"], "name": a["name"], "icon": a["icon"]} for a in new_achievements]})}
            return

        # /improve command — spiders work on spider.Web itself
        if message.startswith("/improve"):
            task = message[8:].strip() or "Review spider.Web's code and suggest one improvement"
            agent_name = "code_team"
            improve_msg = (
                f"You are working on the spider.Web codebase at /home/bobbyblowssmoke/spider.Web/. "
                f"Task: {task}\n\n"
                "Read the relevant files first, then make the change. "
                "Write files using bash blocks with cat > file << 'EOF' syntax. "
                "Test your changes if possible. Be specific and complete."
            )
            improve_ctx: dict = {"improve_used": True, "memory_messages": len(memory.get_history())}
            async for chunk in orchestrator.process(improve_msg, conversation_history=memory.get_history(last_n=10)):
                if chunk.startswith("§META:"):
                    parts = chunk[6:].split(":", 1)
                    if len(parts) == 2:
                        key, value = parts
                        if value in ("true", "True"):
                            improve_ctx[key] = True
                        elif value in ("false", "False"):
                            improve_ctx[key] = False
                        else:
                            try:
                                improve_ctx[key] = int(value)
                            except ValueError:
                                improve_ctx[key] = value
                    continue
                if chunk.startswith("§SPIDER:"):
                    parts = chunk[8:].split(":", 1)
                    if len(parts) == 2:
                        yield {"event": "spider", "data": json.dumps({"spider": parts[0], "text": parts[1], "session_id": sid})}
                    continue
                if chunk.startswith(("§APPROVE:", "§EXEC:")):
                    # Forward exec/approve events to frontend
                    if chunk.startswith("§EXEC:"):
                        parts = chunk[6:].split(":", 2)
                        if len(parts) >= 3:
                            yield {"event": "exec", "data": json.dumps({"action": parts[0], "spider": parts[1], "detail": parts[2], "session_id": sid})}
                    elif chunk.startswith("§APPROVE:"):
                        parts = chunk[9:].split(":", 2)
                        if len(parts) >= 3:
                            yield {"event": "approve", "data": json.dumps({"level": parts[0], "spider": parts[1], "command": parts[2], "session_id": sid})}
                    continue
                full_response.append(chunk)
                if chunk.startswith("*[") and "·" in chunk:
                    agent_name = chunk.split("[")[1].split("·")[0].strip()
                yield {"event": "token", "data": json.dumps({"text": chunk, "session_id": sid})}

            response_text = "".join(full_response)
            await memory.add(Message(role="assistant", content=response_text))
            base_xp, source = _resolve_agent_xp(agent_name)
            xp_info, new_achievements = await _award_gamification(agent_name, source, base_xp, reason="improve_task", context=improve_ctx)
            yield {"event": "done", "data": json.dumps({"session_id": sid, "full_response": response_text, "agent": agent_name, "xp": xp_info, "achievements": [{"key": a["key"], "name": a["name"], "icon": a["icon"]} for a in new_achievements]})}
            return

        # Achievement context — populated from §META markers during streaming
        achievement_ctx: dict = {"memory_messages": len(memory.get_history())}

        async for chunk in orchestrator.process(
            message,
            conversation_history=memory.get_history(last_n=10),
        ):
            # Achievement signal markers (prefixed with §META:) — consumed, not sent to frontend
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
                continue

            # Thinking blocks (prefixed with §THINKING:) — Claude's extended reasoning
            if chunk.startswith("§THINKING:"):
                thinking_text = chunk[10:]
                if thinking_text.strip():
                    yield {
                        "event": "thinking",
                        "data": json.dumps({"text": thinking_text, "session_id": sid}),
                    }
                continue

            # Spider bubble events (prefixed with §SPIDER:)
            if chunk.startswith("§SPIDER:"):
                parts = chunk[8:].split(":", 1)
                if len(parts) == 2:
                    yield {
                        "event": "spider",
                        "data": json.dumps({"spider": parts[0], "text": parts[1], "session_id": sid}),
                    }
                    # Publish to activity feed for dashboard
                    try:
                        from agentic_hub.main import _spider_activity
                        import time as _t
                        _spider_activity[parts[0]] = {"status": "working", "text": parts[1], "timestamp": _t.time()}
                    except Exception:
                        pass
                continue

            # Command approval events (prefixed with §APPROVE:)
            if chunk.startswith("§APPROVE:"):
                parts = chunk[9:].split(":", 2)
                if len(parts) >= 3:
                    yield {
                        "event": "approve",
                        "data": json.dumps({
                            "level": parts[0],      # privileged or local
                            "spider": parts[1],      # which spider wants to run it
                            "command": parts[2],     # the command
                            "session_id": sid,
                        }),
                    }
                continue

            # Command execution events (prefixed with §EXEC:)
            if chunk.startswith("§EXEC:"):
                parts = chunk[6:].split(":", 2)
                if len(parts) >= 3:
                    yield {
                        "event": "exec",
                        "data": json.dumps({
                            "action": parts[0],     # start, stdout, error, timeout, done
                            "spider": parts[1],      # which spider ran it
                            "detail": parts[2],      # command text or output
                            "session_id": sid,
                        }),
                    }
                continue

            full_response.append(chunk)
            if chunk.startswith("*[") and "·" in chunk:
                agent_name = chunk.split("[")[1].split("·")[0].strip()

            yield {
                "event": "token",
                "data": json.dumps({"text": chunk, "session_id": sid}),
            }

        response_text = "".join(full_response)
        await memory.add(Message(role="assistant", content=response_text))

        # Entity extraction — deferred to idle to avoid GPU model swap during active chat
        try:
            from agentic_hub.core.idle_daemon import is_idle
            if is_idle():
                from agentic_hub.core.entity_memory import get_entity_memory
                entity_mem = get_entity_memory()
                combined_text = f"User: {message}\nAssistant: {response_text[:1500]}"
                asyncio.create_task(entity_mem.extract_and_store_background(combined_text, sid))
        except Exception:
            pass

        # Determine reason from context signals
        reason = "chat_completion"
        if achievement_ctx.get("r1_validated"):
            reason = "r1_validated"
        elif achievement_ctx.get("rag_chunks"):
            reason = "rag_query"

        # Award XP with achievement context
        base_xp, source = _resolve_agent_xp(agent_name)
        xp_info, new_achievements = await _award_gamification(
            agent_name, source, base_xp, reason=reason, context=achievement_ctx,
        )

        yield {
            "event": "done",
            "data": json.dumps({
                "session_id": sid,
                "full_response": response_text,
                "agent": agent_name,
                "xp": xp_info,
                "achievements": [
                    {"key": a["key"], "name": a["name"], "icon": a["icon"]}
                    for a in new_achievements
                ],
            }),
        }

    return EventSourceResponse(event_generator())


@router.delete("/chat/{session_id}")
async def clear_session(session_id: str):
    """Clear a chat session."""
    if session_id in _sessions:
        await _sessions[session_id].clear()
        del _sessions[session_id]
    return {"status": "cleared"}


@router.delete("/chat/{session_id}/cancel")
async def cancel_session(session_id: str):
    """Cancel a running task for a session (kill switch)."""
    if session_id in _cancel_tokens:
        _cancel_tokens[session_id].set()
        return {"status": "cancelled", "session_id": session_id}
    return {"status": "no_active_task", "session_id": session_id}
