"""System Profiler — spiders crawl the machine on first launch.

Detects hardware, OS, installed tools, and capabilities.
Saved to data/system_profile.json so spiders know exactly what
machine they're running on. Re-crawls if profile is stale (>24h).
"""
from __future__ import annotations

import json
import logging
import os
import platform
import shutil
import subprocess
import time
from datetime import datetime
from pathlib import Path

logger = logging.getLogger(__name__)

DATA_DIR = Path(__file__).parent.parent.parent.parent / "data"
PROFILE_FILE = DATA_DIR / "system_profile.json"
STALE_HOURS = 24


def _run(cmd: str, timeout: int = 5) -> str:
    """Run a command and return stdout. Uses shlex to avoid shell=True."""
    import shlex
    try:
        # Split into args list — no shell injection possible
        args = shlex.split(cmd)
        r = subprocess.run(args, capture_output=True, text=True, timeout=timeout)
        return r.stdout.strip()
    except Exception:
        # Fallback for piped commands — read files directly in Python instead
        return ""


def _read_file(path: str, default: str = "") -> str:
    """Read a file directly — faster and safer than subprocess."""
    try:
        with open(path, "r") as f:
            return f.read().strip()
    except Exception:
        return default


def _detect_cpu() -> dict:
    """Detect CPU info."""
    info = {"model": "", "cores": os.cpu_count() or 0, "threads": 0, "arch": platform.machine()}

    # Try lscpu first (Linux)
    lscpu = _run("lscpu")
    if lscpu:
        for line in lscpu.split("\n"):
            if "Model name:" in line:
                info["model"] = line.split(":", 1)[1].strip()
            elif "Thread(s) per core:" in line:
                try:
                    tpc = int(line.split(":", 1)[1].strip())
                    cores = info["cores"] or 1
                    info["threads"] = cores * tpc
                except ValueError:
                    pass
            elif "CPU(s):" == line[:7]:
                try:
                    info["threads"] = int(line.split(":", 1)[1].strip())
                except ValueError:
                    pass

    if not info["model"]:
        cpuinfo = _read_file("/proc/cpuinfo")
        for line in cpuinfo.split("\n"):
            if "model name" in line:
                info["model"] = line.split(":", 1)[1].strip()
                break

    return info


def _detect_gpu() -> dict:
    """Detect GPU info."""
    info = {"model": "", "vram_mb": 0, "driver": "", "type": "none"}

    # AMD (ROCm)
    rocm = _run("rocm-smi --showproductname 2>/dev/null")
    if rocm and "GPU" in rocm:
        info["type"] = "amd"
        info["model"] = rocm.split("\n")[-1].strip() if rocm else ""
        vram = _run("rocm-smi --showmeminfo vram 2>/dev/null | grep 'Total' | head -1")
        if vram:
            try:
                info["vram_mb"] = int(int(vram.split()[-2]) / 1048576)
            except (ValueError, IndexError):
                pass
        info["driver"] = _run("rocm-smi --showdriverversion 2>/dev/null | tail -1").strip()

    # NVIDIA
    if info["type"] == "none":
        nvidia = _run("nvidia-smi --query-gpu=name,memory.total,driver_version --format=csv,noheader 2>/dev/null")
        if nvidia:
            parts = nvidia.split(",")
            info["type"] = "nvidia"
            info["model"] = parts[0].strip() if parts else ""
            if len(parts) > 1:
                try:
                    info["vram_mb"] = int(parts[1].strip().replace(" MiB", ""))
                except ValueError:
                    pass
            if len(parts) > 2:
                info["driver"] = parts[2].strip()

    # Fallback — lspci (get discrete GPU first, then integrated)
    if info["type"] == "none":
        lspci_lines = _run("lspci | grep -i 'vga\\|3d\\|display' 2>/dev/null").split("\n")
        for line in lspci_lines:
            if not line.strip():
                continue
            # Extract the human-readable name from brackets
            import re as _re
            bracket_match = _re.findall(r'\[([^\]]+)\]', line)
            if bracket_match:
                # First bracket is manufacturer, second is product
                gpu_name = bracket_match[-1] if len(bracket_match) > 1 else bracket_match[0]
            else:
                gpu_name = line.split(":", 2)[-1].strip()

            # Detect type from this line
            if "AMD" in line or "Radeon" in line:
                info["type"] = "amd"
            elif "NVIDIA" in line:
                info["type"] = "nvidia"
            elif "Intel" in line:
                info["type"] = "intel"

            # Prefer discrete GPU (Navi, GeForce, RTX, RX)
            if any(x in line for x in ["Navi", "GeForce", "RTX", "RX 7", "RX 6", "Radeon RX"]):
                info["model"] = gpu_name
                break
            elif not info["model"]:
                info["model"] = gpu_name

    # Get VRAM from sysfs (AMD) — take the largest (discrete GPU)
    if info["type"] == "amd" and not info["vram_mb"]:
        vram_lines = _run("cat /sys/class/drm/card*/device/mem_info_vram_total 2>/dev/null")
        if vram_lines:
            try:
                vram_values = [int(v) for v in vram_lines.strip().split("\n") if v.strip().isdigit()]
                if vram_values:
                    info["vram_mb"] = int(max(vram_values) / 1048576)
            except ValueError:
                pass

    # NVIDIA VRAM fallback
    if info["type"] == "nvidia" and not info["vram_mb"]:
        nvidia_mem = _run("nvidia-smi --query-gpu=memory.total --format=csv,noheader 2>/dev/null | head -1")
        if nvidia_mem:
            try:
                info["vram_mb"] = int(nvidia_mem.replace("MiB", "").strip())
            except ValueError:
                pass

    return info


