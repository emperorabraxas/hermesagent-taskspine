"""Idle Research Daemon — spiders work while you sleep.

When no user is actively chatting, local spiders run background research:
- Scholar: indexes new files, summarizes recent changes, builds knowledge
- Automator: monitors system health, disk, services, git status
- Oracle: pre-processes common questions, builds context caches

When the user starts chatting → daemon pauses, GPU freed for active work.
When chat goes idle again → daemon resumes research.

All findings stored to data/idle_research/ for context injection.
"""
from __future__ import annotations

import asyncio
import json
import logging
import time
from datetime import datetime
from pathlib import Path

logger = logging.getLogger(__name__)

DATA_DIR = Path(__file__).parent.parent.parent.parent / "data"
RESEARCH_DIR = DATA_DIR / "idle_research"

# How long after last user message before entering idle mode
IDLE_THRESHOLD = 120  # 2 minutes of no activity
# Research cycle interval when idle
RESEARCH_INTERVAL = 300  # 5 minutes between research cycles

# Track activity
_last_user_activity: float = 0.0
_is_idle = True
_pause_event = asyncio.Event()


def mark_active():
    """Called when the user sends a message."""
    global _last_user_activity, _is_idle
    _last_user_activity = time.time()
    if _is_idle:
        _is_idle = False
        logger.info("User active — idle research paused")


def mark_idle():
    """Called when idle threshold is reached."""
    global _is_idle
    if not _is_idle:
        _is_idle = True
        logger.info("User idle — resuming background research")


def is_idle() -> bool:
    """Check if the system is currently idle."""
    return _is_idle


def _ensure_dirs():
    RESEARCH_DIR.mkdir(parents=True, exist_ok=True)


def _save_research(spider: str, data: dict):
    """Save research findings."""
    _ensure_dirs()
    data["timestamp"] = datetime.now().isoformat()
    data["spider"] = spider
    filepath = RESEARCH_DIR / f"{spider}_latest.json"
    filepath.write_text(json.dumps(data, indent=2, default=str))

    # Rolling log
    log_file = RESEARCH_DIR / f"{spider}_log.jsonl"
    with open(log_file, "a") as f:
        f.write(json.dumps(data, default=str) + "\n")
    # Trim
    try:
        lines = log_file.read_text().strip().split("\n")
        if len(lines) > 100:
            log_file.write_text("\n".join(lines[-100:]) + "\n")
    except Exception:
        pass


async def _idle_watcher():
    """Monitor user activity and toggle idle state."""
    global _is_idle
    while True:
        if _last_user_activity > 0:
            elapsed = time.time() - _last_user_activity
            if elapsed >= IDLE_THRESHOLD and not _is_idle:
                mark_idle()
            elif elapsed < IDLE_THRESHOLD and _is_idle:
                _is_idle = False
        await asyncio.sleep(10)


async def _scholar_research():
    """Scholar's idle work: research current projects using conversation history.

    Uses recent chat history to understand what the user is working on,
    then proactively researches related codebases, docs, and patterns.
    Also keeps the RAG index fresh.
    """
    while True:
        if not _is_idle:
            await asyncio.sleep(30)
            continue

        try:
            # 1. Keep RAG index fresh
            from agentic_hub.core.rag import RAGPipeline
            rag = RAGPipeline()
            home = Path.home()

            indexed = 0
            for d in ["spider.Web/src", "project", "uwm-integration/src",
                       "salesforce-backup", "archive_sentinel_anime"]:
                p = home / d
                if p.exists():
                    result = await rag.index_directory(p)
                    indexed += result.get("files_indexed", 0)

            # 2. Project-aware research using conversation history
            from agentic_hub.api.chat import _sessions
            from agentic_hub.config import get_settings
            from agentic_hub.core.gpu_scheduler import get_gpu_scheduler
            from agentic_hub.core.ollama_client import get_ollama

            # Get recent conversation context
            recent_messages = []
            for sid, memory in list(_sessions.items())[-3:]:
                history = memory.get_history(last_n=5)
                for msg in history:
                    if msg.get("role") == "user":
                        recent_messages.append(msg.get("content", "")[:200])

            if recent_messages:
                settings = get_settings()
                scholar_model = "qwen-fast"  # local, uncensored
                scheduler = get_gpu_scheduler()
                await scheduler.ensure_model(scholar_model)
                ollama = get_ollama()

                # Ask Scholar to research what the user has been working on
                context = "\n".join(f"- {m}" for m in recent_messages[-5:])
                research = await ollama.chat(
                    model=scholar_model,
                    messages=[
                        {"role": "system", "content": (
                            "You are a research spider doing background investigation. "
                            "Based on the user's recent conversations, identify:\n"
                            "1. What projects they're actively working on\n"
                            "2. Key technical challenges they mentioned\n"
                            "3. Patterns or solutions that might help them\n"
                            "4. Files or APIs they should check next\n"
                            "Be concise. Use bullet points. Focus on actionable insights."
                        )},
                        {"role": "user", "content": f"Recent user conversations:\n{context}"},
                    ],
                    stream=False,
                    keep_alive=settings.model_keep_alive,
                )

                _save_research("scholar", {
                    "action": "project_research",
                    "files_indexed": indexed,
                    "conversation_topics": recent_messages[-3:],
                    "research_findings": research,
                    "stats": rag.get_stats(),
                })
                logger.info(f"Scholar idle: indexed {indexed} files, researched active projects")
            else:
                if indexed > 0:
                    _save_research("scholar", {
                        "action": "reindex",
                        "files_indexed": indexed,
                        "stats": rag.get_stats(),
                    })

        except Exception as e:
            logger.debug(f"Scholar idle research failed: {e}")

        await asyncio.sleep(RESEARCH_INTERVAL)


