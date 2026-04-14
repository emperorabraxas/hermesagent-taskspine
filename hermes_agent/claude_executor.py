from __future__ import annotations

import shlex
import subprocess
from dataclasses import dataclass
from pathlib import Path


@dataclass
class ClaudeRun:
    command: list[str]
    prompt_path: Path


def build_claude_command(
    *,
    claude_bin: str,
    repo_path: Path,
    prompt_path: Path,
    permission_mode: str = "acceptEdits",
    model: str = "",
) -> ClaudeRun:
    cmd = [claude_bin, "-p", "--add-dir", str(repo_path), "--permission-mode", permission_mode]
    if model:
        cmd += ["--model", model]
    cmd += [prompt_path.read_text()]
    return ClaudeRun(command=cmd, prompt_path=prompt_path)


def run_claude(command: list[str]) -> int:
    p = subprocess.run(command)
    return int(p.returncode)

