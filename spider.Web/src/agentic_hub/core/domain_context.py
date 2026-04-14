"""Domain context injection — loads hard-learned knowledge into agent system prompts.

Reads Salesforce knowledge (critical gotchas) and user feedback memories,
caches the result, and returns a compact string for system prompt injection.
This means agents KNOW the gotchas without having to call sf_knowledge first.
"""
from __future__ import annotations

import logging
from pathlib import Path

import yaml

logger = logging.getLogger(__name__)

_cached_context: str | None = None
_cache_mtime: float = 0.0

KNOWLEDGE_PATH = Path(__file__).parent.parent.parent.parent / "data" / "salesforce_knowledge.yaml"
MEMORY_DIR = Path.home() / ".claude" / "projects" / "-home-bobbyblowssmoke" / "memory"


def _load_critical_knowledge() -> str:
    """Load critical/high severity entries from salesforce_knowledge.yaml."""
    if not KNOWLEDGE_PATH.exists():
        return ""
    try:
        with open(KNOWLEDGE_PATH) as f:
            kb = yaml.safe_load(f)
        knowledge = kb.get("knowledge", {})

        lines = []
        for section, entries in knowledge.items():
            for entry in entries:
                sev = entry.get("severity", "low")
                if sev in ("critical", "high"):
                    lines.append(f"- [{section.upper()}] {entry['title']}: "
                                 f"{entry.get('fix', entry.get('content', ''))[:200].strip()}")
        return "\n".join(lines)
    except Exception as e:
        logger.warning(f"Failed to load SF knowledge: {e}")
        return ""


def _load_feedback_memories() -> str:
    """Load user feedback memories (short actionable rules)."""
    if not MEMORY_DIR.exists():
        return ""
    lines = []
    try:
        for f in sorted(MEMORY_DIR.glob("feedback_*.md")):
            text = f.read_text()
            # Extract just the rule (first non-frontmatter, non-blank line after ---)
            in_body = False
            past_frontmatter = 0
            for line in text.splitlines():
                if line.strip() == "---":
                    past_frontmatter += 1
                    if past_frontmatter == 2:
                        in_body = True
                    continue
                if in_body and line.strip():
                    lines.append(f"- {line.strip()[:200]}")
                    break  # Just the first line (the rule itself)
    except Exception as e:
        logger.warning(f"Failed to load feedback memories: {e}")
    return "\n".join(lines)


def _load_project_state() -> str:
    """Load key project state — what's blocked, what's the current context."""
    lines = [
        "- Salesforce project: ~/salesforce-backup/ (API v66.0, org: joedev)",
        "- UWM integration: 9/10 APIs done. AUS + Loan Export blocked on UWM creds.",
        "- Key LWCs: pricingWorkspace, loanHighlights, createLoanAction, nexaDocUploader",
        "- Deploy: sf project deploy start --source-dir force-app -o joedev",
        "- ALWAYS scope test runs: --test-level RunSpecifiedTests (UwmLoanCreateControllerTest is broken)",
    ]
    return "\n".join(lines)


def get_domain_context() -> str:
    """Get cached domain context for system prompt injection.

    Returns a compact string (~400-600 tokens) with:
    1. Critical Salesforce gotchas (so agents don't hit known traps)
    2. User feedback rules (behavioral corrections from past sessions)
    3. Project state summary (what's done, what's blocked)

    Hot-reloads when salesforce_knowledge.yaml changes.
    """
    global _cached_context, _cache_mtime

    current_mtime = KNOWLEDGE_PATH.stat().st_mtime if KNOWLEDGE_PATH.exists() else 0
    if _cached_context is not None and current_mtime == _cache_mtime:
        return _cached_context

    sf_knowledge = _load_critical_knowledge()
    feedback = _load_feedback_memories()
    project = _load_project_state()

    parts = ["## Domain Knowledge (auto-injected)\n"]
    if sf_knowledge:
        parts.append("### Salesforce Critical Gotchas")
        parts.append(sf_knowledge)
    if feedback:
        parts.append("\n### User Rules (from past sessions)")
        parts.append(feedback)
    if project:
        parts.append("\n### Project State")
        parts.append(project)
    parts.append("\n### Available Tools")
    parts.append("- `salesforce` tool: deploy, retrieve, test, query Salesforce org")
    parts.append("- `sf_knowledge` tool: query full domain knowledge base (27 entries, 8 topics)")
    parts.append("- `sf_validate` tool: CamouFox browser screenshot of Salesforce pages")
    parts.append("- Call `sf_knowledge(topic='all')` before any non-trivial Salesforce change")

    _cached_context = "\n".join(parts)
    _cache_mtime = current_mtime
    return _cached_context
