from __future__ import annotations

import json
import os
import platform
import re
import subprocess
import time
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Tuple


DEFAULT_LEADERBOARD_DATASET = "OpenEvals/leaderboard-data"
DEFAULT_LEADERBOARD_CONFIG = "default"
DEFAULT_LEADERBOARD_SPLIT = "train"

# Metrics in OpenEvals/leaderboard-data.
DEFAULT_CODING_METRIC = "sweVerified_score"
DEFAULT_TOOL_USE_METRIC = "terminalBench_score"
DEFAULT_CHAT_METRIC = "aggregate_score"

_LEADERBOARD_CACHE: Dict[str, Any] = {"ts": 0.0, "rows": None, "err": None}
_OPENAI_MODELS_CACHE: Dict[str, Any] = {"ts": 0.0, "models": None, "err": None}
_CACHE_TTL_SECONDS = 6 * 60 * 60  # 6 hours


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

def _get_leaderboard_index(
    dataset: str,
    config: str,
    split: str,
    hf_token: Optional[str],
) -> Tuple[Dict[str, Dict[str, Any]], Optional[str], int]:
    """Return (index, error, rows_loaded) with caching."""
    now = time.time()
    cache_key = f"{dataset}|{config}|{split}|{bool(hf_token)}"
    cached = _LEADERBOARD_CACHE.get("key") == cache_key and (now - float(_LEADERBOARD_CACHE.get("ts") or 0.0)) < _CACHE_TTL_SECONDS
    if cached and isinstance(_LEADERBOARD_CACHE.get("rows"), list):
        rows = _LEADERBOARD_CACHE["rows"]
        return _index_leaderboard_rows(rows), _LEADERBOARD_CACHE.get("err"), len(rows)

    rows, err = _fetch_hf_dataset_rows(dataset=dataset, config=config, split=split, hf_token=hf_token)
    _LEADERBOARD_CACHE.update({"key": cache_key, "ts": now, "rows": rows, "err": err})
    return _index_leaderboard_rows(rows), err, len(rows)


def _fetch_openai_models(api_key: str, base_url: str = "https://api.openai.com/v1") -> Tuple[Optional[List[Dict[str, Any]]], Optional[str]]:
    """Fetch OpenAI model list (used only to resolve 'latest')."""
    try:
        import requests  # Hermes dependency
    except Exception as e:
        return None, f"requests not available: {e}"

    base = (base_url or "").rstrip("/")
    try:
        resp = requests.get(
            f"{base}/models",
            headers={"Authorization": f"Bearer {api_key}"},
            timeout=8,
        )
        if resp.status_code >= 400:
            return None, f"OpenAI models HTTP {resp.status_code}"
        data = resp.json() or {}
        models = data.get("data")
        if not isinstance(models, list):
            return None, "OpenAI models: unexpected payload"
        return models, None
    except Exception as e:
        return None, str(e)


def resolve_latest_openai_model(api_key: Optional[str], base_url: str = "https://api.openai.com/v1") -> Tuple[Optional[str], Optional[str]]:
    """Resolve the most recently created GPT-family model id."""
    if not api_key:
        return None, "OPENAI_API_KEY missing"
    now = time.time()
    cache_key = f"{base_url}|{api_key[:6]}"
    cached = _OPENAI_MODELS_CACHE.get("key") == cache_key and (now - float(_OPENAI_MODELS_CACHE.get("ts") or 0.0)) < _CACHE_TTL_SECONDS
    if cached and isinstance(_OPENAI_MODELS_CACHE.get("models"), list):
        models = _OPENAI_MODELS_CACHE["models"]
    else:
        models, err = _fetch_openai_models(api_key=api_key, base_url=base_url)
        _OPENAI_MODELS_CACHE.update({"key": cache_key, "ts": now, "models": models, "err": err})
        if err:
            return None, err
        if not models:
            return None, "OpenAI models empty"

    def is_candidate(mid: str) -> bool:
        m = mid.lower()
        if not (m.startswith("gpt-") or m.startswith("o")):
            return False
        if any(x in m for x in ("whisper", "tts", "dall-e", "embedding", "moderation", "realtime", "transcribe", "audio")):
            return False
        return True

    best_id = None
    best_created = -1
    for m in models:
        mid = m.get("id")
        created = m.get("created")
        if not isinstance(mid, str) or not mid.strip():
            continue
        if not is_candidate(mid):
            continue
        try:
            c = int(created) if isinstance(created, (int, float, str)) and str(created).isdigit() else 0
        except Exception:
            c = 0
        if c > best_created:
            best_created = c
            best_id = mid
    if not best_id:
        return None, "No suitable GPT-family model found"
    return best_id, None


