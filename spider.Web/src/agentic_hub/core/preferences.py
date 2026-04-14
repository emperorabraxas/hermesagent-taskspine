"""User preferences — persisted to JSON, injected into agent prompts."""
from __future__ import annotations

import json
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

PREFS_FILE = Path(__file__).parent.parent.parent.parent / "data" / "preferences.json"

DEFAULT_PREFS = {
    # Profile
    "username": "spider.BOB",
    "preferred_language": "Python",
    "project_dirs": ["~/spider.Web", "~/project", "~/uwm-integration"],
    "current_focus": "",

    # Response style
    "response_style": "concise",      # concise | verbose | code-only
    "explain_code": True,              # Include explanations with code
    "use_japanese": True,              # Japanese accents in UI

    # Agent behavior
    "auto_execute": True,              # Auto-run bash blocks
    "opus_review_level": "thorough",   # light | thorough | aggressive
    "code_team_rounds": 3,             # Max conversation rounds
    "scholar_use_rag": True,           # RAG for scholar

    # Models (override models.yaml)
    "scholar_model": "",
    "automator_model": "",
    "oracle_model": "",
    "coder_model": "",

    # API Keys (display only — actual keys in .env)
    "has_anthropic": False,
    "has_openai": False,

    # System
    "theme": "tokyo-ghoul",            # tokyo-ghoul | cyberpunk | minimal
    "ship_scale": 0.78,
    "terminal_only": False,            # True = spiders launches TUI instead of browser
}


def load_prefs() -> dict:
    """Load preferences from disk."""
    PREFS_FILE.parent.mkdir(parents=True, exist_ok=True)
    if PREFS_FILE.exists():
        try:
            with open(PREFS_FILE) as f:
                saved = json.load(f)
            # Merge with defaults (add new keys)
            merged = {**DEFAULT_PREFS, **saved}
            return merged
        except Exception as e:
            logger.warning(f"Failed to load prefs: {e}")
    return dict(DEFAULT_PREFS)


def save_prefs(prefs: dict) -> None:
    """Save preferences to disk."""
    PREFS_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(PREFS_FILE, "w") as f:
        json.dump(prefs, f, indent=2)


def get_agent_context(prefs: dict) -> str:
    """Build context string from preferences to inject into agent prompts."""
    parts = []
    if prefs.get("username"):
        parts.append(f"User: {prefs['username']}")
    if prefs.get("preferred_language"):
        parts.append(f"Preferred language: {prefs['preferred_language']}")
    if prefs.get("current_focus"):
        parts.append(f"Currently working on: {prefs['current_focus']}")
    if prefs.get("project_dirs"):
        parts.append(f"Project dirs: {', '.join(prefs['project_dirs'])}")
    if prefs.get("response_style") == "concise":
        parts.append("Be concise — short answers, minimal explanation.")
    elif prefs.get("response_style") == "verbose":
        parts.append("Be thorough — detailed explanations, examples, alternatives.")
    elif prefs.get("response_style") == "code-only":
        parts.append("Code only — no explanations unless asked. Just the code.")
    if not prefs.get("explain_code"):
        parts.append("Do NOT explain code unless asked.")
    return "\n".join(parts)
