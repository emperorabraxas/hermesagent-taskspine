"""FastAPI application entrypoint."""
from __future__ import annotations

import logging
import secrets as _secrets
import tempfile
import os
from contextlib import asynccontextmanager

from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from agentic_hub.config import load_models_config, get_settings
from agentic_hub.api.agents import router as agents_router
from agentic_hub.api.chat import router as chat_router
from agentic_hub.api.gamification import router as game_router
from agentic_hub.api.models import router as models_router
from agentic_hub.api.traces import router as traces_router
from agentic_hub.core.ollama_client import get_ollama

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger(__name__)

# ── Auth Token — printed to console on startup, required for all /api/* ──
AUTH_TOKEN = _secrets.token_urlsafe(32)
# Public endpoints that don't require auth
AUTH_EXEMPT = {"/health", "/", "/favicon.png", "/ws/chat"}


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup/shutdown lifecycle."""
    logger.info("spider.Web starting up...")
    # Token only goes to terminal — never to logger (logs can be shipped/captured)
    print(f"\n  ╔══════════════════════════════════════════════════╗", flush=True)
    print(f"  ║  🔑 Auth Token (terminal only — not logged)      ║", flush=True)
    print(f"  ║  {AUTH_TOKEN}  ║", flush=True)
    print(f"  ╚══════════════════════════════════════════════════╝\n", flush=True)
    # Also write token to a temp file so launchers (and the UI) can display it.
    # Use OS temp dir (Windows-safe) instead of hardcoding /tmp.
    try:
        token_path = Path(tempfile.gettempdir()) / ".spider-web-token"
        token_path.write_text(AUTH_TOKEN)
        if os.name != "nt":
            token_path.chmod(0o600)
    except Exception:
        pass

    # System crawl — first launch or stale profile
    try:
        from agentic_hub.core.system_profile import ensure_profile, get_system_context
        profile = ensure_profile()
        logger.info("System: %s", get_system_context())
    except Exception as e:
        logger.warning(f"System profile failed (non-fatal): {e}")

    # Verify Ollama is reachable
    ollama = get_ollama()
    try:
        models = await ollama.list_models()
        logger.info(f"Ollama connected — {len(models)} models available")
    except Exception as e:
        logger.warning(f"Ollama not reachable: {e}. Local agents will fail until Ollama is running.")

    # Pre-warm default model (non-blocking) — eliminates cold-start on first chat
    import asyncio
    async def _preload():
        try:
            from agentic_hub.core.gpu_scheduler import get_gpu_scheduler
            config = load_models_config()
            default_model = config.get("agents", {}).get("oracle", {}).get("local_model", "qwen-fast")
            scheduler = get_gpu_scheduler()
            await scheduler.ensure_model(default_model)
            logger.info(f"Pre-loaded {default_model}")
        except Exception as e:
            logger.debug(f"Pre-load failed (non-fatal): {e}")
    asyncio.create_task(_preload())

    # Auto-index common project dirs for RAG (background, non-blocking)
    async def _auto_index():
        try:
            from agentic_hub.core.rag import RAGPipeline
            from pathlib import Path
            rag = RAGPipeline()
            home = Path.home()
            for d in ["spider.Web/src", "project", "uwm-integration/src", "salesforce-backup"]:
                p = home / d
                if p.exists():
                    result = await rag.index_directory(p)
                    if result.get("files_indexed", 0) > 0:
                        logger.info(f"RAG indexed {d}: {result['files_indexed']} files, {result['chunks_created']} chunks")
            stats = rag.get_stats()
            logger.info(f"RAG ready: {stats['total_files']} files, {stats['total_chunks']} chunks")
        except Exception as e:
            logger.warning(f"Auto-index failed (non-fatal): {e}")
    asyncio.create_task(_auto_index())

    # Start Money Maker's 24/7 research daemon
    try:
        from agentic_hub.core.market_daemon import start_daemon
        await start_daemon()
        logger.info("Money Maker research daemon started — 24/7 market intelligence active")
    except Exception as e:
        logger.warning(f"Market daemon failed to start (non-fatal): {e}")

    # Auto-unlock vault if VAULT_PASSWORD is set
    try:
        from agentic_hub.core.secrets import try_load_vault_from_env
        vault = try_load_vault_from_env()
        if vault:
            logger.info(f"Vault unlocked — {len(vault.list_keys())} secrets loaded")
    except Exception as e:
        logger.debug(f"Vault not available (non-fatal): {e}")

    # Initialize RBAC built-in roles
    try:
        from agentic_hub.core.rbac import get_rbac
        rbac = get_rbac()
        await rbac.ensure_built_in_roles()
        logger.info("RBAC roles initialized")
    except Exception as e:
        logger.debug(f"RBAC init skipped (non-fatal): {e}")

    # Initialize advanced database services (Redis + PostgreSQL)
    try:
        from agentic_hub.core.redis_service import get_redis_service
        redis_svc = await get_redis_service()
        if redis_svc.connected:
            # Initialize spider state hashes
            spiders = ["cockpit", "scholar", "oracle", "code_team", "ops", "automator", "warroom", "money_maker", "lab"]
            for s in spiders:
                await redis_svc.set_spider_state(s, {"status": "idle", "text": "", "model": ""})
            # Log startup event
            await redis_svc.log_event("events:system", {"event": "startup", "spiders": "9"})
            info = await redis_svc.info()
            logger.info(f"Redis service active — {info.get('used_memory_human', '?')} memory, Pub/Sub + Streams + Leaderboards ready")
        else:
            logger.info("Redis service: not configured (Pub/Sub, Streams disabled)")
    except Exception as e:
        logger.debug(f"Redis service init skipped (non-fatal): {e}")

    try:
        from agentic_hub.core.pg_service import get_pg_service
        pg_svc = await get_pg_service()
        if pg_svc.connected:
            await pg_svc.setup_extensions()
            await pg_svc.setup_indexes()
            await pg_svc.setup_notify_triggers()
            await pg_svc.setup_materialized_views()
            logger.info("PostgreSQL service active — FTS, LISTEN/NOTIFY, materialized views ready")
        else:
            logger.info("PostgreSQL service: not configured (FTS, analytics disabled)")
    except Exception as e:
        logger.debug(f"PostgreSQL service init skipped (non-fatal): {e}")

    # Periodic materialized view refresh (every 5 minutes)
    async def _refresh_views():
        import asyncio as _aio
        while True:
            await _aio.sleep(300)
            try:
                from agentic_hub.core.pg_service import get_pg_service
                pg = await get_pg_service()
                if pg.connected:
                    await pg.refresh_materialized_views()
                    logger.debug("Materialized views refreshed")
            except Exception:
                pass
    asyncio.create_task(_refresh_views())

    # Start idle research daemon — spiders work while you rest
    try:
        from agentic_hub.core.idle_daemon import start_idle_daemon
        await start_idle_daemon()
        logger.info("Idle research daemon started — spiders research your projects when idle")
    except Exception as e:
        logger.warning(f"Idle daemon failed to start (non-fatal): {e}")

    # Start autonomous strategy scheduler (Money Maker 24/7)
    try:
        from agentic_hub.core.trading.scheduler import start_scheduler
        await start_scheduler()
        logger.info("Strategy scheduler started — Money Maker autonomous")
    except Exception as e:
        logger.debug(f"Strategy scheduler skipped (non-fatal): {e}")

    # Model upgrade scout — search HF for better models on startup
    async def _scout():
        from agentic_hub.core.model_scout import run_scout_background
        await run_scout_background()
    asyncio.create_task(_scout())

    # Discover and connect to external MCP servers
    try:
        from agentic_hub.core.mcp.client import get_mcp_client
        mcp_client = get_mcp_client()
        mcp_tools = await mcp_client.discover_and_connect()
        if mcp_tools:
            logger.info(f"MCP: {mcp_tools} external tools registered from {len(mcp_client.connected_servers)} servers")
    except Exception as e:
        logger.debug(f"MCP discovery skipped (non-fatal): {e}")

    yield

    # Cleanup
    # Disconnect MCP servers
    try:
        from agentic_hub.core.mcp.client import get_mcp_client
        await get_mcp_client().disconnect_all()
    except Exception:
        pass

    # Log shutdown event to Redis
    try:
        from agentic_hub.core.redis_service import get_redis_service
        redis_svc = await get_redis_service()
        if redis_svc.connected:
            await redis_svc.log_event("events:system", {"event": "shutdown"})
    except Exception:
        pass

    from agentic_hub.core.sandbox import get_shell
    await get_shell().close()
    await ollama.close()
    logger.info("spider.Web shut down.")


app = FastAPI(
    title="spider.Web",
    description="Local multi-agent AI platform with Opus orchestration — spider.BOB's web of agents",
    version="0.1.0",
    lifespan=lifespan,
)

# CORS — locked to localhost by default. Override via CORS_ORIGINS env var.
_settings = get_settings()
_cors_origins = ["http://localhost:8420", "http://127.0.0.1:8420"]
if hasattr(_settings, "cors_origins") and _settings.cors_origins:
    _cors_origins.extend(o.strip() for o in _settings.cors_origins.split(",") if o.strip())

app.add_middleware(
    CORSMiddleware,
    allow_origins=_cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Auth + Rate limiting middleware
import time
from collections import deque
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse as StarletteJSONResponse


class AuthMiddleware(BaseHTTPMiddleware):
    """Bearer token auth on all /api/* endpoints. Token printed to console on startup."""

    async def dispatch(self, request, call_next):
        path = request.url.path

        # Skip auth for exempt paths (health, static, websocket)
        if path in AUTH_EXEMPT or not path.startswith("/api/"):
            return await call_next(request)

        # Allow token via header or query param (SSE needs query param)
        auth_header = request.headers.get("authorization", "")
        token = ""
        if auth_header.startswith("Bearer "):
            token = auth_header[7:]
        if not token:
            token = request.query_params.get("token", "")

        if token != AUTH_TOKEN:
            return StarletteJSONResponse(
                {"error": "Unauthorized", "hint": "Pass token from server console as Bearer header or ?token= param"},
                status_code=401,
            )

        return await call_next(request)

app.add_middleware(AuthMiddleware)

class RateLimitMiddleware(BaseHTTPMiddleware):
    """In-memory rate limiter per IP."""
    LIMITS = {
        "/api/chat": (30, 60),       # 30 req/min
        "/api/config": (5, 60),      # 5 req/min
        "/api/preferences": (10, 60), # 10 req/min
    }
    _buckets: dict[str, deque] = {}

    async def dispatch(self, request, call_next):
        ip = request.client.host if request.client else "unknown"
        path = request.url.path
        for prefix, (limit, window) in self.LIMITS.items():
            if path.startswith(prefix):
                key = f"{ip}:{prefix}"
                now = time.time()
                q = self._buckets.setdefault(key, deque())
                while q and now - q[0] > window:
                    q.popleft()
                if len(q) >= limit:
                    return JSONResponse(
                        {"error": "Rate limit exceeded", "retry_after": int(window - (now - q[0]))},
                        status_code=429,
                        headers={"Retry-After": str(int(window - (now - q[0])))},
                    )
                q.append(now)
                break
        return await call_next(request)

app.add_middleware(RateLimitMiddleware)

app.include_router(chat_router)
app.include_router(agents_router)
app.include_router(models_router)
app.include_router(game_router)
app.include_router(traces_router)

# ── Live spider activity (bridges TUI ↔ Dashboard) ─────────────────

import time as _time
_spider_activity: dict[str, dict] = {}  # agent → {status, text, timestamp}


@app.get("/api/spiders/activity")
async def spider_activity():
    """Get current spider activity — polled by dashboard for live updates."""
    now = _time.time()
    # Clean stale entries (older than 30s)
    active = {
        k: v for k, v in _spider_activity.items()
        if now - v.get("timestamp", 0) < 30
    }
    return {"status": "ok", "spiders": active}


@app.get("/api/metrics")
async def get_metrics():
    """Factory metrics — revenue, agents, trades, strategies, uptime."""
    metrics = {}
    # Revenue from hustle engine
    try:
        from agentic_hub.core.trading.hustle import get_hustle_engine
        engine = get_hustle_engine()
        p = engine.get_progress()
        metrics["revenue"] = p["earned"]
        metrics["goal"] = p["goal"]
        metrics["goal_pct"] = p["progress_pct"]
    except Exception:
        metrics["revenue"] = 0
        metrics["goal"] = 600
    # Active agents
    now = _time.time()
    active = sum(1 for v in _spider_activity.values() if now - v.get("timestamp", 0) < 30 and v.get("status") == "working")
    metrics["agents_active"] = active
    metrics["agents_total"] = 5
    # Trade count
    try:
        from agentic_hub.core.trading.executor import get_executor
        metrics["trades"] = len(get_executor().get_trade_history(1000))
    except Exception:
        metrics["trades"] = 0
    # Active strategies
    try:
        from agentic_hub.core.trading.scheduler import get_scheduler
        strats = get_scheduler().get_strategies()
        metrics["strategies"] = len([s for s in strats if s.get("enabled")])
    except Exception:
        metrics["strategies"] = 0
    # Uptime
    try:
        from agentic_hub.core.market_daemon import get_daemon_uptime_hours
        metrics["uptime_hours"] = round(get_daemon_uptime_hours(), 1)
    except Exception:
        metrics["uptime_hours"] = 0
    return metrics


# ── Analytics & Search ────────────────────────────────────────────────


@app.get("/api/search")
async def search(q: str = "", search_type: str = "all", limit: int = 20):
    """Full-text search across messages and entities."""
    if not q:
        return {"status": "error", "message": "query parameter 'q' required"}
    try:
        from agentic_hub.core.pg_service import get_pg_service
        pg = await get_pg_service()
        if not pg.connected:
            return {"status": "error", "message": "PostgreSQL not connected"}
        results = {}
        if search_type in ("all", "messages"):
            results["messages"] = await pg.search_messages(q, limit=limit)
        if search_type in ("all", "entities"):
            results["entities"] = await pg.search_entities(q, limit=limit)
        return {"status": "ok", **results}
    except Exception as e:
        return {"status": "error", "message": str(e)}


@app.get("/api/analytics/spiders")
async def analytics_spiders():
    """Pre-computed spider stats from materialized views."""
    try:
        from agentic_hub.core.pg_service import get_pg_service
        pg = await get_pg_service()
        if not pg.connected:
            return {"status": "error", "message": "PostgreSQL not connected"}
        stats = await pg.get_spider_stats()
        response_times = await pg.get_spider_response_times()
        return {"status": "ok", "stats": stats, "response_times": response_times}
    except Exception as e:
        return {"status": "error", "message": str(e)}


@app.get("/api/analytics/xp")
async def analytics_xp(days: int = 30):
    """XP leaderboard (Redis) + daily trend (PostgreSQL)."""
    result: dict = {"status": "ok"}
    try:
        from agentic_hub.core.redis_service import get_redis_service
        redis = await get_redis_service()
        if redis.connected:
            result["leaderboard"] = await redis.get_leaderboard("leaderboard:xp")
            result["tasks"] = await redis.get_leaderboard("leaderboard:tasks")
            result["usage"] = await redis.get_leaderboard("leaderboard:usage")
    except Exception:
        result["leaderboard"] = []
    try:
        from agentic_hub.core.pg_service import get_pg_service
        pg = await get_pg_service()
        if pg.connected:
            result["daily_xp"] = await pg.get_daily_xp(days)
            result["xp_trend"] = await pg.get_xp_trend(days=days)
    except Exception:
        pass
    return result


@app.get("/api/analytics/activity")
async def analytics_activity(days: int = 7):
    """Conversation activity over time."""
    try:
        from agentic_hub.core.pg_service import get_pg_service
        pg = await get_pg_service()
        if not pg.connected:
            return {"status": "error", "message": "PostgreSQL not connected"}
        activity = await pg.get_conversation_activity(days)
        popular = await pg.get_popular_entities()
        return {"status": "ok", "activity": activity, "popular_entities": popular}
    except Exception as e:
        return {"status": "error", "message": str(e)}


@app.post("/api/analytics/refresh")
async def analytics_refresh():
    """Refresh materialized views on demand."""
    try:
        from agentic_hub.core.pg_service import get_pg_service
        pg = await get_pg_service()
        if not pg.connected:
            return {"status": "error", "message": "PostgreSQL not connected"}
        await pg.refresh_materialized_views()
        return {"status": "ok", "message": "Materialized views refreshed"}
    except Exception as e:
        return {"status": "error", "message": str(e)}


@app.post("/api/spiders/activity")
async def update_spider_activity(request: Request):
    """Update spider activity — called by chat handlers."""
    body = await request.json()
    agent = body.get("agent", "")
    status = body.get("status", "idle")  # idle, working, done
    text = body.get("text", "")
    if agent:
        _spider_activity[agent] = {
            "status": status,
            "text": text,
            "timestamp": _time.time(),
        }
    return {"status": "ok"}

# WebSocket endpoint (bidirectional chat — alongside SSE for backward compat)
from agentic_hub.api.ws import ws_chat
app.websocket("/ws/chat")(ws_chat)


# ── Plaid API (The Vault — bank account integration) ───────────────


@app.post("/api/plaid/link-token")
async def plaid_link_token():
    """Create a Plaid Link token for the frontend widget."""
    try:
        from agentic_hub.core.plaid_client import get_plaid_manager
        mgr = get_plaid_manager()
        token = mgr.create_link_token()
        return {"status": "ok", "link_token": token}
    except ValueError as e:
        return {"status": "error", "message": str(e)}
    except Exception as e:
        return {"status": "error", "message": f"Plaid error: {e}"}


@app.post("/api/plaid/exchange")
async def plaid_exchange(request: Request):
    """Exchange public_token from Plaid Link for access_token."""
    body = await request.json()
    public_token = body.get("public_token", "")
    if not public_token:
        return {"status": "error", "message": "public_token required"}
    try:
        from agentic_hub.core.plaid_client import get_plaid_manager
        mgr = get_plaid_manager()
        result = mgr.exchange_public_token(public_token)
        return {"status": "ok", **result}
    except Exception as e:
        return {"status": "error", "message": str(e)}


@app.get("/api/plaid/accounts")
async def plaid_accounts():
    """Fetch all linked Plaid accounts with balances."""
    try:
        from agentic_hub.core.plaid_client import get_plaid_manager
        from agentic_hub.core.secrets import get_vault
        mgr = get_plaid_manager()
        vault = get_vault()
        if not vault:
            return {"status": "error", "message": "Vault not unlocked"}

        all_accounts = []
        for key in vault.list_keys():
            if key.startswith("PLAID_ACCESS_"):
                token = vault.retrieve(key)
                if token:
                    try:
                        accounts = mgr.get_balances(token)
                        all_accounts.extend(accounts)
                    except Exception as e:
                        logger.warning(f"Plaid balance fetch failed for {key}: {e}")
        return {"status": "ok", "accounts": all_accounts}
    except Exception as e:
        return {"status": "error", "message": str(e)}


@app.get("/api/plaid/transactions")
async def plaid_transactions(days: int = 30):
    """Fetch recent transactions from all linked accounts."""
    from datetime import date, timedelta
    try:
        from agentic_hub.core.plaid_client import get_plaid_manager
        from agentic_hub.core.secrets import get_vault
        mgr = get_plaid_manager()
        vault = get_vault()
        if not vault:
            return {"status": "error", "message": "Vault not unlocked"}

        end = date.today()
        start = end - timedelta(days=days)
        all_txns = []
        for key in vault.list_keys():
            if key.startswith("PLAID_ACCESS_"):
                token = vault.retrieve(key)
                if token:
                    try:
                        txns = mgr.get_transactions(token, str(start), str(end))
                        all_txns.extend(txns)
                    except Exception as e:
                        logger.warning(f"Plaid txn fetch failed for {key}: {e}")

        all_txns.sort(key=lambda t: t["date"], reverse=True)
        return {"status": "ok", "transactions": all_txns[:100]}
    except Exception as e:
        return {"status": "error", "message": str(e)}


# ── Hot-Swap / Live Reload ─────────────────────────────────────────

@app.post("/api/reload")
async def reload_config():
    """Hot-reload all configuration without restarting the server."""
    reloaded = []
    # Clear models.yaml cache
    try:
        from agentic_hub.config import _models_config_cache
        import agentic_hub.config as cfg
        cfg._models_config_cache = None
        cfg._models_config_mtime = 0.0
        reloaded.append("models.yaml")
    except Exception:
        pass
    # Clear settings singleton
    try:
        import agentic_hub.config as cfg
        cfg._settings = None
        reloaded.append("settings (.env)")
    except Exception:
        pass
    # Clear RBAC cache
    try:
        from agentic_hub.core.rbac import get_rbac
        get_rbac().clear_cache()
        reloaded.append("rbac")
    except Exception:
        pass
    return {"status": "ok", "reloaded": reloaded}


# ── DAG API ────────────────────────────────────────────────────────

@app.get("/api/hitl/pending")
async def hitl_pending():
    """Get pending HITL requests waiting for user input."""
    from agentic_hub.core.hitl import get_hitl_manager
    mgr = get_hitl_manager()
    return {"status": "ok", "pending": mgr.get_pending_requests()}


@app.get("/api/dag")
async def list_dags():
    """List all available DAG workflows (built-in + saved)."""
    from agentic_hub.core.dag import DAGS, load_saved_dags
    all_dags = {**DAGS, **load_saved_dags()}
    return {
        "status": "ok",
        "dags": {name: {"description": d.description, "nodes": len(d.nodes), "edges": len(d.edges)}
                 for name, d in all_dags.items()},
    }


@app.get("/api/dag/{name}")
async def get_dag_detail(name: str):
    """Get full DAG definition."""
    from agentic_hub.core.dag import DAGS, load_saved_dags, get_dag
    dag = get_dag(name)
    if not dag:
        saved = load_saved_dags()
        dag = saved.get(name)
    if not dag:
        return {"status": "error", "message": f"DAG '{name}' not found"}
    return {"status": "ok", "dag": dag.to_dict()}


@app.post("/api/dag")
async def create_dag(request: Request):
    """Create/save a DAG definition."""
    from agentic_hub.core.dag import DAGDefinition, save_dag
    body = await request.json()
    try:
        dag = DAGDefinition.from_dict(body)
        errors = dag.validate()
        if errors:
            return {"status": "error", "errors": errors}
        path = save_dag(dag)
        return {"status": "ok", "message": f"DAG '{dag.name}' saved", "path": str(path)}
    except Exception as e:
        return {"status": "error", "message": str(e)}


@app.post("/api/dag/{name}/run")
async def run_dag(name: str, request: Request):
    """Execute a DAG workflow (non-streaming — returns full result)."""
    from agentic_hub.core.dag import DAGS, load_saved_dags, get_dag, DAGExecutor
    dag = get_dag(name)
    if not dag:
        saved = load_saved_dags()
        dag = saved.get(name)
    if not dag:
        return {"status": "error", "message": f"DAG '{name}' not found"}

    body = await request.json()
    message = body.get("message", "")
    if not message:
        return {"status": "error", "message": "message required"}

    executor = DAGExecutor(dag)
    events = []
    output = []
    async for chunk in executor.execute(message):
        events.append(chunk)
        if not chunk.startswith("§"):
            output.append(chunk)

    return {
        "status": "ok",
        "dag": name,
        "output": "".join(output),
        "events": events[-50:],  # Last 50 events
        "node_status": executor.get_status(),
    }


# ── Apple Shortcuts / iPhone Integration ──────────────────────────────
# Clean JSON endpoints for Siri, Shortcuts, widgets, NFC, camera, voice


@app.post("/api/shortcuts/chat")
async def shortcuts_chat(request: Request):
    """Chat with spiders from iPhone. Siri-friendly — fast local response."""
    import asyncio as _aio
    body = await request.json()
    message = body.get("message", "")
    if not message:
        return {"status": "error", "message": "message required"}
    try:
        # Fast path: raw Ollama HTTP call (skip wrappers, GPU scheduler, validation)
        import httpx
        async with httpx.AsyncClient(timeout=55) as hc:
            r = await hc.post("http://localhost:11434/api/generate", json={
                "model": "qwen-fast",
                "prompt": f"User: {message}\nAssistant:",
                "stream": False,
                "think": False,
                "options": {"num_predict": 150},
            })
            data = r.json()
            response = data.get("response", "").strip()
        return {"status": "ok", "response": response, "spider": "oracle"}
    except _aio.TimeoutError:
        return {"status": "ok", "response": "Spiders are still loading. Try again in a moment.", "spider": "system"}
    except Exception as e:
        return {"status": "error", "message": str(e)}


@app.get("/api/shortcuts/status")
async def shortcuts_status():
    """Spider status for Siri/widgets — clean JSON."""
    now = _time.time()
    spiders = []
    from agentic_hub.config import load_models_config
    config = load_models_config()
    spider_names = {"cockpit": "Rootwindow", "scholar": "Fangveil", "oracle": "Windowkernel",
                    "code_team": "Cachephantom", "ops": "Nullwisp", "automator": "Cryptweaver",
                    "money_maker": "Wirelash", "warroom": "Rootcipher", "lab": "Rootshroud"}
    for key, name in spider_names.items():
        activity = _spider_activity.get(key, {})
        status = activity.get("status", "idle") if now - activity.get("timestamp", 0) < 30 else "idle"
        model = config.get("agents", {}).get(key, {}).get("local_model", "")
        spiders.append({"name": name, "id": key, "status": status, "model": model,
                        "text": activity.get("text", "")})
    active = sum(1 for s in spiders if s["status"] == "working")
    return {"status": "ok", "spiders": spiders, "active": active, "total": len(spiders),
            "summary": f"{active}/{len(spiders)} spiders active"}


@app.get("/api/shortcuts/portfolio")
async def shortcuts_portfolio():
    """Portfolio summary for Siri — speaks net worth and accounts."""
    try:
        from agentic_hub.core.portfolio import get_portfolio_summary
        summary = get_portfolio_summary()
        accounts = []
        total = 0
        if isinstance(summary, dict):
            for acct in summary.get("accounts", []):
                bal = acct.get("balance", 0)
                total += bal
                accounts.append({"name": acct.get("name", ""), "balance": bal})
        return {"status": "ok", "net_worth": total, "accounts": accounts,
                "summary": f"Net worth: ${total:,.2f} across {len(accounts)} accounts"}
    except Exception as e:
        return {"status": "ok", "net_worth": 0, "accounts": [], "summary": "Portfolio not available"}


@app.get("/api/shortcuts/quote")
async def shortcuts_quote(s: str = ""):
    """Quick stock/crypto quote for Siri."""
    if not s:
        return {"status": "error", "message": "symbol parameter 's' required"}
    try:
        from agentic_hub.core.market_daemon import get_latest_intel
        intel = get_latest_intel()
        # Search in cached market data
        symbol = s.upper()
        return {"status": "ok", "symbol": symbol, "source": "market_daemon",
                "data": f"Latest intel available for {symbol}",
                "summary": f"{symbol} data retrieved from market daemon"}
    except Exception as e:
        return {"status": "error", "message": str(e)}


@app.post("/api/shortcuts/trade")
async def shortcuts_trade(request: Request):
    """Quick trade from iPhone."""
    body = await request.json()
    action = body.get("action", "")  # buy, sell
    symbol = body.get("symbol", "")
    amount = body.get("amount", 0)
    if not action or not symbol:
        return {"status": "error", "message": "action and symbol required"}
    # Route through Wirelash
    message = f"{action} {amount} {symbol}" if amount else f"{action} {symbol}"
    try:
        from agentic_hub.core.orchestrator import Orchestrator
        orch = Orchestrator()
        chunks = []
        async for chunk in orch.process(message):
            if not chunk.startswith("§") and not chunk.startswith("*["):
                chunks.append(chunk)
        return {"status": "ok", "response": "".join(chunks).strip(), "action": action, "symbol": symbol}
    except Exception as e:
        return {"status": "error", "message": str(e)}


@app.post("/api/shortcuts/vision")
async def shortcuts_vision(request: Request):
    """Analyze image from iPhone camera — send base64, get analysis."""
    body = await request.json()
    image = body.get("image_base64", body.get("image", ""))
    prompt = body.get("prompt", "Describe what you see in this image.")
    if not image:
        return {"status": "error", "message": "image_base64 required"}
    try:
        from agentic_hub.core.tools.builtin import VisionTool
        tool = VisionTool()
        result = await tool.execute(prompt=prompt, image=image, source_type="base64")
        return {"status": "ok", "analysis": result.output, "success": result.success}
    except Exception as e:
        return {"status": "error", "message": str(e)}


@app.post("/api/shortcuts/transcribe")
async def shortcuts_transcribe(request: Request):
    """Transcribe audio from iPhone voice memo."""
    import tempfile
    body = await request.body()
    if not body:
        return {"status": "error", "message": "audio data required (POST raw audio)"}
    try:
        with tempfile.NamedTemporaryFile(suffix=".m4a", delete=False) as f:
            f.write(body)
            tmp_path = f.name
        from agentic_hub.core.tools.builtin import TranscribeTool
        tool = TranscribeTool()
        result = await tool.execute(audio_path=tmp_path)
        Path(tmp_path).unlink(missing_ok=True)
        return {"status": "ok", "text": result.output, "success": result.success}
    except Exception as e:
        return {"status": "error", "message": str(e)}


@app.post("/api/shortcuts/analyze")
async def shortcuts_analyze(request: Request):
    """Analyze text from iPhone share sheet — summarize, extract entities, classify."""
    body = await request.json()
    text = body.get("text", "")
    analysis_type = body.get("type", "summarize")  # summarize, entities, classify
    if not text:
        return {"status": "error", "message": "text required"}
    try:
        if analysis_type == "entities":
            from agentic_hub.core.tools.builtin import HFNERTool
            tool = HFNERTool()
            result = await tool.execute(text=text)
        elif analysis_type == "classify":
            labels = body.get("labels", "positive,negative,neutral")
            from agentic_hub.core.tools.builtin import HFClassifyTool
            tool = HFClassifyTool()
            result = await tool.execute(text=text, labels=labels)
        else:
            from agentic_hub.core.tools.builtin import HFSummarizeTool
            tool = HFSummarizeTool()
            result = await tool.execute(text=text)
        return {"status": "ok", "result": result.output, "type": analysis_type, "success": result.success}
    except Exception as e:
        return {"status": "error", "message": str(e)}


@app.get("/api/shortcuts/briefing")
async def shortcuts_briefing():
    """Morning market briefing for Siri — reads a full summary."""
    parts = []
    try:
        from agentic_hub.core.market_daemon import get_latest_intel
        intel = get_latest_intel()
        if intel:
            parts.append(intel[:500])
    except Exception:
        parts.append("Market data not available")
    try:
        r = await get_metrics()
        parts.append(f"Revenue: ${r.get('revenue', 0):.2f}. Trades: {r.get('trades', 0)}. "
                      f"Strategies: {r.get('strategies', 0)} active. Uptime: {r.get('uptime_hours', 0)} hours.")
    except Exception:
        pass
    now = _time.time()
    active = sum(1 for v in _spider_activity.values() if now - v.get("timestamp", 0) < 30 and v.get("status") == "working")
    parts.append(f"{active} of 9 spiders currently active.")
    return {"status": "ok", "briefing": " ".join(parts),
            "summary": "Market briefing generated"}


@app.get("/api/shortcuts/widgets/portfolio")
async def shortcuts_widget_portfolio():
    """Widget-formatted portfolio data."""
    try:
        from agentic_hub.core.portfolio import get_portfolio_summary
        summary = get_portfolio_summary()
        return {"status": "ok", "widget": "portfolio", "data": summary}
    except Exception:
        return {"status": "ok", "widget": "portfolio", "data": {"net_worth": 0, "accounts": []}}


@app.get("/api/shortcuts/widgets/spiders")
async def shortcuts_widget_spiders():
    """Widget-formatted spider status."""
    result = await shortcuts_status()
    return {"status": "ok", "widget": "spiders", "data": result}


@app.post("/api/shortcuts/notify")
async def shortcuts_send_notify(request: Request):
    """Send a notification to iPhone (test endpoint)."""
    body = await request.json()
    title = body.get("title", "spider.Web")
    text = body.get("text", "")
    if not text:
        return {"status": "error", "message": "text required"}
    try:
        from agentic_hub.core.shortcuts_client import get_shortcuts_client
        client = get_shortcuts_client()
        result = await client.notify(title, text)
        return {"status": "ok", **result}
    except Exception as e:
        return {"status": "error", "message": str(e)}


STATIC_DIR = Path(__file__).parent / "static"


@app.get("/health")
async def health():
    return {"status": "ok", "service": "spider-web"}


# Serve index.html at root — dashboard accessible at http://localhost:8420/
@app.get("/")
async def serve_index():
    """Serve the spider.Web dashboard."""
    index = STATIC_DIR / "index.html"
    if index.exists():
        return FileResponse(str(index), media_type="text/html")
    return {"status": "error", "message": "Dashboard not found. Place index.html in src/agentic_hub/static/"}


# Serve static assets (favicon, future CSS/JS)
if STATIC_DIR.exists():
    app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")


@app.get("/api/config")
async def get_config():
    """Check which features are available."""
    from agentic_hub.config import get_settings, load_models_config
    s = get_settings()
    return {
        "has_anthropic": bool(s.anthropic_api_key),
        "has_openai": bool(s.openai_api_key),
        "has_google": bool(s.google_api_key),
        "has_deepseek": bool(s.deepseek_api_key),
        "has_xai": bool(s.xai_api_key),
        "has_hf": bool(s.hf_token),
        "has_oracle": bool(s.oci_compartment_id),
        "has_shortcuts": bool(s.pushcut_api_key or s.ifttt_webhook_key),
        "mode": "full" if s.anthropic_api_key else "local-only",
    }


class KeysRequest(BaseModel):
    anthropic_key: str = ""
    openai_key: str = ""
    google_key: str = ""
    deepseek_key: str = ""
    xai_key: str = ""
    hf_token: str = ""


@app.post("/api/config/keys")
async def save_keys(req: KeysRequest):
    """Save API keys to .env — validates format before saving."""
    import re as _re
    # SECURITY: validate key format to prevent injection
    KEY_FORMATS = {
        "ANTHROPIC_API_KEY": (req.anthropic_key, r"^sk-ant-"),
        "OPENAI_API_KEY": (req.openai_key, r"^sk-"),
        "GOOGLE_API_KEY": (req.google_key, r"^AIza"),
        "DEEPSEEK_API_KEY": (req.deepseek_key, r"^sk-"),
        "XAI_API_KEY": (req.xai_key, r"^xai-"),
        "HF_TOKEN": (req.hf_token, r"^hf_"),
    }
    env_path = Path(__file__).parent.parent.parent / ".env"
    try:
        content = env_path.read_text() if env_path.exists() else ""
        KEY_MAP = {}
        for env_name, (key_val, pattern) in KEY_FORMATS.items():
            if key_val:
                if not _re.match(pattern, key_val):
                    return {"status": "error", "message": f"Invalid format for {env_name}"}
                if not _re.match(r"^[A-Za-z0-9_\-]+$", key_val):
                    return {"status": "error", "message": f"Invalid characters in {env_name}"}
                KEY_MAP[env_name] = key_val
        for env_name, key_val in KEY_MAP.items():
            if key_val:
                if f"{env_name}=" in content:
                    content = re.sub(rf"{env_name}=.*", f"{env_name}={key_val}", content)
                else:
                    content += f"\n{env_name}={key_val}\n"
        env_path.write_text(content)
        saved = sum(1 for v in KEY_MAP.values() if v)
        return {"status": "ok", "message": f"{saved} key(s) saved. Restart server to apply."}
    except Exception as e:
        return {"status": "error", "message": str(e)}


# ── Vault / Encrypted Secrets ──────────────────────────────────────


class VaultInitRequest(BaseModel):
    master_password: str


class VaultSecretRequest(BaseModel):
    name: str
    value: str = ""


@app.post("/api/secrets/init")
async def vault_init(req: VaultInitRequest):
    """Initialize or unlock the encrypted vault with a master password."""
    from agentic_hub.core.secrets import init_vault, SecretVault
    try:
        vault = init_vault(req.master_password)
        return {
            "status": "ok",
            "message": "Vault unlocked" if SecretVault.vault_exists() else "Vault created",
            "keys": vault.list_keys(),
        }
    except ValueError as e:
        return {"status": "error", "message": str(e)}


@app.get("/api/secrets")
async def vault_list():
    """List all secret names in the vault (not values)."""
    from agentic_hub.core.secrets import get_vault
    vault = get_vault()
    if vault is None:
        return {"status": "locked", "keys": [], "message": "Vault not unlocked. POST /api/secrets/init first."}
    return {"status": "ok", "keys": vault.list_keys()}


@app.post("/api/secrets/store")
async def vault_store(req: VaultSecretRequest):
    """Store a secret in the encrypted vault."""
    from agentic_hub.core.secrets import get_vault
    vault = get_vault()
    if vault is None:
        return {"status": "error", "message": "Vault not unlocked"}
    if not req.name or not req.value:
        return {"status": "error", "message": "Both name and value required"}
    vault.store(req.name, req.value)
    return {"status": "ok", "message": f"Secret '{req.name}' stored"}


@app.delete("/api/secrets/{name}")
async def vault_delete(name: str):
    """Delete a secret from the vault."""
    from agentic_hub.core.secrets import get_vault
    vault = get_vault()
    if vault is None:
        return {"status": "error", "message": "Vault not unlocked"}
    deleted = vault.delete(name)
    if deleted:
        return {"status": "ok", "message": f"Secret '{name}' deleted"}
    return {"status": "error", "message": f"Secret '{name}' not found"}


@app.get("/api/secrets/status")
async def vault_status():
    """Check vault status — initialized, locked, or unlocked."""
    from agentic_hub.core.secrets import get_vault, SecretVault
    vault = get_vault()
    return {
        "initialized": SecretVault.initialized(),
        "vault_exists": SecretVault.vault_exists(),
        "unlocked": vault is not None,
        "key_count": len(vault.list_keys()) if vault else 0,
    }


# ── RBAC ───────────────────────────────────────────────────────────


class RoleAssignRequest(BaseModel):
    user_id: int = 1
    role: str


class RoleCreateRequest(BaseModel):
    name: str
    description: str = ""
    permissions: list[dict] = []  # [{"resource": "agent:*", "action": "invoke"}, ...]


@app.get("/api/rbac/roles")
async def rbac_list_roles():
    """List all roles with their permissions."""
    from agentic_hub.core.rbac import BUILT_IN_ROLES
    roles = {
        name: [p.to_dict() for p in perms]
        for name, perms in BUILT_IN_ROLES.items()
    }
    return {"status": "ok", "roles": roles}


@app.get("/api/rbac/user/{user_id}")
async def rbac_get_user_role(user_id: int):
    """Get the role assigned to a user."""
    from agentic_hub.core.rbac import get_rbac
    rbac = get_rbac()
    role = await rbac.get_user_role(user_id)
    allowed_tools = await rbac.get_allowed_tools(user_id)
    allowed_agents = await rbac.get_allowed_agents(user_id)
    return {
        "status": "ok",
        "user_id": user_id,
        "role": role,
        "allowed_tools": list(allowed_tools) if allowed_tools is not None else "all",
        "allowed_agents": list(allowed_agents) if allowed_agents is not None else "all",
    }


@app.post("/api/rbac/assign")
async def rbac_assign_role(req: RoleAssignRequest):
    """Assign a role to a user."""
    from agentic_hub.core.rbac import get_rbac
    rbac = get_rbac()
    ok = await rbac.assign_role(req.user_id, req.role)
    if ok:
        return {"status": "ok", "message": f"User {req.user_id} assigned role '{req.role}'"}
    return {"status": "error", "message": f"Role '{req.role}' not found"}


@app.post("/api/rbac/check")
async def rbac_check_permission(request: Request):
    """Check if a user has a specific permission."""
    from agentic_hub.core.rbac import get_rbac
    body = await request.json()
    rbac = get_rbac()
    allowed = await rbac.check_permission(
        body.get("user_id", 1),
        body.get("resource", ""),
        body.get("action", ""),
    )
    return {"status": "ok", "allowed": allowed}


@app.get("/api/preferences")
async def get_preferences():
    from agentic_hub.core.preferences import load_prefs
    return load_prefs()


@app.post("/api/preferences")
async def save_preferences(request: Request):
    from agentic_hub.core.preferences import load_prefs, save_prefs
    body = await request.json()
    prefs = load_prefs()
    prefs.update(body)
    save_prefs(prefs)
    return {"status": "ok"}


@app.get("/api/images/{filename}")
async def serve_image(filename: str):
    """Serve generated images — path traversal protected."""
    from fastapi import HTTPException
    base = (Path(__file__).parent.parent.parent / "data" / "images").resolve()
    img_path = (base / filename).resolve()
    if not img_path.is_relative_to(base) or not img_path.exists():
        raise HTTPException(status_code=403, detail="Forbidden")
    suffix = img_path.suffix.lower().lstrip(".")
    media = {"png": "image/png", "jpg": "image/jpeg", "jpeg": "image/jpeg",
             "gif": "image/gif", "webp": "image/webp"}.get(suffix, "application/octet-stream")
    return FileResponse(img_path, media_type=media)


@app.get("/")
async def serve_ui():
    return FileResponse(
        STATIC_DIR / "index.html",
        headers={"Cache-Control": "no-cache, no-store, must-revalidate", "Pragma": "no-cache", "Expires": "0"},
    )