def _detect_memory() -> dict:
    """Detect RAM info."""
    info = {"total_mb": 0, "swap_mb": 0, "swap_enabled": False}

    meminfo = _run("free -m | head -3")
    if meminfo:
        lines = meminfo.strip().split("\n")
        for line in lines:
            parts = line.split()
            if parts and parts[0] == "Mem:":
                try:
                    info["total_mb"] = int(parts[1])
                except (ValueError, IndexError):
                    pass
            elif parts and parts[0] == "Swap:":
                try:
                    info["swap_mb"] = int(parts[1])
                    info["swap_enabled"] = info["swap_mb"] > 0
                except (ValueError, IndexError):
                    pass

    return info


def _detect_disk() -> dict:
    """Detect disk info."""
    info = {"total_gb": 0, "used_gb": 0, "free_gb": 0, "filesystem": ""}

    df = _run("df -BG / | tail -1")
    if df:
        parts = df.split()
        try:
            info["filesystem"] = parts[0]
            info["total_gb"] = int(parts[1].replace("G", ""))
            info["used_gb"] = int(parts[2].replace("G", ""))
            info["free_gb"] = int(parts[3].replace("G", ""))
        except (ValueError, IndexError):
            pass

    return info


def _detect_os() -> dict:
    """Detect OS info."""
    info = {
        "name": "",
        "version": "",
        "kernel": platform.release(),
        "distro": "",
        "package_manager": "",
        "shell": os.environ.get("SHELL", ""),
        "display_server": "",
        "desktop": os.environ.get("XDG_CURRENT_DESKTOP", ""),
        "hostname": platform.node(),
        "user": os.environ.get("USER", ""),
    }

    # Distro
    os_release = _run("cat /etc/os-release 2>/dev/null")
    if os_release:
        for line in os_release.split("\n"):
            if line.startswith("PRETTY_NAME="):
                info["distro"] = line.split("=", 1)[1].strip('"')
            elif line.startswith("ID="):
                info["name"] = line.split("=", 1)[1].strip('"')
            elif line.startswith("VERSION_ID="):
                info["version"] = line.split("=", 1)[1].strip('"')

    # Package manager
    for pm in ["pacman", "apt", "dnf", "yum", "zypper", "apk", "brew", "nix"]:
        if shutil.which(pm):
            info["package_manager"] = pm
            break

    # Display server
    if os.environ.get("WAYLAND_DISPLAY"):
        info["display_server"] = "wayland"
    elif os.environ.get("DISPLAY"):
        info["display_server"] = "x11"

    return info


