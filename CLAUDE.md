# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

This is a **personal workspace** (home directory as git repo) containing multiple independent projects across different tech stacks. The `.gitignore` uses a whitelist approach — everything is ignored by default, with specific directories and files explicitly allowed.

## Project Map

| Directory | What it is | Stack |
|-----------|-----------|-------|
| `project/` | NEON_ABYSS dual-arch Windows cross-compilation build system | C, Makefile, MinGW-w64 |
| `test/` | Godot 4.6 game project (Forward Plus renderer, Jolt Physics) | GDScript, Godot Engine |
| `uwm-integration/` | UWM auth token handler (token acquisition + refresh flows) | Node.js, axios, xmlbuilder2 |
| `Solution1/` | Empty C# solution stub | .NET, JetBrains Rider |
| `archive_sentinel_anime/` | Anime preservation system with RAG pipeline | Python, YAML, NLP/ML |
| `salesforce-backup/` | Salesforce LWC project with CI tooling | JavaScript, LWC, Jest, ESLint, Husky |
| `ai-dotfiles/` | AI assistant configs for JetBrains/Cursor editors | Markdown, JSON configs |
| `sf-project/` | Empty Salesforce metadata stub | — |
| `agentic-hub/` | Spider Web — local multi-agent AI platform, Opus orchestrator | Python, FastAPI, Ollama, Next.js |

## Build & Run Commands

### project/ (NEON_ABYSS)
```bash
cd project && make build    # Cross-compile for win32 + win64
cd project && make clean    # Remove build artifacts
```

### uwm-integration/
```bash
cd uwm-integration && npm run test:auth-token     # Test auth-token flow
cd uwm-integration && npm run test:auth-refresh    # Test auth-refresh flow
cd uwm-integration && node run-local.js            # Run locally
```
Requires `.env` file with credentials (not committed).

### salesforce-backup/
```bash
cd salesforce-backup && npm run lint          # ESLint
cd salesforce-backup && npm run test:unit     # Jest unit tests (LWC)
cd salesforce-backup && npm run prettier      # Format code
```
Has Husky pre-commit hooks with lint-staged.

### archive_sentinel_anime/
Python scripts under `scripts/`. Follow `registry.yaml` for the 11-step build order. Has its own `.venv`.

### agentic-hub/ (Spider Web)
```bash
cd agentic-hub && source .venv/bin/activate
hub serve                    # Start API server on :8420
hub chat                     # Interactive chat REPL
hub agents list              # Show agents and models
hub models list              # Show Ollama models
hub setup                    # Re-run API key setup
docker compose up -d         # Start Postgres + Redis
```
Requires `.env` with API keys (optional — works in local-only mode without them).

### test/ (Godot)
Open in Godot 4.6 editor. Export preset configured for Windows Desktop.

## Architecture Notes

- **uwm-integration** uses `run-local.js` as a harness that loads event JSON files from `events/` and routes to the appropriate handler — mimicking a serverless invocation pattern locally.
- **archive_sentinel_anime** follows a multi-stage pipeline defined in `registry.yaml`: ingest, normalize, extract, index, then RAG-powered search/chat.
- **Root `package.json`** exists at `~/package.json` with shared deps (axios, dotenv, xmlbuilder2, nodemon) — this is separate from per-project package.json files.

## Git Conventions

- Single branch (`main`), single remote
- The `.gitignore` whitelists specific directories — new project directories must be added to `.gitignore` to be tracked
- Git user: `emperorabraxas`
