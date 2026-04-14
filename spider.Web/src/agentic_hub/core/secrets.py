"""Encrypted secret storage — Fernet-encrypted JSON vault.

Replaces plaintext .env for API keys. Master password derives a Fernet key
via PBKDF2 (480k iterations). Vault stored at data/vault.enc, salt at
data/.vault_salt. Transparent fallback: if vault doesn't exist, .env works.
"""
from __future__ import annotations

import base64
import json
import logging
import os
from pathlib import Path
from typing import Any

from cryptography.fernet import Fernet, InvalidToken
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes

logger = logging.getLogger(__name__)

DATA_DIR = Path(__file__).parent.parent.parent.parent / "data"
VAULT_PATH = DATA_DIR / "vault.enc"
SALT_PATH = DATA_DIR / ".vault_salt"
PBKDF2_ITERATIONS = 480_000


def _derive_key(password: str, salt: bytes) -> bytes:
    """Derive Fernet key from master password + salt via PBKDF2."""
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=PBKDF2_ITERATIONS,
    )
    return base64.urlsafe_b64encode(kdf.derive(password.encode()))


class SecretVault:
    """Fernet-encrypted JSON vault for API keys and secrets.

    Usage:
        vault = SecretVault("my-master-password")
        vault.store("ANTHROPIC_API_KEY", "sk-ant-...")
        key = vault.retrieve("ANTHROPIC_API_KEY")
    """

    def __init__(self, master_password: str):
        self._password = master_password
        self._salt = self._load_or_create_salt()
        self._key = _derive_key(master_password, self._salt)
        self._fernet = Fernet(self._key)
        self._secrets: dict[str, str] = {}
        self._load()

    def _load_or_create_salt(self) -> bytes:
        """Load existing salt or generate a new 16-byte salt."""
        if SALT_PATH.exists():
            return SALT_PATH.read_bytes()
        salt = os.urandom(16)
        SALT_PATH.parent.mkdir(parents=True, exist_ok=True)
        SALT_PATH.write_bytes(salt)
        # Restrict permissions to owner only
        SALT_PATH.chmod(0o600)
        return salt

    def _load(self) -> None:
        """Load and decrypt the vault."""
        if not VAULT_PATH.exists():
            self._secrets = {}
            return
        try:
            encrypted = VAULT_PATH.read_bytes()
            decrypted = self._fernet.decrypt(encrypted)
            self._secrets = json.loads(decrypted.decode())
        except InvalidToken:
            logger.error("Vault decryption failed — wrong master password")
            raise ValueError("Wrong master password — cannot decrypt vault")
        except Exception as e:
            logger.error(f"Vault load error: {e}")
            self._secrets = {}

    def _save(self) -> None:
        """Encrypt and save the vault to disk."""
        plaintext = json.dumps(self._secrets, indent=2).encode()
        encrypted = self._fernet.encrypt(plaintext)
        VAULT_PATH.parent.mkdir(parents=True, exist_ok=True)
        VAULT_PATH.write_bytes(encrypted)
        VAULT_PATH.chmod(0o600)

    def store(self, name: str, value: str) -> None:
        """Store a secret in the vault."""
        self._secrets[name] = value
        self._save()
        logger.info(f"Secret stored: {name}")

    def retrieve(self, name: str) -> str | None:
        """Retrieve a secret by name. Returns None if not found."""
        return self._secrets.get(name)

    def list_keys(self) -> list[str]:
        """List all secret names (not values)."""
        return list(self._secrets.keys())

    def delete(self, name: str) -> bool:
        """Remove a secret. Returns True if it existed."""
        if name in self._secrets:
            del self._secrets[name]
            self._save()
            logger.info(f"Secret deleted: {name}")
            return True
        return False

    def has(self, name: str) -> bool:
        """Check if a secret exists."""
        return name in self._secrets

    @staticmethod
    def vault_exists() -> bool:
        """Check if an encrypted vault file exists on disk."""
        return VAULT_PATH.exists()

    @staticmethod
    def initialized() -> bool:
        """Check if vault infrastructure (salt) exists."""
        return SALT_PATH.exists()


# Singleton — lazily initialized with master password
_vault: SecretVault | None = None
_master_password: str | None = None


def init_vault(master_password: str) -> SecretVault:
    """Initialize the vault singleton with a master password."""
    global _vault, _master_password
    _master_password = master_password
    _vault = SecretVault(master_password)
    return _vault


def get_vault() -> SecretVault | None:
    """Get the vault singleton. Returns None if not initialized."""
    return _vault


def try_load_vault_from_env() -> SecretVault | None:
    """Try to load vault using VAULT_PASSWORD from environment.

    This allows non-interactive startup: set VAULT_PASSWORD in .env
    or as an environment variable, and the vault auto-unlocks.
    """
    global _vault, _master_password
    if _vault is not None:
        return _vault

    password = os.environ.get("VAULT_PASSWORD", "")
    if not password:
        return None

    if not SecretVault.vault_exists():
        return None

    try:
        _master_password = password
        _vault = SecretVault(password)
        logger.info("Vault auto-unlocked via VAULT_PASSWORD")
        return _vault
    except ValueError:
        logger.warning("VAULT_PASSWORD set but decryption failed")
        return None


# Map vault secret names to Settings field names
VAULT_TO_SETTINGS = {
    "ANTHROPIC_API_KEY": "anthropic_api_key",
    "OPENAI_API_KEY": "openai_api_key",
    "GOOGLE_API_KEY": "google_api_key",
    "DEEPSEEK_API_KEY": "deepseek_api_key",
    "XAI_API_KEY": "xai_api_key",
    "DATABASE_URL": "database_url",
    "REDIS_URL": "redis_url",
    "PLAID_CLIENT_ID": "plaid_client_id",
    "PLAID_SECRET": "plaid_secret",
}


def overlay_vault_secrets(settings: Any) -> None:
    """Overlay vault secrets onto Settings, filling empty fields only.

    Called by config.get_settings() after loading from .env.
    Vault values take precedence only when the .env value is empty.
    """
    vault = get_vault() or try_load_vault_from_env()
    if vault is None:
        return

    for vault_name, settings_field in VAULT_TO_SETTINGS.items():
        current = getattr(settings, settings_field, "")
        if not current:
            secret = vault.retrieve(vault_name)
            if secret:
                object.__setattr__(settings, settings_field, secret)
                logger.debug(f"Loaded {vault_name} from vault")
