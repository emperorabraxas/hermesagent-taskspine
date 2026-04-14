from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path


@dataclass
class SystemProfile:
    cpu_threads: int
    mem_total_bytes: int
    vram_total_bytes: int
    vram_used_bytes: int

    @property
    def mem_total_gb(self) -> float:
        return self.mem_total_bytes / (1024**3)

    @property
    def vram_total_gb(self) -> float:
        return self.vram_total_bytes / (1024**3)

    @property
    def vram_used_gb(self) -> float:
        return self.vram_used_bytes / (1024**3)


def _read_int(path: Path) -> int:
    try:
        return int(path.read_text().strip())
    except Exception:
        return 0


def _detect_threads() -> int:
    try:
        return os.cpu_count() or 1
    except Exception:
        return 1


def _detect_mem_total_bytes() -> int:
    # /proc/meminfo MemTotal is in kB
    try:
        meminfo = Path("/proc/meminfo").read_text().splitlines()
        for line in meminfo:
            if line.startswith("MemTotal:"):
                parts = line.split()
                return int(parts[1]) * 1024
    except Exception:
        pass
    return 0


def _detect_amd_vram_bytes() -> tuple[int, int]:
    # Prefer AMDGPU mem_info files when present.
    total = 0
    used = 0
    base = Path("/sys/class/drm")
    if not base.exists():
        return 0, 0

    totals = []
    useds = []
    for card in sorted(base.glob("card*/device")):
        t = card / "mem_info_vram_total"
        u = card / "mem_info_vram_used"
        if t.exists():
            totals.append(_read_int(t))
        if u.exists():
            useds.append(_read_int(u))

    # Take the largest VRAM device as primary GPU.
    if totals:
        idx = max(range(len(totals)), key=lambda i: totals[i])
        total = totals[idx]
        used = useds[idx] if idx < len(useds) else 0
    return total, used


def get_system_profile() -> SystemProfile:
    total_vram, used_vram = _detect_amd_vram_bytes()
    return SystemProfile(
        cpu_threads=_detect_threads(),
        mem_total_bytes=_detect_mem_total_bytes(),
        vram_total_bytes=total_vram,
        vram_used_bytes=used_vram,
    )

