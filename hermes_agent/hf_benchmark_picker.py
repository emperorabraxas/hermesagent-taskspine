from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from huggingface_hub import HfApi


@dataclass
class Candidate:
    model_id: str
    score: float
    metrics: dict[str, float]
    reason: str


def _extract_benchmark_metrics(card_data: dict[str, Any]) -> dict[str, float]:
    """
    Hugging Face model cards sometimes include a `model-index` block with eval results.
    This extracts a small set of common metrics when available.
    """
    out: dict[str, float] = {}
    model_index = card_data.get("model-index") or card_data.get("model_index") or []
    if not isinstance(model_index, list):
        return out
    for entry in model_index:
        results = entry.get("results") if isinstance(entry, dict) else None
        if not isinstance(results, list):
            continue
        for r in results:
            metrics = r.get("metrics") if isinstance(r, dict) else None
            if not isinstance(metrics, list):
                continue
            for m in metrics:
                name = (m.get("name") or "").strip().lower()
                val = m.get("value")
                if not isinstance(val, (int, float)) or not name:
                    continue
                if "mmlu" in name:
                    out["mmlu"] = max(out.get("mmlu", 0.0), float(val))
                if "humaneval" in name or "human eval" in name:
                    out["humaneval"] = max(out.get("humaneval", 0.0), float(val))
                if "gsm8k" in name:
                    out["gsm8k"] = max(out.get("gsm8k", 0.0), float(val))
    return out


def pick_best_low_tier_model(
    *,
    goal: str,
    max_params_b: float = 3.0,
    limit: int = 25,
) -> list[Candidate]:
    """
    Best-effort benchmark-driven picker using HF card benchmark metadata.

    Note: This intentionally does NOT use likes/downloads as the ranking signal.
    """
    api = HfApi()

    # Search base models (not GGUF repos) so we can read benchmark metadata.
    # We keep this query broad; the ranking is metric-driven when available.
    query = "instruct"
    models = api.list_models(search=query, task="text-generation", limit=limit, full=True)

    candidates: list[Candidate] = []
    for m in models:
        model_id = getattr(m, "modelId", None) or getattr(m, "id", None) or ""
        if not model_id:
            continue
        card_data = getattr(m, "cardData", None) or {}
        metrics = _extract_benchmark_metrics(card_data if isinstance(card_data, dict) else {})
        if not metrics:
            continue

        # Simple goal-weighted score.
        # - summarize/extract/classify favor general knowledge (MMLU) + reasoning (GSM8K)
        # - code favors HumanEval when present
        mmlu = metrics.get("mmlu", 0.0)
        he = metrics.get("humaneval", 0.0)
        gsm = metrics.get("gsm8k", 0.0)

        if goal == "code":
            score = (he * 0.65) + (mmlu * 0.25) + (gsm * 0.10)
            reason = "weighted: HumanEval>MMLU>GSM8K"
        else:
            score = (mmlu * 0.55) + (gsm * 0.30) + (he * 0.15)
            reason = "weighted: MMLU>GSM8K>HumanEval"

        candidates.append(Candidate(model_id=model_id, score=score, metrics=metrics, reason=reason))

    candidates.sort(key=lambda c: c.score, reverse=True)
    return candidates[:10]

