"""Shell execution for agents — shared persistent bash session.

All spiders share one bash process. cd persists, environment builds up.
Like a shared terminal that all agents type into sequentially.
"""
from __future__ import annotations

import asyncio
import logging
import os
import re
import uuid
from dataclasses import dataclass

logger = logging.getLogger(__name__)

TIMEOUT = 120  # 2 minutes — agents do real work
MAX_OUTPUT = 50_000  # 50KB


@dataclass
class ExecResult:
    command: str
    stdout: str
    stderr: str
    returncode: int
    timed_out: bool = False


class PersistentShell:
    """A single long-running bash process shared by all spiders.

    Commands run sequentially through the same shell. cd persists,
    environment variables persist, aliases persist — like a real terminal.
    Uses a sentinel pattern to detect when each command finishes.
    """

    def __init__(self):
        self._proc: asyncio.subprocess.Process | None = None
        self._lock = asyncio.Lock()
        self._started = False

    async def _ensure_started(self):
        """Start the bash process if not already running."""
        if self._proc is not None and self._proc.returncode is None:
            # Check if streams are still usable (event loop may have changed)
            try:
                if self._proc.stdin and not self._proc.stdin.is_closing():
                    return  # still alive and usable
            except Exception:
                pass
            # Streams broken — kill and restart
            try:
                self._proc.kill()
                await self._proc.wait()
            except Exception:
                pass
            self._proc = None

        env = os.environ.copy()
        env["PS1"] = ""  # disable prompt to avoid noise

        self._proc = await asyncio.create_subprocess_exec(
            "bash", "--norc", "--noprofile",
            stdin=asyncio.subprocess.PIPE,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            env=env,
            cwd=os.path.expanduser("~"),
        )
        self._started = True
        logger.info("Persistent shell started (PID %s)", self._proc.pid)

    # Compiled regex blocklist — case-insensitive
    BLOCKED_PATTERNS = [
        # Destructive filesystem
        re.compile(r"rm\s+(-[rf]+\s+)?/($|[*\s])", re.I),
        re.compile(r"dd\s+if=", re.I),
        re.compile(r"mkfs\.", re.I),
        re.compile(r">\s*/dev/sd", re.I),
        re.compile(r":\(\)\s*\{.*\}", re.I),  # fork bomb
        re.compile(r"chmod\s+-R\s+0{3}\s+/", re.I),
        re.compile(r"chown\s+-R\s+.*\s+/($|\s)", re.I),
        # Code execution / eval
        re.compile(r"\beval\b", re.I),
        re.compile(r"\bexec\b", re.I),
        re.compile(r"python[23]?\s+-c\s", re.I),
        re.compile(r"perl\s+-e\s", re.I),
        re.compile(r"ruby\s+-e\s", re.I),
        # Network exfiltration
        re.compile(r"curl\b.*\|\s*(ba)?sh", re.I),
        re.compile(r"wget\b.*\|\s*(ba)?sh", re.I),
        re.compile(r"nc\s+(-[elp]+\s+)?", re.I),
        re.compile(r"\bncat\b", re.I),
        # Reverse shells
        re.compile(r"bash\s+-i\s+", re.I),
        re.compile(r"/dev/tcp/", re.I),
        # Service disruption
        re.compile(r"\breboot\b", re.I),
        re.compile(r"\bpoweroff\b", re.I),
        re.compile(r"\bshutdown\b", re.I),
        re.compile(r"iptables\s+-F", re.I),
        re.compile(r"systemctl\s+(stop|disable)\s+(sshd|NetworkManager|docker)", re.I),
    ]

    # Allowlisted python -c patterns — TIGHT: only known-safe imports
    ALLOWED_PYTHON_PATTERNS = [
        re.compile(r"python3?\s+-c\s+\"from\s+agentic_hub\.core\.portfolio\s+import\s+log_trade", re.I),
        re.compile(r"python3?\s+-c\s+\"from\s+agentic_hub\.core\.trading\.", re.I),
    ]

    def _is_dangerous(self, command: str) -> str | None:
        """Check for commands that could damage the system. Regex-based, case-insensitive."""
        # Check allowlist first
        for allow in self.ALLOWED_PYTHON_PATTERNS:
            if allow.search(command):
                return None
        for pattern in self.BLOCKED_PATTERNS:
            if pattern.search(command):
                return f"Blocked: matches '{pattern.pattern}'"
        return None

    async def execute(
        self,
        command: str,
        timeout: int = TIMEOUT,
        max_output: int = MAX_OUTPUT,
    ) -> ExecResult:
        """Run a command in the persistent shell.

        Safety: commands run sequentially (locked), dangerous patterns blocked,
        and each command saves/restores the working directory so spiders
        don't accidentally leave each other in weird locations.
        """
        # Pre-check for system-destroying commands
        danger = self._is_dangerous(command)
        if danger:
            return ExecResult(command=command, stdout="", stderr=f"⛔ {danger}", returncode=-1)

        async with self._lock:
            try:
                await self._ensure_started()
            except Exception as e:
                return ExecResult(command=command, stdout="", stderr=f"Shell start failed: {e}", returncode=-1)

            if self._proc is None or self._proc.stdin is None:
                return ExecResult(command=command, stdout="", stderr="Shell not available", returncode=-1)

            # Sentinel — unique marker to detect end of output
            sentinel = f"__SPIDER_DONE_{uuid.uuid4().hex[:12]}__"

            # Write command + sentinel echo
            # We capture the exit code, then echo the sentinel with the code
            cmd_block = (
                f"{command}\n"
                f"__spider_rc=$?\n"
                f"echo \"{sentinel} $__spider_rc\"\n"
                f"echo \"{sentinel}\" >&2\n"
            )

            try:
                self._proc.stdin.write(cmd_block.encode())
                await self._proc.stdin.drain()
            except Exception as e:
                # Shell died — restart on next call
                self._proc = None
                return ExecResult(command=command, stdout="", stderr=f"Shell write failed: {e}", returncode=-1)

            # Read stdout until sentinel
            stdout_parts = []
            stderr_parts = []
            returncode = 0
            timed_out = False

            try:
                stdout_task = self._read_until_sentinel(self._proc.stdout, sentinel, max_output)
                stderr_task = self._read_until_sentinel(self._proc.stderr, sentinel, max_output)

                done, pending = await asyncio.wait(
                    [asyncio.create_task(stdout_task), asyncio.create_task(stderr_task)],
                    timeout=timeout,
                )

                if pending:
                    # Timeout — cancel pending reads but DON'T kill the shell
                    for task in pending:
                        task.cancel()
                    timed_out = True

                for task in done:
                    try:
                        result = task.result()
                        if result is not None:
                            # Check if this is stdout (has returncode) or stderr
                            if isinstance(result, tuple):
                                stdout_text, rc = result
                                stdout_parts.append(stdout_text)
                                returncode = rc
                            else:
                                stderr_parts.append(result)
                    except Exception:
                        pass

            except Exception as e:
                return ExecResult(command=command, stdout="", stderr=str(e), returncode=-1)

            stdout_str = "".join(stdout_parts)[:max_output]
            stderr_str = "".join(stderr_parts)[:max_output]

            if timed_out:
                stderr_str = f"Timed out after {timeout}s (shell still alive)\n" + stderr_str

            result = ExecResult(
                command=command,
                stdout=stdout_str,
                stderr=stderr_str,
                returncode=returncode,
                timed_out=timed_out,
            )
            # Audit log — every command recorded
            self._audit_log(command, result)
            return result

    async def _read_until_sentinel(
        self, stream, sentinel: str, max_output: int
    ) -> tuple[str, int] | str:
        """Read from stream until sentinel line appears."""
        lines = []
        total_bytes = 0

        while True:
            try:
                line = await asyncio.wait_for(stream.readline(), timeout=1.0)
            except asyncio.TimeoutError:
                continue
            except Exception:
                break

            if not line:
                break

            decoded = line.decode("utf-8", errors="replace")

            if sentinel in decoded:
                # Extract returncode from stdout sentinel
                parts = decoded.strip().split()
                if len(parts) >= 2:
                    try:
                        rc = int(parts[-1])
                        return "".join(lines), rc
                    except ValueError:
                        pass
                return "".join(lines), 0 if stream == self._proc.stdout else "".join(lines)

            total_bytes += len(decoded)
            if total_bytes <= max_output:
                lines.append(decoded)
            elif not lines or not lines[-1].endswith("(truncated)\n"):
                lines.append(f"... (truncated at {max_output} bytes)\n")

        return ("".join(lines), 0) if isinstance(lines, list) else "".join(lines)

    def _audit_log(self, command: str, result: ExecResult):
        """Append command to audit log."""
        from datetime import datetime
        from pathlib import Path
        audit_dir = Path(__file__).parent.parent.parent.parent / "data"
        audit_dir.mkdir(parents=True, exist_ok=True)
        audit_file = audit_dir / "audit.log"
        try:
            ts = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
            status = "TIMEOUT" if result.timed_out else f"rc:{result.returncode}"
            line = f"{ts} | {status} | {command}\n"
            with open(audit_file, "a") as f:
                f.write(line)
            # Rotate at 10MB
            if audit_file.stat().st_size > 10_000_000:
                rotated = audit_dir / "audit.log.1"
                if rotated.exists():
                    rotated.unlink()
                audit_file.rename(rotated)
        except Exception:
            pass

    async def get_cwd(self) -> str:
        """Get the current working directory of the shell."""
        result = await self.execute("pwd", timeout=5)
        return result.stdout.strip() if result.stdout else "~"

    def is_alive(self) -> bool:
        """Check if the shell process is still running."""
        return self._proc is not None and self._proc.returncode is None

    async def close(self):
        """Kill the persistent shell."""
        if self._proc and self._proc.returncode is None:
            self._proc.terminate()
            try:
                await asyncio.wait_for(self._proc.wait(), timeout=5)
            except asyncio.TimeoutError:
                self._proc.kill()
            logger.info("Persistent shell closed")
        self._proc = None


