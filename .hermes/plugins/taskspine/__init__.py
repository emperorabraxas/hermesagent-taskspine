from __future__ import annotations

import json
import os
import platform
import re
import subprocess
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Tuple


DEFAULT_LEADERBOARD_DATASET = "OpenEvals/leaderboard-data"
DEFAULT_LEADERBOARD_CONFIG = "default"
DEFAULT_LEADERBOARD_SPLIT = "train"

# Metrics in OpenEvals/leaderboard-data.
DEFAULT_CODING_METRIC = "sweVerified_score"
DEFAULT_TOOL_USE_METRIC = "terminalBench_score"
DEFAULT_CHAT_METRIC = "aggregate_score"


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

def _normalize_key(s: str) -> str:
    s = (s or "").strip().lower()
    s = re.sub(r"\s+", " ", s)
    return s


def _fetch_hf_dataset_rows(
    dataset: str,
    config: str,
    split: str,
    hf_token: Optional[str],
) -> Tuple[List[Dict[str, Any]], Optional[str]]:
    """Fetch dataset rows via HF Dataset Viewer `/rows` API.

    Uses a tiny slice API (max 100 rows per request), so we page until
    exhaustion. This is intentionally dependency-free (no pandas/pyarrow).
    """
    try:
        import requests  # Hermes dependency
    except Exception as e:
        return [], f"requests not available: {e}"

    headers: Dict[str, str] = {}
    if hf_token:
        headers["Authorization"] = f"Bearer {hf_token}"

    all_rows: List[Dict[str, Any]] = []
    offset = 0
    while True:
        url = (
            "https://datasets-server.huggingface.co/rows"
            f"?dataset={dataset}&config={config}&split={split}&offset={offset}&length=100"
        )
        try:
            resp = requests.get(url, headers=headers, timeout=8)
            if resp.status_code >= 400:
                return all_rows, f"HF rows API HTTP {resp.status_code}"
            data = resp.json() or {}
        except Exception as e:
            return all_rows, str(e)

        rows = data.get("rows") or []
        if not isinstance(rows, list) or not rows:
            break
        for r in rows:
            row = (r or {}).get("row")
            if isinstance(row, dict):
                all_rows.append(row)
        if len(rows) < 100:
            break
        offset += 100

    return all_rows, None


def _index_leaderboard_rows(rows: List[Dict[str, Any]]) -> Dict[str, Dict[str, Any]]:
    idx: Dict[str, Dict[str, Any]] = {}
    for r in rows:
        for key in ("model_id", "model_name"):
            val = r.get(key)
            if isinstance(val, str) and val.strip():
                idx[_normalize_key(val)] = r
    return idx


def _extract_metric(row: Dict[str, Any], metric_key: str) -> Optional[float]:
    val = row.get(metric_key)
    if isinstance(val, (int, float)):
        return float(val)
    return None


