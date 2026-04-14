# Agentic Hub

Local multi-agent AI platform. Opus orchestrates everything — routes to local models (Ollama) for research/chat/automation, and runs Opus ↔ Codex collaborative coding for code tasks.

## Stack
- **Backend**: Python FastAPI (src/agentic_hub/)
- **Frontend**: Next.js (web/) — cyberpunk/neon abyss theme
- **CLI**: Typer (`hub` command)
- **Models**: Ollama (local) + Anthropic API (Opus) + OpenAI API (Codex)
- **DB**: Postgres :5434, Redis :6380

## Commands
```bash
# Dev server
cd spider.Web && source .venv/bin/activate
uvicorn agentic_hub.main:app --reload --port 8420

# CLI
hub chat                    # Interactive chat
hub agents list             # Show agents and their models
hub models list             # Show available models
hub stats                   # Gamification stats

# Infrastructure
docker compose up -d        # Start Postgres + Redis
alembic upgrade head        # Run migrations
```

## Architecture
- `core/orchestrator.py` — Opus brain: classifies user input, routes to agents, verifies results
- `core/code_team.py` — Opus ↔ Codex multi-turn coding collaboration
- `core/ollama_client.py` — Async wrapper for Ollama HTTP API
- `core/gpu_scheduler.py` — Single-GPU model loading/unloading coordinator
- `agents/` — Local model agents (Scholar, Automator, Oracle)
- `config/models.yaml` — Agent ↔ model mapping (user-configurable)
