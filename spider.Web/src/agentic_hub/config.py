from __future__ import annotations

import yaml
from pathlib import Path
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # Cloud API keys
    anthropic_api_key: str = ""
    openai_api_key: str = ""
    google_api_key: str = ""
    deepseek_api_key: str = ""
    xai_api_key: str = ""
    hf_token: str = ""  # Hugging Face Hub token (HF_TOKEN in .env)
    oci_compartment_id: str = ""  # Oracle Cloud compartment OCID
    oci_config_profile: str = "DEFAULT"  # OCI config profile name
    pushcut_api_key: str = ""  # Pushcut API key for Apple Shortcuts triggers
    pushcut_webhook_url: str = ""  # Pushcut webhook base URL
    ifttt_webhook_key: str = ""  # IFTTT Maker webhook key (fallback)
    semantic_scholar_api_key: str = ""  # Optional — free API, key raises rate limit to 100 req/s

    # Plaid
    plaid_client_id: str = ""
    plaid_secret: str = ""
    plaid_environment: str = "sandbox"  # sandbox | development | production

    # Ollama
    ollama_base_url: str = "http://localhost:11434"

    # Database — credentials via .env, not hardcoded
    database_url: str = ""  # set DATABASE_URL in .env

    # Redis
    redis_url: str = ""  # set REDIS_URL in .env

    # Server
    hub_host: str = "127.0.0.1"  # SECURITY: localhost only. Use --host 0.0.0.0 to expose.
    cors_origins: str = ""  # Comma-separated additional CORS origins (default: localhost only)
    hub_port: int = 8420

    # Model overrides (take precedence over models.yaml)
    scholar_model: str = ""
    automator_model: str = ""
    oracle_model: str = ""

    # GPU scheduler — keep models loaded longer to avoid reload latency
    model_keep_alive: str = "30m"  # was 10m — 30m reduces GPU swap frequency

    # Semantic cache
    semantic_cache_enabled: bool = True
    semantic_cache_threshold: float = 0.92
    semantic_cache_ttl: int = 86400  # 24 hours


# Hot-reload cache for models.yaml
_models_config_cache: dict | None = None
_models_config_mtime: float = 0.0


def load_models_config(config_path: Path | None = None) -> dict:
    """Load agent-to-model mapping from models.yaml.

    Hot-reload: re-reads the file when its mtime changes, so edits
    to models.yaml take effect without restarting the server.
    """
    global _models_config_cache, _models_config_mtime

    if config_path is None:
        config_path = Path(__file__).parent.parent.parent / "config" / "models.yaml"
    if not config_path.exists():
        raise FileNotFoundError(f"Models config not found: {config_path}")

    current_mtime = config_path.stat().st_mtime
    if _models_config_cache is not None and current_mtime == _models_config_mtime:
        return _models_config_cache

    with open(config_path) as f:
        _models_config_cache = yaml.safe_load(f)
    _models_config_mtime = current_mtime
    return _models_config_cache


def write_models_config(config: dict, config_path: Path | None = None) -> Path:
    """Write models.yaml safely — invalidates hot-reload cache."""
    global _models_config_cache, _models_config_mtime

    if config_path is None:
        config_path = Path(__file__).parent.parent.parent / "config" / "models.yaml"

    config_path.parent.mkdir(parents=True, exist_ok=True)
    with open(config_path, "w") as f:
        yaml.dump(config, f, default_flow_style=False, sort_keys=False, allow_unicode=True)

    # Invalidate cache so next load_models_config() reads fresh
    _models_config_cache = None
    _models_config_mtime = 0.0
    return config_path


# Singleton
_settings: Settings | None = None


def get_settings() -> Settings:
    global _settings
    if _settings is None:
        _settings = Settings()
        # Overlay encrypted vault secrets (fills empty fields only)
        try:
            from agentic_hub.core.secrets import overlay_vault_secrets
            overlay_vault_secrets(_settings)
        except Exception:
            pass  # Vault not available — .env values stand
    return _settings
