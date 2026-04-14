# HermesAgent (Taskspine harness)

Not affiliated with `NousResearch/hermes-agent`. This repo is a separate project that implements the “router → planner → executor” harness we designed in this chat.

HermesAgent is a strict orchestration harness that routes work across tiers:

- **Low (local)**: cheap ideation + workflow (no edits)
- **Plan (Codex)**: produce a decision-complete execution packet + confidence score
- **Execute (Claude Code)**: edit/execute only when you explicitly approve

Hard rules:

- HermesAgent **never edits target repos directly** (it only prepares prompts/commands).
- HermesAgent **never commits**.
- HermesAgent **asks every time** before using paid models and before running Claude.
- HermesAgent **never auto-starts** Ollama or pulls models.

## Install (editable)

```bash
cd ~/work/hermes-agent
python -m venv .venv
source .venv/bin/activate
python -m pip install -e .
```

## Quickstart

Initialize config and optionally set a git remote:

```bash
hermes init
# later:
hermes init --remote git@github.com:YOU/hermes-agent.git
```

Run a task against a repo:

```bash
cd /path/to/some/repo
hermes run "Add a CLI flag to enable X and update tests"
```

If Ollama is not reachable, Hermes can still suggest a low-tier model (benchmark-based) and print an import command:

```bash
hermes models suggest "summarize logs" --goal summarize
```
