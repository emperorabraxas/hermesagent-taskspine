# hermesagent-taskspine

This repo is a fork of `NousResearch/hermes-agent` with **Taskspine** customizations:

- A strict lane model for code work:
  - **Low tier**: local models (Ollama) to draft ideas/workflows.
  - **Mid tier**: planning/review/validation (Codex / other paid model).
  - **High tier**: execution (Claude Code), when needed.
- GitHub webhook wiring docs + scripts (HTTPS-first).
- MCP repo config (`.mcp.json`) and Dependabot updates.

Docs:
- `taskspine/docs/github-webhook.md`

Project plugin (optional):
- `.hermes/plugins/taskspine/` (enable with `HERMES_ENABLE_PROJECT_PLUGINS=1`)
- Suggest command (leaderboard-first): `hermes taskspine models suggest --include-ollama`
- Default leaderboard dataset: `OpenEvals/leaderboard-data` (coding=`sweVerified_score`, tool-use=`terminalBench_score`, chat=`aggregate_score`)

Taskspine routing parameters (env vars):
- `TASKSPINE_WEBHOOK_PUBLIC_URL` (e.g. `https://hooks.wirelash.dev/github/webhook`)
- Low lane: `TASKSPINE_LOW_BASE_URL` (default `http://127.0.0.1:11434/v1`), `TASKSPINE_LOW_MODEL` (optional)
- Mid lane (OpenAI): `TASKSPINE_MID_OPENAI_BASE_URL` (default `https://api.openai.com/v1`), `TASKSPINE_MID_OPENAI_MODEL` (`latest` or explicit)
- High lane (Claude Code ACP): `TASKSPINE_HIGH_ACP_COMMAND` (default `claude`), `TASKSPINE_HIGH_MODEL` (default `claude-opus-4-6`), `TASKSPINE_HIGH_ACP_ARGS` (optional)