async def _automator_research():
    """Automator's idle work: system health monitoring."""
    import subprocess

    while True:
        if not _is_idle:
            await asyncio.sleep(30)
            continue

        try:
            checks = {}

            # Disk space — no shell
            try:
                result = subprocess.run(
                    ["df", "-h", "/", "/home", "--output=pcent,avail"],
                    capture_output=True, text=True, timeout=5
                )
                lines = result.stdout.strip().split("\n")
                checks["disk"] = "\n".join(lines[1:]) if len(lines) > 1 else result.stdout.strip()
            except Exception:
                pass

            # Memory — no shell
            try:
                result = subprocess.run(
                    ["free", "-h"],
                    capture_output=True, text=True, timeout=5
                )
                lines = result.stdout.strip().split("\n")
                checks["memory"] = "\n".join(lines[:2])
            except Exception:
                pass

            # GPU — try rocm-smi first, then nvidia-smi (no shell)
            try:
                result = subprocess.run(
                    ["rocm-smi", "--showuse", "--showtemp"],
                    capture_output=True, text=True, timeout=5
                )
                checks["gpu"] = result.stdout.strip() if result.returncode == 0 else ""
            except FileNotFoundError:
                pass
            if not checks.get("gpu"):
                try:
                    result = subprocess.run(
                        ["nvidia-smi", "--query-gpu=utilization.gpu,temperature.gpu,memory.used",
                         "--format=csv,noheader"],
                        capture_output=True, text=True, timeout=5
                    )
                    checks["gpu"] = result.stdout.strip() if result.returncode == 0 else "no GPU info"
                except FileNotFoundError:
                    checks["gpu"] = "no GPU info"

            # Ollama models loaded — httpx instead of curl
            try:
                import httpx
                resp = httpx.get("http://localhost:11434/api/ps", timeout=5)
                checks["ollama_loaded"] = resp.text[:500]
            except Exception:
                pass

            # Git status of spider.Web — no shell
            try:
                result = subprocess.run(
                    ["git", "status", "--short"],
                    capture_output=True, text=True, timeout=5,
                    cwd=str(Path.home() / "spider.Web"),
                )
                checks["git_status"] = result.stdout.strip()[:500]
            except Exception:
                pass

            _save_research("automator", {
                "action": "system_health",
                "checks": checks,
            })

        except Exception as e:
            logger.debug(f"Automator idle research failed: {e}")

        await asyncio.sleep(RESEARCH_INTERVAL)


def get_idle_research_context() -> str:
    """Get latest idle research findings for context injection."""
    _ensure_dirs()
    parts = []

    for spider in ["scholar", "automator"]:
        filepath = RESEARCH_DIR / f"{spider}_latest.json"
        if filepath.exists():
            try:
                data = json.loads(filepath.read_text())
                ts = data.get("timestamp", "?")
                action = data.get("action", "?")

                if spider == "scholar":
                    stats = data.get("stats", {})
                    parts.append(f"Scholar (idle): {stats.get('total_files', 0)} files indexed, "
                                f"{stats.get('total_chunks', 0)} RAG chunks ({ts[:16]})")
                elif spider == "automator":
                    checks = data.get("checks", {})
                    disk = checks.get("disk", "?")
                    mem = checks.get("memory", "?").split("\n")[-1] if checks.get("memory") else "?"
                    parts.append(f"Automator (idle): disk {disk}, mem {mem} ({ts[:16]})")
            except Exception:
                pass

    return "\n".join(parts) if parts else ""


async def start_idle_daemon():
    """Start all idle research loops. Called on server startup."""
    _ensure_dirs()
    logger.info("Idle research daemon starting — spiders work while you rest")
    asyncio.create_task(_idle_watcher())
    asyncio.create_task(_scholar_research())
    asyncio.create_task(_automator_research())