# Singleton — shared by all spiders
_shell: PersistentShell | None = None


def get_shell() -> PersistentShell:
    """Get the shared persistent shell instance."""
    global _shell
    if _shell is None:
        _shell = PersistentShell()
    return _shell


async def execute(
    command: str,
    cwd: str | None = None,
    timeout: int = TIMEOUT,
    max_output: int = MAX_OUTPUT,
) -> ExecResult:
    """Execute a command in the shared persistent shell.

    For backwards compatibility — same interface as before.
    If cwd is specified, we cd there first (and it persists).
    """
    shell = get_shell()
    if cwd:
        cd_result = await shell.execute(f"cd {cwd}", timeout=5)
        if cd_result.returncode != 0:
            return ExecResult(command=command, stdout="", stderr=f"cd failed: {cd_result.stderr}", returncode=-1)
    return await shell.execute(command, timeout=timeout, max_output=max_output)


def _validate_path(path: str) -> str | None:
    """Validate a file path is within allowed directories. Returns error or None."""
    from pathlib import Path
    ALLOWED_ROOTS = [Path.home() / d for d in [
        "spider.Web", "project", "uwm-integration", "salesforce-backup",
        "archive_sentinel_anime", "ai-dotfiles", "test", "Solution1",
    ]]
    BLOCKED_PREFIXES = ["/etc/", "/proc/", "/dev/", "/sys/", "/boot/", "/root/"]
    resolved = Path(path).resolve()
    # Block sensitive system paths
    for prefix in BLOCKED_PREFIXES:
        if str(resolved).startswith(prefix):
            return f"Access denied: {prefix} is blocked"
    # Must be within allowed roots or /tmp
    if str(resolved).startswith("/tmp"):
        return None
    if not any(resolved.is_relative_to(r) for r in ALLOWED_ROOTS if r.exists()):
        return f"Access denied: {path} is outside allowed directories"
    # Block symlinks that escape
    if Path(path).is_symlink():
        target = Path(path).resolve()
        if not any(target.is_relative_to(r) for r in ALLOWED_ROOTS if r.exists()):
            return f"Access denied: symlink escapes allowed directory"
    return None