def _leaderboard_scores_for_candidate(
    candidate: Dict[str, str],
    leaderboard_index: Dict[str, Dict[str, Any]],
    coding_metric: str,
    tool_use_metric: str,
    chat_metric: str,
) -> Tuple[Optional[Dict[str, Any]], Optional[str]]:
    keys_to_try: List[str] = []
    for k in ("hf", "name"):
        v = (candidate.get(k) or "").strip()
        if v:
            keys_to_try.append(v)
    for k in keys_to_try:
        row = leaderboard_index.get(_normalize_key(k))
        if row:
            return (
                {
                    "matched_key": k,
                    "model_id": row.get("model_id"),
                    "model_name": row.get("model_name"),
                    "coding": _extract_metric(row, coding_metric),
                    "tool_use": _extract_metric(row, tool_use_metric),
                    "general_chat": _extract_metric(row, chat_metric),
                    "metrics": {
                        coding_metric: _extract_metric(row, coding_metric),
                        tool_use_metric: _extract_metric(row, tool_use_metric),
                        chat_metric: _extract_metric(row, chat_metric),
                    },
                },
                None,
            )
    return None, "no leaderboard match"


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
    leaderboard_dataset: str,
    leaderboard_config: str,
    leaderboard_split: str,
    coding_metric: str,
    tool_use_metric: str,
    chat_metric: str,
    w_coding: float,
    w_tool_use: float,
    w_chat: float,
) -> Dict[str, Any]:
    """Suggest a low-tier local model using benchmark-first logic.

    Inputs:
      candidates: list of {"name": <local_name>, "hf": <optional_hf_repo_id>}
    """
    leaderboard_rows, leaderboard_err = _fetch_hf_dataset_rows(
        dataset=leaderboard_dataset,
        config=leaderboard_config,
        split=leaderboard_split,
        hf_token=hf_token,
    )
    leaderboard_index = _index_leaderboard_rows(leaderboard_rows) if leaderboard_rows else {}

    scored: List[Dict[str, Any]] = []
    for c in candidates:
        name = (c.get("name") or "").strip()
        hf = (c.get("hf") or "").strip()
        entry: Dict[str, Any] = {
            "name": name,
            "hf": hf or None,
            "score": None,
            "score_source": None,
            "leaderboard": None,
            "leaderboard_error": None,
        }

        # Leaderboard override (benchmark dataset) — preferred when a match exists.
        if leaderboard_index:
            lb, lb_err = _leaderboard_scores_for_candidate(
                candidate={"name": name, "hf": hf},
                leaderboard_index=leaderboard_index,
                coding_metric=coding_metric,
                tool_use_metric=tool_use_metric,
                chat_metric=chat_metric,
            )
            entry["leaderboard"] = lb
            entry["leaderboard_error"] = lb_err

            if lb:
                parts: List[Tuple[float, float]] = []
                if lb.get("coding") is not None:
                    parts.append((w_coding, float(lb["coding"])))
                if lb.get("tool_use") is not None:
                    parts.append((w_tool_use, float(lb["tool_use"])))
                if lb.get("general_chat") is not None:
                    parts.append((w_chat, float(lb["general_chat"])))

                if parts:
                    denom = sum(w for w, _ in parts) or 1.0
                    entry["score"] = sum(w * s for w, s in parts) / denom
                    entry["score_source"] = f"leaderboard:{leaderboard_dataset}"

        # Fallback: HF model card model-index benchmarks.
        if entry["score"] is None and hf:
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
        "leaderboard": {
            "dataset": leaderboard_dataset,
            "config": leaderboard_config,
            "split": leaderboard_split,
            "rows_loaded": len(leaderboard_rows),
            "error": leaderboard_err,
            "metrics": {
                "coding": coding_metric,
                "tool_use": tool_use_metric,
                "general_chat": chat_metric,
            },
            "weights": {
                "coding": w_coding,
                "tool_use": w_tool_use,
                "general_chat": w_chat,
            },
        },
        "recommendation": best,
        "candidates": scored,
        "notes": [
            "Selection ignores likes/downloads.",
            "If a model matches the configured leaderboard dataset, that benchmark score overrides HF model-index.",
            "To get leaderboard matches for local Ollama tags, map them to HF IDs via --candidates (local=org/name).",
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
        "--leaderboard-dataset",
        default=os.environ.get("TASKSPINE_LEADERBOARD_DATASET", DEFAULT_LEADERBOARD_DATASET),
        help="HF dataset ID providing benchmark scores (overrides HF model-index when matched).",
    )
    suggest.add_argument(
        "--leaderboard-config",
        default=os.environ.get("TASKSPINE_LEADERBOARD_CONFIG", DEFAULT_LEADERBOARD_CONFIG),
        help="HF dataset config/subset name.",
    )
    suggest.add_argument(
        "--leaderboard-split",
        default=os.environ.get("TASKSPINE_LEADERBOARD_SPLIT", DEFAULT_LEADERBOARD_SPLIT),
        help="HF dataset split name.",
    )
    suggest.add_argument(
        "--coding-metric",
        default=os.environ.get("TASKSPINE_CODING_METRIC", DEFAULT_CODING_METRIC),
        help="Column name for coding score.",
    )
    suggest.add_argument(
        "--tool-use-metric",
        default=os.environ.get("TASKSPINE_TOOL_USE_METRIC", DEFAULT_TOOL_USE_METRIC),
        help="Column name for tool-use score.",
    )
    suggest.add_argument(
        "--chat-metric",
        default=os.environ.get("TASKSPINE_CHAT_METRIC", DEFAULT_CHAT_METRIC),
        help="Column name for general chat score.",
    )
    suggest.add_argument("--w-coding", type=float, default=1.0, help="Weight for coding metric.")
    suggest.add_argument("--w-tool-use", type=float, default=1.0, help="Weight for tool-use metric.")
    suggest.add_argument("--w-chat", type=float, default=1.0, help="Weight for general chat metric.")
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
        result = suggest_low_tier_models(
            system=system,
            candidates=candidates,
            hf_token=hf_token,
            leaderboard_dataset=args.leaderboard_dataset,
            leaderboard_config=args.leaderboard_config,
            leaderboard_split=args.leaderboard_split,
            coding_metric=args.coding_metric,
            tool_use_metric=args.tool_use_metric,
            chat_metric=args.chat_metric,
            w_coding=float(args.w_coding),
            w_tool_use=float(args.w_tool_use),
            w_chat=float(args.w_chat),
        )
        print(json.dumps(result, indent=2, sort_keys=True))
        return

    raise SystemExit("Unknown taskspine subcommand")


def register(ctx) -> None:
    ctx.register_cli_command(
        name="taskspine",
        help="Taskspine utilities (model routing helpers, webhook docs, etc.)",
        description=(
            "Local model suggestion is benchmark-first: leaderboard dataset override first, "
            "then HF model-index fallback — never likes/downloads."
        ),
        setup_fn=_setup_taskspine_cmd,
        handler_fn=_handle_taskspine_cmd,
    )
