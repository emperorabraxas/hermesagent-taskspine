from __future__ import annotations

import httpx


def is_ollama_reachable(base_url: str, timeout_sec: float = 1.2) -> bool:
    try:
        r = httpx.get(f"{base_url.rstrip('/')}/api/tags", timeout=timeout_sec)
        return r.status_code == 200
    except Exception:
        return False


def run_local_ideation(*, base_url: str, model: str, task: str) -> str:
    """
    Best-effort local ideation step. This is intentionally short and non-executing.
    """
    prompt = (
        "You are the low-tier ideation model. Produce:\n"
        "1) a concise idea/workflow\n"
        "2) 3-7 clarifying questions (only if needed)\n"
        "Do NOT propose code edits; do NOT claim you executed anything.\n\n"
        f"Task: {task}"
    )
    payload = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "stream": False,
        "keep_alive": "2m",
        "options": {"temperature": 0.4, "num_ctx": 4096},
    }
    r = httpx.post(f"{base_url.rstrip('/')}/api/chat", json=payload, timeout=60)
    r.raise_for_status()
    data = r.json()
    msg = data.get("message") or {}
    return (msg.get("content") or "").strip()

