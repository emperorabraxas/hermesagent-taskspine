# spider.Web

Local multi-agent AI platform (FastAPI + Ollama) with a web dashboard, CLI, and optional Tauri desktop shell.

## Quickstart

```bash
cd spider.Web
bash scripts/setup.sh
```

Note: `scripts/` is a directory; run `scripts/setup.sh` (not `scripts`).

Then run:

```bash
# starts API on http://localhost:8420 and opens the browser UI
hub
```

Or equivalently:
```bash
spiders
```

Or API-only:

```bash
hub serve
```

Or terminal UI:

```bash
hub tui
```

## Auth Token

On server start, an auth token is printed to the server terminal and also written to:

```bash
cat "$(python3 -c "import tempfile; print(tempfile.gettempdir())")/.spider-web-token"
```

The browser UI will prompt for this token and stores it in `localStorage` (`spider_auth_token`).

## Optional Services

- Postgres + Redis (for persistence / analytics / streams): `docker compose up -d`
  - Postgres: `127.0.0.1:5434`
  - Redis: `127.0.0.1:6380`
- Ollama (local models): `ollama serve`

Environment variables live in `.env` (copy from `.env.example`).

## Cloudflare Tunnel (Optional)

This machine is configured with a Cloudflare tunnel in `~/.cloudflared/config.yml`:

- Tunnel: `spiderweb`
- Hostname: `spiders.wirelash.dev`
- Service: `http://localhost:8420`

Run it:

```bash
cloudflared tunnel --config ~/.cloudflared/config.yml run spiderweb
```

The UI still requires the auth token; use the token shown by the server.

## Windows

Recommended: run under WSL2 so `bash scripts/setup.sh` works as-is.

Native Windows (PowerShell):
```powershell
cd spider.Web
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -e .
copy .env.example .env
spiders serve
```
