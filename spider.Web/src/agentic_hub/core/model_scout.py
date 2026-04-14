"""Model upgrade scout — searches HF on startup for models that beat current assignments.

Only suggests an upgrade when a candidate:
  1. Scores HIGHER on the relevant benchmark than the currently assigned model
  2. Uses EQUAL OR LESS VRAM (no heavier models)

Benchmark scores come from two sources:
  - Seed data: hardcoded known scores for common model families
  - Learned data: scores scraped from HF model cards at runtime, persisted to
    data/benchmark_scores.json so knowledge accumulates across restarts

When a model card lacks benchmark data, the candidate is silently skipped.

Runs once at launch as a background task. Writes upgrades to data/model_suggestions.json
and learned scores to data/benchmark_scores.json.
"""
from __future__ import annotations

import asyncio
import json
import logging
import re
import time
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)

DATA_DIR = Path(__file__).parent.parent.parent.parent / "data"
SUGGESTIONS_FILE = DATA_DIR / "model_suggestions.json"
SCORES_FILE = DATA_DIR / "benchmark_scores.json"

VRAM_BUDGET_GB = 8.0

# ── Seed benchmark scores (bootstrap — overridden by learned data) ───
# Sources: Open LLM Leaderboard, official papers, model cards
# chat:      MMLU (general knowledge, 0-100)
# code:      HumanEval pass@1 (code generation, 0-100)
# reasoning: GPQA Diamond (graduate-level reasoning, 0-100)
# embed:     MTEB average (embedding quality, 0-100)

_SEED_SCORES: dict[str, dict[str, float]] = {
    "qwen2.5-7b":       {"mmlu": 74.2, "humaneval": 61.6, "gpqa": 36.3},
    "qwen2.5-coder-7b": {"mmlu": 68.0, "humaneval": 88.4, "gpqa": 30.0},
    "qwen3-8b":         {"mmlu": 77.0, "humaneval": 72.0, "gpqa": 43.0},
    "qwen3.5-7b":       {"mmlu": 78.5, "humaneval": 74.0, "gpqa": 45.2},
    "qwen3.5-9b":       {"mmlu": 80.1, "humaneval": 76.0, "gpqa": 48.0},
    "llama-3.1-8b":     {"mmlu": 69.4, "humaneval": 62.0, "gpqa": 32.8},
    "llama-3.3-8b":     {"mmlu": 73.0, "humaneval": 68.0, "gpqa": 36.0},
    "llama-4-scout":    {"mmlu": 80.3, "humaneval": 73.0, "gpqa": 45.0},
    "deepseek-r1-7b":   {"mmlu": 52.5, "humaneval": 36.2, "gpqa": 49.1},
    "mistral-7b":       {"mmlu": 62.5, "humaneval": 30.5, "gpqa": 28.0},
    "codestral-7b":     {"mmlu": 60.0, "humaneval": 81.1, "gpqa": 25.0},
    "phi-4-7b":         {"mmlu": 78.0, "humaneval": 76.0, "gpqa": 42.0},
    "gemma-2-9b":       {"mmlu": 72.3, "humaneval": 54.0, "gpqa": 35.0},
    "gemma-3-9b":       {"mmlu": 75.0, "humaneval": 62.0, "gpqa": 39.0},
    "mxbai-embed-large": {"mteb": 54.4},
    "nomic-embed-text":  {"mteb": 55.7},
    "snowflake-arctic":  {"mteb": 56.1},
    "qwen-fast":         {"mmlu": 74.2, "humaneval": 61.6, "gpqa": 36.3},
    "qwen3-coder-abliterated": {"mmlu": 68.0, "humaneval": 88.4, "gpqa": 30.0},
    "qwen2.5-abliterated": {"mmlu": 74.2, "humaneval": 61.6, "gpqa": 36.3},
}

_ROLE_CONFIG = {
    "chat": {
        "benchmark": "mmlu",
        "benchmark_label": "MMLU",
        "queries": ["gguf instruct", "gguf chat 7b", "gguf chat 8b", "gguf qwen instruct"],
        "config_path": ("agents", "oracle", "local_model"),
    },
    "code": {
        "benchmark": "humaneval",
        "benchmark_label": "HumanEval",
        "queries": ["gguf coder", "gguf code instruct 7b", "gguf qwen coder"],
        "config_path": ("code_team", None, "local_coder"),
    },
    "reasoning": {
        "benchmark": "gpqa",
        "benchmark_label": "GPQA Diamond",
        "queries": ["gguf reasoning 7b", "gguf deepseek-r1", "gguf qwq"],
        "config_path": ("code_team", None, "local_reviewer"),
    },
    "embed": {
        "benchmark": "mteb",
        "benchmark_label": "MTEB Avg",
        "queries": ["embedding model", "gguf embed"],
        "config_path": None,
    },
}

_PARAM_TO_GB = {
    "1b": 0.8, "1.5b": 1.1, "2b": 1.5, "3b": 2.2, "4b": 2.8,
    "7b": 4.7, "8b": 5.5, "9b": 6.6, "12b": 8.0, "13b": 8.5,
    "14b": 9.5, "15b": 10.0, "22b": 14.0, "32b": 20.0, "70b": 42.0,
}