def build_taskspine_routing_context() -> str:
    """Return a short routing policy block for injection via pre_llm_call."""
    def classify_task(task: str) -> str:
        t = (task or "").lower()
        # Cheap heuristics: if in doubt, treat as general chat.
        if any(k in t for k in ("bug", "fix", "refactor", "implement", "patch", "pr", "pull request", "repo", "code", "tests", "pytest", "build", "compile")):
            return "coding"
        if any(k in t for k in ("tool", "webhook", "github", "api", "mcp", "terminal", "shell", "command", "aws", "cloudflare", "tunnel", "deploy")):
            return "tool-use"
        return "general chat"

    # Webhook URL is user-controlled; keep it explicit.
    webhook_url = os.environ.get("TASKSPINE_WEBHOOK_PUBLIC_URL", "").strip()

    # Low lane: local Ollama
    low_base_url = os.environ.get("TASKSPINE_LOW_BASE_URL", "http://127.0.0.1:11434/v1").strip()
    hf_token = os.environ.get("HF_TOKEN", "").strip() or None
    dataset = os.environ.get("TASKSPINE_LEADERBOARD_DATASET", DEFAULT_LEADERBOARD_DATASET).strip()
    config = os.environ.get("TASKSPINE_LEADERBOARD_CONFIG", DEFAULT_LEADERBOARD_CONFIG).strip()
    split = os.environ.get("TASKSPINE_LEADERBOARD_SPLIT", DEFAULT_LEADERBOARD_SPLIT).strip()
    coding_metric = os.environ.get("TASKSPINE_CODING_METRIC", DEFAULT_CODING_METRIC).strip()
    tool_metric = os.environ.get("TASKSPINE_TOOL_USE_METRIC", DEFAULT_TOOL_USE_METRIC).strip()
    chat_metric = os.environ.get("TASKSPINE_CHAT_METRIC", DEFAULT_CHAT_METRIC).strip()

    candidates = [{"name": n, "hf": ""} for n in _try_list_ollama_models()]
    system = detect_system_profile()

    lb_index, lb_err, lb_rows = _get_leaderboard_index(dataset, config, split, hf_token)

    user_task = os.environ.get("TASKSPINE_USER_TASK", "").strip()
    # If we're running inside Hermes, user_message is passed via pre_llm_call hook.
    # We fall back to an env var to support CLI debugging.
    task_type = classify_task(user_task) if user_task else "general chat"

    if task_type == "coding":
        w_coding, w_tool, w_chat = 1.0, 0.35, 0.15
    elif task_type == "tool-use":
        w_coding, w_tool, w_chat = 0.35, 1.0, 0.15
    else:
        w_coding, w_tool, w_chat = 0.25, 0.25, 1.0

    low_model = os.environ.get("TASKSPINE_LOW_MODEL", "").strip() or None
    if not low_model and candidates and lb_index:
        # Prefer models that match the leaderboard; otherwise just pick the first installed.
        best_score = None
        best_name = None
        for c in candidates:
            lb, _ = _leaderboard_scores_for_candidate(c, lb_index, coding_metric, tool_metric, chat_metric)
            if not lb:
                continue
            parts: List[Tuple[float, float]] = []
            if lb.get("coding") is not None:
                parts.append((w_coding, float(lb["coding"])))
            if lb.get("tool_use") is not None:
                parts.append((w_tool, float(lb["tool_use"])))
            if lb.get("general_chat") is not None:
                parts.append((w_chat, float(lb["general_chat"])))
            if not parts:
                continue
            denom = sum(w for w, _ in parts) or 1.0
            score = sum(w * s for w, s in parts) / denom
            if best_score is None or score > best_score:
                best_score = score
                best_name = c["name"]
        low_model = best_name or (candidates[0]["name"] if candidates else None)
    if not low_model and candidates:
        low_model = candidates[0]["name"]

    # Mid lane: OpenAI latest
    openai_base = os.environ.get("TASKSPINE_MID_OPENAI_BASE_URL", "https://api.openai.com/v1").strip()
    openai_key = os.environ.get("OPENAI_API_KEY", "").strip() or None
    mid_model = os.environ.get("TASKSPINE_MID_OPENAI_MODEL", "latest").strip()
    if mid_model.lower() == "latest":
        resolved, _err = resolve_latest_openai_model(openai_key, base_url=openai_base)
        if resolved:
            mid_model = resolved

    # High lane: Claude Code (ACP) using Opus 4.6
    high_acp_cmd = os.environ.get("TASKSPINE_HIGH_ACP_COMMAND", "claude").strip()
    high_model = os.environ.get("TASKSPINE_HIGH_MODEL", "claude-opus-4-6").strip()
    high_acp_args = os.environ.get("TASKSPINE_HIGH_ACP_ARGS", "").strip()
    if high_acp_args:
        # Split on whitespace (simple), user can override precisely if needed.
        acp_args = high_acp_args.split()
    else:
        acp_args = ["--acp", "--stdio", "--model", high_model]

    lines: List[str] = []
    lines.append("[TASKSPINE ROUTING]")
    lines.append(f"- System: CPU-only, ~{system.mem_total_gib:.1f} GiB RAM.")
    if webhook_url:
        lines.append(f"- GitHub webhook URL (public HTTPS): {webhook_url}")
    lines.append(f"- Task type heuristic: {task_type} (weights: coding={w_coding}, tool-use={w_tool}, chat={w_chat}).")
    lines.append("- Low lane (local): use delegate_task with base_url/model for cheap drafting.")
    if low_model:
        lines.append(f"  - base_url={low_base_url} model={low_model} (leaderboard={dataset})")
    else:
        lines.append(f"  - base_url={low_base_url} model=<set TASKSPINE_LOW_MODEL> (leaderboard={dataset})")
    if lb_err:
        lines.append(f"  - leaderboard note: {lb_err} (rows_loaded={lb_rows})")
    lines.append("- Mid lane (plan/review): OpenAI + latest model id (resolve via /models).")
    lines.append(f"  - base_url={openai_base} model={mid_model}")
    lines.append("- High lane (execute): Claude Code via ACP on Opus 4.6 (1M ctx).")
    lines.append(f"  - delegate_task(acp_command={high_acp_cmd}, acp_args={acp_args})")
    lines.append("- Rules: benchmark-first for low model; never likes/downloads.")
    lines.append("- Suggested flow: low lane drafts → mid lane reviews (toolsets=['read_only','web']) → high lane executes (ACP).")

    return "\n".join(lines)


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

    latest = models_sub.add_parser("openai-latest", help="Resolve the latest OpenAI model id via /models")
    latest.add_argument(
        "--openai-base-url",
        default=os.environ.get("TASKSPINE_MID_OPENAI_BASE_URL", "https://api.openai.com/v1"),
        help="OpenAI API base URL (default: https://api.openai.com/v1).",
    )
    latest.add_argument(
        "--openai-token-env",
        default="OPENAI_API_KEY",
        help="Env var name containing OpenAI API key.",
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

    if args.taskspine_cmd == "models" and args.models_cmd == "openai-latest":
        key = os.environ.get(args.openai_token_env, "").strip() or None
        model_id, err = resolve_latest_openai_model(key, base_url=str(args.openai_base_url))
        print(json.dumps({"model": model_id, "error": err, "base_url": args.openai_base_url}, indent=2, sort_keys=True))
        return

    raise SystemExit("Unknown taskspine subcommand")


def register(ctx) -> None:
    def _pre_llm_call_hook(**kwargs):
        # Keep this short; any heavy lifting is cached.
        try:
            user_message = kwargs.get("user_message")
            if isinstance(user_message, str) and user_message.strip():
                # Used by build_taskspine_routing_context() classifier.
                os.environ["TASKSPINE_USER_TASK"] = user_message.strip()
            return {"context": build_taskspine_routing_context()}
        except Exception as e:
            return {"context": f"[TASKSPINE ROUTING] (hook error: {e})"}

    ctx.register_hook("pre_llm_call", _pre_llm_call_hook)
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