async def read_file(path: str) -> str:
    """Read a file — path-restricted to project directories."""
    err = _validate_path(path)
    if err:
        return err
    try:
        with open(path, "r", errors="replace") as f:
            return f.read(MAX_OUTPUT)
    except Exception as e:
        return f"Error reading {path}: {e}"


async def write_file(path: str, content: str) -> str:
    """Write content to a file — path-restricted."""
    err = _validate_path(path)
    if err:
        return err
    try:
        with open(path, "w") as f:
            f.write(content)
        return f"Written {len(content)} bytes to {path}"
    except Exception as e:
        return f"Error writing {path}: {e}"


async def list_dir(path: str = ".") -> str:
    """List directory contents."""
    result = await execute(f"ls -la {path}")
    return result.stdout or result.stderr


async def edit_file(path: str, old_text: str, new_text: str, replace_all: bool = False) -> str:
    """Surgical file editing — replace specific text without rewriting the whole file.

    Fails if old_text is not found or appears multiple times (unless replace_all=True).
    """
    err = _validate_path(path)
    if err:
        return err
    try:
        with open(path, "r") as f:
            content = f.read()
    except Exception as e:
        return f"Error reading {path}: {e}"

    count = content.count(old_text)
    if count == 0:
        return f"Error: old_text not found in {path}"
    if count > 1 and not replace_all:
        return f"Error: old_text found {count} times in {path}. Use replace_all=True to replace all, or provide more context to make it unique."

    new_content = content.replace(old_text, new_text) if replace_all else content.replace(old_text, new_text, 1)
    try:
        with open(path, "w") as f:
            f.write(new_content)
        replaced = count if replace_all else 1
        return f"Edited {path}: replaced {replaced} occurrence(s), {len(new_content)} bytes written"
    except Exception as e:
        return f"Error writing {path}: {e}"