# ── Persistent score database ────────────────────────────────────

class ScoreDB:
    """Benchmark scores that persist across restarts. Seed + learned."""

    def __init__(self):
        self._scores: dict[str, dict[str, float]] = dict(_SEED_SCORES)
        self._load()

    def _load(self):
        """Merge learned scores from disk (overrides seeds)."""
        if SCORES_FILE.exists():
            try:
                learned = json.loads(SCORES_FILE.read_text())
                for key, scores in learned.get("scores", {}).items():
                    if key in self._scores:
                        self._scores[key].update(scores)
                    else:
                        self._scores[key] = scores
                logger.debug(f"Score DB: loaded {len(learned.get('scores', {}))} learned entries")
            except Exception as e:
                logger.debug(f"Score DB: can't load {SCORES_FILE}: {e}")

    def save(self):
        """Persist only learned scores (not seeds) to disk."""
        # Separate learned from seed
        learned = {}
        for key, scores in self._scores.items():
            if key not in _SEED_SCORES:
                learned[key] = scores
            else:
                # Check if any scores differ from seed (were updated)
                diff = {k: v for k, v in scores.items() if _SEED_SCORES.get(key, {}).get(k) != v}
                if diff:
                    learned[key] = scores

        data = {
            "updated": time.time(),
            "total_entries": len(self._scores),
            "learned_entries": len(learned),
            "scores": learned,
        }
        try:
            SCORES_FILE.parent.mkdir(parents=True, exist_ok=True)
            SCORES_FILE.write_text(json.dumps(data, indent=2))
        except Exception as e:
            logger.warning(f"Score DB: can't save: {e}")

    def lookup(self, model_name: str, benchmark: str) -> float | None:
        """Look up a score. Fuzzy matches model name against known keys."""
        name = model_name.lower().replace(":", "-").replace("/", "-")
        for key, scores in self._scores.items():
            if key in name or name in key:
                val = scores.get(benchmark)
                if val is not None:
                    return val
        return None

    def learn(self, model_key: str, benchmark: str, score: float, source: str = "hf_card"):
        """Record a newly discovered benchmark score."""
        key = model_key.lower().strip()
        if key not in self._scores:
            self._scores[key] = {}
        old = self._scores[key].get(benchmark)
        self._scores[key][benchmark] = score
        if old is None:
            logger.info(f"Score DB: learned {key} {benchmark}={score} (source: {source})")
        elif old != score:
            logger.info(f"Score DB: updated {key} {benchmark}={old}→{score} (source: {source})")

    @property
    def count(self) -> int:
        return len(self._scores)


# ── HF model card benchmark scraping ─────────────────────────────

# Patterns to extract scores from model card metadata or README
_BENCHMARK_PATTERNS = {
    "mmlu": [
        re.compile(r"MMLU[^:]*?[:=\s]+(\d{1,2}\.?\d*)", re.IGNORECASE),
        re.compile(r"mmlu_pro[^:]*?[:=\s]+(\d{1,2}\.?\d*)", re.IGNORECASE),
    ],
    "humaneval": [
        re.compile(r"HumanEval[^:]*?[:=\s]+(\d{1,2}\.?\d*)", re.IGNORECASE),
        re.compile(r"pass@1[^:]*?[:=\s]+(\d{1,2}\.?\d*)", re.IGNORECASE),
    ],
    "gpqa": [
        re.compile(r"GPQA[^:]*?[:=\s]+(\d{1,2}\.?\d*)", re.IGNORECASE),
    ],
    "mteb": [
        re.compile(r"MTEB[^:]*?[:=\s]+(\d{1,2}\.?\d*)", re.IGNORECASE),
    ],
}


def _scrape_scores_from_card(model_id: str, hf: Any) -> dict[str, float]:
    """Try to extract benchmark scores from a HF model card."""
    scraped: dict[str, float] = {}
    try:
        info = hf.model_info(model_id)
        tags = info.get("tags", [])
        # Some model cards encode scores in tags like "mmlu:74.2"
        for tag in tags:
            for benchmark, patterns in _BENCHMARK_PATTERNS.items():
                for pat in patterns:
                    m = pat.search(tag)
                    if m:
                        val = float(m.group(1))
                        if 0 < val <= 100:
                            scraped[benchmark] = val
    except Exception:
        pass
    return scraped


# ── Core scout logic ─────────────────────────────────────────────

def _extract_param_count(model_id: str) -> str | None:
    match = re.search(r"(\d+\.?\d*)b(?:\b|[-_.])", model_id.lower())
    if match:
        raw = match.group(1)
        if raw.endswith(".0"):
            raw = raw[:-2]
        return f"{raw}b"
    return None


def _estimate_vram_gb(param_str: str) -> float:
    if param_str in _PARAM_TO_GB:
        return _PARAM_TO_GB[param_str]
    match = re.match(r"(\d+\.?\d*)", param_str)
    if match:
        return float(match.group(1)) * 0.65
    return 99.0


