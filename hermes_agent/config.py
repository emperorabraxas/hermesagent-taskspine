from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml


def _default_config_path() -> Path:
    xdg = os.environ.get("XDG_CONFIG_HOME")
    base = Path(xdg) if xdg else Path.home() / ".config"
    return base / "hermes-agent" / "config.yaml"


@dataclass
class GitConfig:
    remote: str = ""


@dataclass
class OpenAIConfig:
    model: str = "gpt-5.4"
    max_tokens: int = 1800
    confidence_threshold: float = 0.78


@dataclass
class ClaudeConfig:
    enabled: bool = True
    command: str = "claude"
    model: str = ""  # optional; let user default take over
    permission_mode: str = "acceptEdits"


@dataclass
class LowTierConfig:
    # Hermes does not auto-install; these are used for suggestion + prompts.
    ollama_base_url: str = "http://localhost:11434"
    local_model: str = ""  # if empty, Hermes will only suggest models; it won't run Ollama
    cpu_preferred: bool = True
    max_gguf_gb: float = 3.0


@dataclass
class HermesConfig:
    git: GitConfig
    openai: OpenAIConfig
    claude: ClaudeConfig
    low: LowTierConfig

    @staticmethod
    def default() -> "HermesConfig":
        return HermesConfig(
            git=GitConfig(),
            openai=OpenAIConfig(),
            claude=ClaudeConfig(),
            low=LowTierConfig(),
        )

    @staticmethod
    def load(path: Path) -> "HermesConfig":
        data = yaml.safe_load(path.read_text()) or {}
        git = GitConfig(**(data.get("git") or {}))
        openai = OpenAIConfig(**(data.get("openai") or {}))
        claude = ClaudeConfig(**(data.get("claude") or {}))
        low = LowTierConfig(**(data.get("low") or {}))
        return HermesConfig(git=git, openai=openai, claude=claude, low=low)

    def save(self, path: Path) -> None:
        obj: dict[str, Any] = {
            "git": {"remote": self.git.remote},
            "openai": {
                "model": self.openai.model,
                "max_tokens": self.openai.max_tokens,
                "confidence_threshold": self.openai.confidence_threshold,
            },
            "claude": {
                "enabled": self.claude.enabled,
                "command": self.claude.command,
                "model": self.claude.model,
                "permission_mode": self.claude.permission_mode,
            },
            "low": {
                "ollama_base_url": self.low.ollama_base_url,
                "local_model": self.low.local_model,
                "cpu_preferred": self.low.cpu_preferred,
                "max_gguf_gb": self.low.max_gguf_gb,
            },
        }
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(yaml.safe_dump(obj, sort_keys=False))


def ensure_config(path: Path | None = None) -> Path:
    cfg_path = path or _default_config_path()
    if cfg_path.exists():
        return cfg_path
    cfg = HermesConfig.default()
    cfg.save(cfg_path)
    return cfg_path
