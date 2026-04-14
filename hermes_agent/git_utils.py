from __future__ import annotations

import subprocess
from pathlib import Path


def _run(cmd: list[str], *, cwd: Path) -> str:
    p = subprocess.run(cmd, cwd=str(cwd), capture_output=True, text=True)
    if p.returncode != 0:
        raise RuntimeError((p.stderr or p.stdout or "").strip() or f"Command failed: {' '.join(cmd)}")
    return (p.stdout or "").strip()


def set_origin_remote(*, repo_path: Path, remote_url: str) -> None:
    repo_path = repo_path.expanduser().resolve()
    _run(["git", "rev-parse", "--is-inside-work-tree"], cwd=repo_path)

    # Remove origin if exists; ignore errors.
    subprocess.run(["git", "remote", "remove", "origin"], cwd=str(repo_path), capture_output=True, text=True)
    _run(["git", "remote", "add", "origin", remote_url], cwd=repo_path)

