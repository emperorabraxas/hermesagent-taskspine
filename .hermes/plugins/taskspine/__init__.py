from __future__ import annotations

import json
import os
import platform
import re
import subprocess
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Tuple


@dataclass(frozen=True)
class SystemProfile:
    os: str
    arch: str
    cpu: str
    mem_total_gib: float


def _read_mem_total_gib_linux() -> Optional[float]:
    try:
        with open("/proc/meminfo", "r", encoding="utf-8") as f:
            for line in f:
                if line.startswith("MemTotal:"):
                    parts = line.split()
                    # MemTotal: <kB>
                    kb = float(parts[1])
                    return kb / 1024.0 / 1024.0
    except Exception:
        return None
    return None


def _read_cpu_model_linux() -> Optional[str]:
    try:
        out = subprocess.check_output(["lscpu"], text=True, timeout=2)
    except Exception:
        return None
    for line in out.splitlines():
        if ":" not in line:
            continue
        k, v = line.split(":", 1)
        if k.strip().lower() == "model name":
            return v.strip()
    return None


def detect_system_profile() -> SystemProfile:
    mem = _read_mem_total_gib_linux()
    cpu = _read_cpu_model_linux()
    return SystemProfile(
        os=platform.system(),
        arch=platform.machine(),
        cpu=cpu or platform.processor() or "unknown",
        mem_total_gib=float(mem) if mem is not None else 0.0,
    )


def _try_list_ollama_models() -> List[str]:
    """Best-effort: list installed Ollama models if Ollama is reachable."""
    try:
        import requests  # Hermes dependency
    except Exception:
        return []
    try:
        resp = requests.get("http://127.0.0.1:11434/api/tags", timeout=1.5)
        resp.raise_for_status()
        data = resp.json() or {}
        models = data.get("models") or []
        names: List[str] = []
        for m in models:
            name = (m or {}).get("name")
            if isinstance(name, str) and name.strip():
                names.append(name.strip())
        return sorted(set(names))
    except Exception:
        return []


def _score_from_hf_model_index(model_info: Dict[str, Any]) -> Optional[float]:
    """Extract a single numeric score from Hugging Face `model-index` if present.

    This intentionally ignores likes/downloads. It only considers benchmark results
    declared in the model card metadata.
    """
    card = model_info.get("cardData") or {}
    model_index = card.get("model-index")
    if not isinstance(model_index, list) or not model_index:
        return None

    # Heuristic: pick the best "overall-ish" metric we can find.
    best: Optional[float] = None
    for entry in model_index:
        results = (entry or {}).get("results") or []
        for r in results:
            metrics = (r or {}).get("metrics") or []
            for m in metrics:
                val = (m or {}).get("value")
                if isinstance(val, (int, float)):
                    best = val if best is None else max(best, float(val))
    return best


def _fetch_hf_model_info(repo_id: str, hf_token: Optional[str]) -> Tuple[Optional[Dict[str, Any]], Optional[str]]:
    try:
        import requests  # Hermes dependency
    except Exception as e:
        return None, f"requests not available: {e}"

    headers = {}
    if hf_token:
        headers["Authorization"] = f"Bearer {hf_token}"
    url = f"https://huggingface.co/api/models/{repo_id}"
    try:
        resp = requests.get(url, headers=headers, timeout=5)
        if resp.status_code >= 400:
            return None, f"HF API HTTP {resp.status_code}"
        return resp.json(), None
    except Exception as e:
        return None, str(e)