def _get_current_model(role: str, config: dict) -> str:
    cfg = _ROLE_CONFIG[role]
    if cfg["config_path"] is None:
        return "mxbai-embed-large"
    section, subsection, field = cfg["config_path"]
    if subsection is None:
        return config.get(section, {}).get(field, "")
    return config.get(section, {}).get(subsection, {}).get(field, "")


def _get_installed_vram(model_name: str, installed: list[dict]) -> float | None:
    for m in installed:
        if m.get("name", "").startswith(model_name.split(":")[0]):
            return m.get("size", 0) / (1024**3)
    param_str = _extract_param_count(model_name)
    if param_str:
        return _estimate_vram_gb(param_str)
    return None


async def scout_models() -> dict:
    """Search HF for models that score higher AND use equal/less VRAM."""
    from agentic_hub.core.ollama_client import get_ollama
    from agentic_hub.config import load_models_config

    ollama = get_ollama()
    try:
        installed = await ollama.list_models()
    except Exception as e:
        logger.warning(f"Model scout: can't reach Ollama: {e}")
        return {}

    config = load_models_config()
    score_db = ScoreDB()
    upgrades: dict[str, dict] = {}

    try:
        from agentic_hub.core.hf_client import HuggingFaceClient
        hf = HuggingFaceClient()
    except Exception as e:
        logger.warning(f"Model scout: HF client unavailable: {e}")
        return {}

    for role, role_cfg in _ROLE_CONFIG.items():
        benchmark = role_cfg["benchmark"]
        current_model = _get_current_model(role, config)
        if not current_model:
            continue

        current_score = score_db.lookup(current_model, benchmark)
        current_vram = _get_installed_vram(current_model, installed)

        if current_score is None:
            logger.debug(f"Scout [{role}]: no {benchmark} score for '{current_model}', skipping")
            continue

        best: dict[str, Any] | None = None
        seen: set[str] = set()

        for query in role_cfg["queries"]:
            try:
                for sort in ["trending", "downloads"]:
                    models = hf.list_models(query=query, sort=sort, limit=15)
                    for m in models:
                        model_id = m.get("id", "")
                        if model_id in seen:
                            continue
                        seen.add(model_id)

                        param_str = _extract_param_count(model_id)
                        if not param_str:
                            continue
                        est_vram = _estimate_vram_gb(param_str)
                        if est_vram > VRAM_BUDGET_GB:
                            continue
                        if current_vram and est_vram > current_vram * 1.05:
                            continue

                        # Check score: DB first, then try scraping card
                        candidate_score = score_db.lookup(model_id, benchmark)
                        if candidate_score is None:
                            scraped = _scrape_scores_from_card(model_id, hf)
                            for bm, val in scraped.items():
                                # Normalize the key for storage
                                base = model_id.split("/")[-1].lower() if "/" in model_id else model_id.lower()
                                score_db.learn(base, bm, val, source="hf_card")
                            candidate_score = scraped.get(benchmark)

                        if candidate_score is None or candidate_score <= current_score:
                            continue

                        if best is None or candidate_score > best["score"]:
                            best = {
                                "model_id": model_id,
                                "params": param_str,
                                "est_vram_gb": round(est_vram, 1),
                                "score": candidate_score,
                                "score_delta": round(candidate_score - current_score, 1),
                                "benchmark": role_cfg["benchmark_label"],
                                "downloads": m.get("downloads", 0),
                            }
            except Exception as e:
                logger.debug(f"Scout: search '{query}' failed: {e}")

        if best:
            upgrades[role] = {
                "current_model": current_model,
                "current_score": current_score,
                "current_vram_gb": round(current_vram, 1) if current_vram else None,
                "upgrade": best,
            }
            logger.info(
                f"⬆️  Upgrade [{role}]: {best['model_id']} "
                f"({best['benchmark']}: {best['score']} vs {current_score}, "
                f"+{best['score_delta']}) "
                f"~{best['est_vram_gb']}GB — replaces {current_model}"
            )
        else:
            logger.info(f"✓  Scout [{role}]: {current_model} is optimal")

    # Persist learned scores
    score_db.save()
    logger.info(f"Score DB: {score_db.count} models tracked ({SCORES_FILE.name})")

    result = {
        "timestamp": time.time(),
        "vram_budget_gb": VRAM_BUDGET_GB,
        "upgrades": upgrades,
        "roles_scanned": list(_ROLE_CONFIG.keys()),
    }

    try:
        SUGGESTIONS_FILE.parent.mkdir(parents=True, exist_ok=True)
        SUGGESTIONS_FILE.write_text(json.dumps(result, indent=2, default=str))
    except Exception as e:
        logger.warning(f"Scout: can't write suggestions: {e}")

    if not upgrades:
        logger.info("Model scout: all assignments optimal — no upgrades")

    return result


async def run_scout_background():
    """Startup background task. Delays 15s to let model preload finish."""
    await asyncio.sleep(15)
    try:
        await scout_models()
    except Exception as e:
        logger.warning(f"Model scout failed (non-fatal): {e}")