async def glob_files(pattern: str, path: str = ".") -> str:
    """Find files matching a glob pattern. Supports ** for recursive."""
    import glob as _glob
    from pathlib import Path

    base = Path(path).resolve()
    err = _validate_path(str(base))
    if err:
        return err

    try:
        matches = sorted(_glob.glob(str(base / pattern), recursive=True))
        # Filter to only files (not dirs) and limit output
        files = [str(Path(m).relative_to(base)) for m in matches if Path(m).is_file()]
        if not files:
            return f"No files matching '{pattern}' in {path}"
        result = "\n".join(files[:200])
        if len(files) > 200:
            result += f"\n... and {len(files) - 200} more"
        return f"{len(files)} files found:\n{result}"
    except Exception as e:
        return f"Glob error: {e}"


async def grep_search(pattern: str, path: str = ".", case_sensitive: bool = True, file_glob: str = "") -> str:
    """Search file contents with regex. Returns file:line:content matches."""
    from pathlib import Path

    base = Path(path).resolve()
    err = _validate_path(str(base))
    if err:
        return err

    # Build grep command — prefer ripgrep if available, fallback to grep
    cmd_parts = ["rg" if _has_rg() else "grep", "-rn"]
    if not case_sensitive:
        cmd_parts.append("-i")
    if file_glob:
        if _has_rg():
            cmd_parts.extend(["--glob", file_glob])
        else:
            cmd_parts.extend(["--include", file_glob])
    cmd_parts.extend(["--", pattern, str(base)])

    import subprocess
    try:
        result = subprocess.run(
            cmd_parts, capture_output=True, text=True, timeout=30,
            cwd=str(base),
        )
        output = result.stdout.strip()
        if not output:
            return f"No matches for '{pattern}' in {path}"
        lines = output.split("\n")
        if len(lines) > 200:
            output = "\n".join(lines[:200]) + f"\n... and {len(lines) - 200} more matches"
        return output
    except subprocess.TimeoutExpired:
        return "Search timed out (30s limit)"
    except Exception as e:
        return f"Search error: {e}"


def _has_rg() -> bool:
    """Check if ripgrep is available."""
    import shutil
    return shutil.which("rg") is not None


async def git_cmd(command: str, args: str = "", cwd: str = "") -> str:
    """Execute git commands with safety checks.

    Allowed: status, diff, add, commit, push, pull, log, branch, checkout, stash, show, remote
    Blocked: force-push, reset --hard, clean -f, branch -D
    """
    import subprocess
    from pathlib import Path

    ALLOWED = {"status", "diff", "add", "commit", "push", "pull", "log", "branch",
               "checkout", "stash", "show", "remote", "fetch", "tag", "rebase", "merge"}
    BLOCKED_PATTERNS = ["--force", "-f push", "reset --hard", "clean -f", "branch -D", "push --force"]

    if command not in ALLOWED:
        return f"Git command '{command}' not allowed. Allowed: {', '.join(sorted(ALLOWED))}"

    full_args = f"{command} {args}".strip()
    for blocked in BLOCKED_PATTERNS:
        if blocked in full_args:
            return f"Blocked: '{blocked}' is a destructive operation"

    work_dir = cwd or str(Path.home() / "spider.Web")
    err = _validate_path(work_dir)
    if err:
        return err

    try:
        result = subprocess.run(
            ["git", command] + (args.split() if args else []),
            capture_output=True, text=True, timeout=30,
            cwd=work_dir,
        )
        output = result.stdout.strip()
        if result.stderr.strip() and result.returncode != 0:
            output += f"\n{result.stderr.strip()}"
        return output or "(no output)"
    except subprocess.TimeoutExpired:
        return "Git command timed out (30s)"
    except Exception as e:
        return f"Git error: {e}"
