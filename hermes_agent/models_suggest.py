from __future__ import annotations

from hermes_agent.config import HermesConfig
from hermes_agent.hf_benchmark_picker import pick_best_low_tier_model
from hermes_agent.system_profile import get_system_profile


def suggest_low_tier_model(*, task: str, goal: str, cfg: HermesConfig) -> dict:
    """
    Suggest a low-tier model based on benchmark metadata when available.
    This does not install/pull models; it prints copy/paste commands.
    """
    profile = get_system_profile()

    # Heuristic: if VRAM is heavily used, bias toward CPU run instructions.
    vram_pressure = 0.0
    if profile.vram_total_bytes:
        vram_pressure = profile.vram_used_bytes / max(profile.vram_total_bytes, 1)

    top = pick_best_low_tier_model(goal=goal if goal in ("code",) else "general")
    if not top:
        return {
            "report": (
                "No benchmark metadata found via Hugging Face card data.\n"
                "Recommendation: pick a small instruct model (1–3B) and import a GGUF build manually.\n"
            ),
            "candidates": [],
            "system": profile.__dict__,
        }

    best = top[0]
    max_gb = cfg.low.max_gguf_gb

    cpu_hint = " (CPU-preferred)" if (cfg.low.cpu_preferred or vram_pressure > 0.85) else ""
    report = []
    report.append("Hermes low-tier model suggestion (benchmark-driven)\n")
    report.append(f"System: {profile.cpu_threads} threads, {profile.mem_total_gb:.1f} GB RAM, {profile.vram_total_gb:.1f} GB VRAM ({profile.vram_used_gb:.1f} used)\n")
    report.append(f"Goal: {goal}\n")
    report.append(f"Chosen base model: {best.model_id}{cpu_hint}\n")
    report.append(f"Benchmarks seen in card data: {best.metrics} ({best.reason})\n\n")
    report.append("Next steps (no auto-install):\n")
    report.append(f"- Find a GGUF repo for `{best.model_id}` and import under ~{max_gb:.1f}GB:\n")
    report.append("  `hub models import --hf <gguf_repo_id> --quant Q4_K_M --max-size {max_gb} --template chatml`\n".format(max_gb=max_gb))
    report.append("- Run on CPU if VRAM is busy:\n")
    report.append("  `OLLAMA_NUM_GPU=0 ollama run <ollama_model_name> \"<prompt>\"`\n")

    return {
        "report": "".join(report),
        "best": {
            "model_id": best.model_id,
            "metrics": best.metrics,
            "score": best.score,
            "reason": best.reason,
        },
        "candidates": [
            {"model_id": c.model_id, "score": c.score, "metrics": c.metrics, "reason": c.reason}
            for c in top
        ],
        "system": profile.__dict__,
        "task": task,
        "goal": goal,
    }

