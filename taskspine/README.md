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
- Command: `hermes taskspine models suggest --include-ollama`
