from __future__ import annotations

import subprocess
from pathlib import Path


def resolve_repo_root(cwd: Path) -> Path:
    try:
        out = subprocess.check_output(["git", "rev-parse", "--show-toplevel"], cwd=str(cwd), text=True).strip()
        if out:
            return Path(out)
    except Exception:
        pass
    return cwd


def summarize_repo(repo_root: Path) -> str:
    """
    Keep this intentionally light: we don't want to slurp the whole repo into a paid prompt.
    """
    parts = []
    parts.append(f"repo_root: {repo_root}\n")
    try:
        status = subprocess.check_output(["git", "status", "--porcelain=v1"], cwd=str(repo_root), text=True).strip()
        parts.append("git_dirty: " + ("yes" if status else "no") + "\n")
    except Exception:
        parts.append("git_status: unavailable\n")
    try:
        ls = subprocess.check_output(["git", "ls-files"], cwd=str(repo_root), text=True)
        parts.append(f"tracked_files: {len(ls.splitlines())}\n")
    except Exception:
        parts.append("tracked_files: unknown\n")
    return "".join(parts)