def _detect_tools() -> dict:
    """Detect installed development tools and runtimes."""
    tools = {}
    checks = {
        "python": "python3 --version",
        "node": "node --version",
        "npm": "npm --version",
        "rust": "rustc --version",
        "go": "go version",
        "java": "java --version 2>&1 | head -1",
        "docker": "docker --version",
        "git": "git --version",
        "ollama": "ollama --version 2>/dev/null",
        "gcc": "gcc --version | head -1",
        "make": "make --version | head -1",
        "cargo": "cargo --version",
        "pip": "pip --version",
        "godot": "godot --version 2>/dev/null || echo ''",
        "dotnet": "dotnet --version 2>/dev/null || echo ''",
        # CLI tools for data wrangling & inspection
        "jq": "jq --version",
        "yq": "yq --version",
        "httpie": "http --version",
        "ripgrep": "rg --version | head -1",
        "fd": "fd --version",
        "bat": "bat --version | head -1",
        "tokei": "tokei --version",
        "pgcli": "pgcli --version",
        "redis-cli": "redis-cli --version",
        "fzf": "fzf --version | head -1",
        "lazygit": "lazygit --version | head -1",
        "delta": "delta --version",
    }

    for name, cmd in checks.items():
        ver = _run(cmd)
        if ver:
            tools[name] = ver.split("\n")[0][:80]

    return tools


def _detect_ollama_models() -> list:
    """Detect installed Ollama models."""
    raw = _run("ollama list 2>/dev/null")
    if not raw:
        return []
    models = []
    for line in raw.split("\n")[1:]:  # skip header
        parts = line.split()
        if parts:
            models.append({"name": parts[0], "size": parts[2] + " " + parts[3] if len(parts) > 3 else "?"})
    return models


def crawl_system() -> dict:
    """Full system crawl — run on first launch."""
    logger.info("Crawling system hardware and OS...")

    profile = {
        "crawled_at": datetime.now().isoformat(),
        "cpu": _detect_cpu(),
        "gpu": _detect_gpu(),
        "memory": _detect_memory(),
        "disk": _detect_disk(),
        "os": _detect_os(),
        "tools": _detect_tools(),
        "ollama_models": _detect_ollama_models(),
    }

    DATA_DIR.mkdir(parents=True, exist_ok=True)
    PROFILE_FILE.write_text(json.dumps(profile, indent=2))
    logger.info("System profile saved to %s", PROFILE_FILE)

    return profile


def load_profile() -> dict | None:
    """Load cached profile, or None if stale/missing."""
    if not PROFILE_FILE.exists():
        return None
    try:
        profile = json.loads(PROFILE_FILE.read_text())
        # Check staleness
        crawled = profile.get("crawled_at", "")
        if crawled:
            from datetime import datetime as dt
            age = (dt.now() - dt.fromisoformat(crawled)).total_seconds()
            if age > STALE_HOURS * 3600:
                logger.info("System profile stale (%dh old), re-crawling", int(age / 3600))
                return None
        return profile
    except Exception:
        return None


def ensure_profile() -> dict:
    """Load or create the system profile."""
    profile = load_profile()
    if profile is None:
        profile = crawl_system()
    return profile


def get_system_context() -> str:
    """Generate a human-readable system summary for spider system prompts."""
    p = ensure_profile()

    cpu = p.get("cpu", {})
    gpu = p.get("gpu", {})
    mem = p.get("memory", {})
    disk = p.get("disk", {})
    osinfo = p.get("os", {})

    vram_gb = gpu.get("vram_mb", 0) / 1024
    vram = f"{vram_gb:.0f}GB VRAM" if vram_gb > 0 else "? VRAM"
    ram_gb = mem.get("total_mb", 0) / 1024
    swap_status = "enabled" if mem.get("swap_enabled") else "DISABLED"

    # Clean GPU model name — just the product name
    gpu_model = gpu.get("model", "none")
    # Extract just the bracket content if present
    if "[" in gpu_model and "]" in gpu_model:
        gpu_model = gpu_model[gpu_model.index("[") + 1:gpu_model.index("]")]

    ctx = (
        f"SYSTEM: {osinfo.get('distro', 'Linux')} (Kernel {osinfo.get('kernel', '?')}) "
        f"| CPU: {cpu.get('model', '?')} ({cpu.get('cores', '?')}C/{cpu.get('threads', '?')}T) "
        f"| GPU: {gpu_model} ({gpu.get('type', '?')}, {vram}) "
        f"| RAM: {ram_gb:.0f}GB (Swap: {swap_status}) "
        f"| Disk: {disk.get('free_gb', '?')}GB free / {disk.get('total_gb', '?')}GB "
        f"| {osinfo.get('package_manager', '?')} | {osinfo.get('shell', '?').split('/')[-1]}"
    )
    return ctx