def suggest_low_tier_models(
    system: SystemProfile,
    candidates: List[Dict[str, str]],
    hf_token: Optional[str],
) -> Dict[str, Any]:
    """Suggest a low-tier local model using benchmark-first logic.

    Inputs:
      candidates: list of {"name": <local_name>, "hf": <optional_hf_repo_id>}
    """
    scored: List[Dict[str, Any]] = []
    for c in candidates:
        name = (c.get("name") or "").strip()
        hf = (c.get("hf") or "").strip()
        entry: Dict[str, Any] = {"name": name, "hf": hf or None, "score": None, "score_source": None}
        if hf:
            info, err = _fetch_hf_model_info(hf, hf_token)
            if info:
                score = _score_from_hf_model_index(info)
                if score is not None:
                    entry["score"] = score
                    entry["score_source"] = "hf:model-index"
            elif err:
                entry["score_source"] = f"hf:error:{err}"
        scored.append(entry)

    # Prefer benchmark-scored entries; fall back to name heuristics if no scores.
    scored_with = [x for x in scored if isinstance(x.get("score"), (int, float))]
    if scored_with:
        scored_with.sort(key=lambda x: float(x["score"]), reverse=True)
        best = scored_with[0]
    else:
        def _name_rank(n: str) -> int:
            n = n.lower()
            # Conservative CPU-first heuristic.
            if re.search(r"(coder|code)", n):
                return 3
            if re.search(r"(instruct|chat)", n):
                return 2
            return 1

        scored.sort(key=lambda x: _name_rank(x.get("name") or ""), reverse=True)
        best = scored[0] if scored else {"name": None}

    return {
        "system": {
            "os": system.os,
            "arch": system.arch,
            "cpu": system.cpu,
            "mem_total_gib": system.mem_total_gib,
        },
        "recommendation": best,
        "candidates": scored,
        "notes": [
            "Selection ignores likes/downloads; uses benchmark results from HF model-index when available.",
            "Provide candidate HF repo IDs to enable benchmark-first scoring.",
        ],
    }


def _parse_candidates(raw: str) -> List[Dict[str, str]]:
    """Parse candidates from 'local=hf,local2=hf2,local3'."""
    raw = (raw or "").strip()
    if not raw:
        return []
    out: List[Dict[str, str]] = []
    for part in raw.split(","):
        part = part.strip()
        if not part:
            continue
        if "=" in part:
            name, hf = part.split("=", 1)
            out.append({"name": name.strip(), "hf": hf.strip()})
        else:
            out.append({"name": part, "hf": ""})
    return out


def _setup_taskspine_cmd(subparser) -> None:
    sub = subparser.add_subparsers(dest="taskspine_cmd", required=True)

    models = sub.add_parser("models", help="Taskspine model utilities")
    models_sub = models.add_subparsers(dest="models_cmd", required=True)

    suggest = models_sub.add_parser("suggest", help="Suggest a low-tier local model")
    suggest.add_argument(
        "--candidates",
        default="",
        help="Comma-separated candidates: local=hf_repo_id,local2=hf_repo_id2,local3",
    )
    suggest.add_argument(
        "--hf-token-env",
        default="HF_TOKEN",
        help="Env var name containing a Hugging Face token (optional)",
    )
    suggest.add_argument(
        "--include-ollama",
        action="store_true",
        help="Include installed Ollama model names as candidates (no HF mapping).",
    )


def _handle_taskspine_cmd(args) -> None:
    if args.taskspine_cmd == "models" and args.models_cmd == "suggest":
        hf_token = os.environ.get(args.hf_token_env, "").strip() or None
        candidates = _parse_candidates(args.candidates)
        if args.include_ollama:
            for name in _try_list_ollama_models():
                candidates.append({"name": name, "hf": ""})
        system = detect_system_profile()
        result = suggest_low_tier_models(system=system, candidates=candidates, hf_token=hf_token)
        print(json.dumps(result, indent=2, sort_keys=True))
        return

    raise SystemExit("Unknown taskspine subcommand")


def register(ctx) -> None:
    ctx.register_cli_command(
        name="taskspine",
        help="Taskspine utilities (model routing helpers, webhook docs, etc.)",
        description="Local model suggestion is benchmark-first (HF model-index), never likes/downloads.",
        setup_fn=_setup_taskspine_cmd,
        handler_fn=_handle_taskspine_cmd,
    )

