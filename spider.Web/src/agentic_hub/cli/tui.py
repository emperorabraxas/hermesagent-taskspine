"""Terminal UI — Live animated spider.Web with persistent hub.

The web hub stays at the top with animated spider and live status.
Chat scrolls below. Spiders update in real-time as agents work.
"""
from __future__ import annotations

import asyncio
import sys
import os
import time
import shutil

import httpx
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.layout import Layout
from rich.table import Table

from pathlib import Path
import tempfile

console = Console()
HUB_BASE = "http://localhost:8420"

def _load_auth_headers() -> dict[str, str]:
    """Read auth token from server's token file."""
    token_file = Path(tempfile.gettempdir()) / ".spider-web-token"
    if token_file.exists():
        token = token_file.read_text().strip()
        if token:
            return {"Authorization": f"Bearer {token}"}
    return {}

AUTH_HEADERS = _load_auth_headers()

# Spider animation frames — legs flex between states
SPIDER_FRAMES = [
    '  /\\  .-""-.  /\\\n //\\\\/  ,,,  \\//\\\\\n |/\\| ,;;;;;, |/\\|\n //\\\\\\;-====-;///\\\\\n//  \\/   .   \\/  \\\\',
    '  /\\  .-""-.  /\\\n //\\\\/  >>>  \\//\\\\\n |/\\| ,;***;, |/\\|\n //\\\\\\;-!!!!-;///\\\\\n//  \\/   *   \\/  \\\\',
    '  /\\  .-""-.  /\\\n //\\\\/  <<<  \\//\\\\\n |/\\| ,;@@@;, |/\\|\n //\\\\\\;-~~~~-;///\\\\\n//  \\/   #   \\/  \\\\',
]

MINI_SPIDER = {
    "scholar": "[cyan]🕷 Scraper[/cyan]",
    "oracle": "[purple]🕷 Proxy[/purple]",
    "automator": "[yellow]🕷 Cron[/yellow]",
    "code_team": "[red]🕷 Payload[/red]",
    "cockpit": "[bold red]🕷 Root[/bold red]",
    "money_maker": "[green]🐺 Wolf[/green]",
    "manager": "[bold red]🧠 Router[/bold red]",
    "pipeline": "[yellow]🔗 Pipeline[/yellow]",
    "dag": "[yellow]🕸️ DAG[/yellow]",
    "warroom": "[red]⚔️ Exploit[/red]",
    "lab": "[#ff6b6b]🕷 Zero[/#ff6b6b]",
    "ops": "[red]🕷 Router[/red]",
}

SPIDER_WORKING = {
    "scholar": "🕷 ···scraping···",
    "oracle": "🕷 ···proxying···",
    "automator": "🕷 ···executing···",
    "code_team": "🕷 ···compiling···",
    "money_maker": "🐺 ···hunting···",
    "lab": "🕷 ···testing···",
    "ops": "🕷 ···routing···",
    "cockpit": "🕷 ···routing···",
}

# Room config for the web hub
ROOMS = [
    ("scholar", "DATA MINE", "cyan"),
    ("cockpit", "ROOT NODE", "bold red"),
    ("oracle", "DEEP WEB", "purple"),
    ("code_team", "COMPILER", "green"),
    ("ops", "BACKBONE", "red"),
    ("automator", "BOT NET", "yellow"),
    ("warroom", "DARK ROOM", "yellow"),
    ("money_maker", "THE VAULT", "green"),
    ("lab", "ZERO DAY", "#ff6b6b"),
]


def build_web_hub(spider_status: dict | None = None, vault_mode: bool = False, frame: int = 0) -> str:
    """Build the animated web hub with live spider status."""
    # Determine node colors based on active status
    def node(room_key: str, color: str) -> str:
        if spider_status and room_key in spider_status:
            info = spider_status[room_key]
            if info.get("status") == "working":
                return f"[bold {color}]●[/bold {color}]"
        return f"[dim]●[/dim]"

    # Pulsing center based on frame
    pulse = ["░", "▒", "▓", "█"][frame % 4]
    center_color = "green" if vault_mode else "red"

    n = {r[0]: node(r[0], r[2]) for r in ROOMS}

    border = "yellow" if vault_mode else "red"
    title = "[yellow]THE VAULT[/yellow]" if vault_mode else "[red]spider.Web[/red]"
    subtitle = "🐺 Wolf Mode" if vault_mode else "蜘蛛の巣"

    hub = f"""[{border}]    ┌─────{n['scholar']}─────{n['cockpit']}─────{n['oracle']}─────┐
    │ [dim]DATA[/dim]   [dim]ROOT[/dim]   [dim]DEEP[/dim]  │
    │ [dim]MINE[/dim]   [dim]NODE[/dim]   [dim] WEB[/dim]  │
    ├─────{n['code_team']}─────{n['ops']}─────{n['automator']}─────┤
    │ [dim]COMP[/dim]  [{center_color}]{pulse} {title} {pulse}[/{center_color}] [dim] BOT[/dim]  │
    │ [dim]ILER[/dim]  [dim]  BACKBONE [/dim] [dim] NET[/dim]  │
    ├─────{n['warroom']}─────{n['money_maker']}─────{n['lab']}─────┤
    │ [dim]DARK[/dim]   [dim] THE[/dim]   [dim]ZERO[/dim]  │
    │ [dim]ROOM[/dim]   [dim]VAULT[/dim]  [dim] DAY[/dim]  │
    └──────────────────────────┘
    [dim]       {subtitle}[/dim][/{border}]"""
    return hub


def build_status_bar(stats: dict | None, metrics: dict | None = None) -> str:
    """Build a one-line status bar with operational metrics."""
    if not stats:
        return "[dim]Loading...[/dim]"
    xp = stats.get("total_xp", 0)
    lvl = stats.get("level", 0)
    streak = stats.get("streak", {}).get("current", 0)
    parts = [f"[bold red]Lv {lvl}[/bold red]", f"[white]{xp:,} XP[/white]", f"[yellow]🔥{streak}[/yellow]"]
    if metrics:
        active = metrics.get("agents_active", 0)
        total = metrics.get("agents_total", 9)
        parts.append(f"[cyan]🕷 {active}/{total}[/cyan]")
        uptime = metrics.get("uptime_hours", 0)
        if uptime:
            parts.append(f"[dim]⏱{uptime}h[/dim]")
    return " · ".join(parts)


def build_spider_status_line(spider_status: dict | None) -> str:
    """Build a live spider activity line."""
    if not spider_status:
        return "[dim]  No spider activity[/dim]"
    active = []
    for key, info in spider_status.items():
        if info.get("status") == "working":
            name = MINI_SPIDER.get(key, key)
            text = info.get("text", "working")[:25]
            active.append(f"{name} [dim]{text}[/dim]")
    if not active:
        return "[dim]  All spiders idle[/dim]"
    return "  " + " │ ".join(active[:4])


def print_hub(stats=None, metrics=None, spider_status=None, vault_mode=False, frame=0):
    """Print the full hub header to console."""
    console.print(build_web_hub(spider_status, vault_mode, frame))
    console.print(f"  {build_status_bar(stats, metrics)}")
    console.print(build_spider_status_line(spider_status))
    console.print("[dim]  /vault · /council · /dashboard · /status · /new · /quit[/dim]\n")


async def fetch_status(client: httpx.AsyncClient):
    """Fetch current stats, metrics, and spider activity."""
    stats = metrics = spiders = None
    try:
        r = await client.get(f"{HUB_BASE}/api/game/stats", headers=AUTH_HEADERS, timeout=3)
        stats = r.json()
    except Exception:
        pass
    try:
        r = await client.get(f"{HUB_BASE}/api/metrics", headers=AUTH_HEADERS, timeout=3)
        metrics = r.json()
    except Exception:
        pass
    try:
        r = await client.get(f"{HUB_BASE}/api/spiders/activity", headers=AUTH_HEADERS, timeout=3)
        d = r.json()
        spiders = d.get("spiders", {})
    except Exception:
        pass
    return stats, metrics, spiders


async def tui_chat():
    """Full terminal UI with animated web hub header."""
    console.clear()

    # Check server
    try:
        async with httpx.AsyncClient(timeout=5) as c:
            r = await c.get(f"{HUB_BASE}/health")
            if r.status_code != 200:
                raise Exception()
    except Exception:
        console.print("[red]Server not running. Start with: hub serve[/red]")
        return

    # Get initial state
    async with httpx.AsyncClient(timeout=5) as c:
        stats, metrics, spiders = await fetch_status(c)

    # Print initial hub
    frame = 0
    vault_mode = False
    print_hub(stats, metrics, spiders, vault_mode, frame)

    session_id = None
    force_agent = None

    while True:
        try:
            prompt_label = "[yellow]vault 🐺>[/yellow] " if vault_mode else "[bold red]you >[/bold red] "
            user_input = console.input(prompt_label).strip()
        except (EOFError, KeyboardInterrupt):
            console.print("\n[dim]🕸 Disconnecting from the web...[/dim]")
            break

        if not user_input:
            continue

        if user_input.lower() in ("/quit", "/exit", "/q"):
            console.print("[dim]🕸 Disconnecting from the web...[/dim]")
            break

        if user_input.lower() == "/new":
            if session_id:
                try:
                    async with httpx.AsyncClient() as c:
                        await c.delete(f"{HUB_BASE}/api/chat/{session_id}", headers=AUTH_HEADERS)
                except Exception:
                    pass
            session_id = None
            force_agent = None
            # Clear and reprint hub
            console.clear()
            frame += 1
            async with httpx.AsyncClient(timeout=3) as c:
                stats, metrics, spiders = await fetch_status(c)
            print_hub(stats, metrics, spiders, vault_mode, frame)
            continue

        if user_input.lower() in ("/vault", "/money", "/mm"):
            force_agent = "money_maker"
            vault_mode = True
            console.clear()
            frame += 1
            async with httpx.AsyncClient(timeout=3) as c:
                stats, metrics, spiders = await fetch_status(c)
            print_hub(stats, metrics, spiders, vault_mode, frame)
            console.print("[yellow]  🐺 Entered The Vault — Wolf is hunting.[/yellow]\n")
            continue

        if user_input.lower() in ("/exit_vault", "/ev"):
            force_agent = None
            vault_mode = False
            console.clear()
            frame += 1
            async with httpx.AsyncClient(timeout=3) as c:
                stats, metrics, spiders = await fetch_status(c)
            print_hub(stats, metrics, spiders, vault_mode, frame)
            console.print("[dim]  Left The Vault — normal routing.[/dim]\n")
            continue

        if user_input.lower() in ("/council", "/warroom", "/war"):
            user_input = "/council " + (user_input.split(None, 1)[1] if " " in user_input else "What should we focus on?")
            force_agent = "warroom"

        if user_input.lower() in ("/dashboard", "/web", "/open"):
            import subprocess
            subprocess.Popen(
                ["xdg-open", HUB_BASE],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
            console.print("[dim]  🕸 Opening dashboard in browser...[/dim]\n")
            continue

        if user_input.lower() == "/status":
            try:
                async with httpx.AsyncClient(timeout=5) as c:
                    stats, metrics, spiders = await fetch_status(c)
                    r = await c.get(f"{HUB_BASE}/api/config", headers=AUTH_HEADERS)
                    cfg = r.json()
                console.clear()
                frame += 1
                print_hub(stats, metrics, spiders, vault_mode, frame)
                console.print(f"  [dim]Mode: {cfg.get('mode', '?')} | Cloud: {sum(1 for v in cfg.values() if v is True)}/5[/dim]\n")
            except Exception:
                console.print("[dim]  Could not fetch status.[/dim]\n")
            continue

        if user_input.lower() == "/help":
            console.print("[dim]Commands:[/dim]")
            console.print("  /vault       Enter Wolf mode (The Vault)")
            console.print("  /council     Dark Room — all spiders strategize")
            console.print("  /dashboard   Open web dashboard in browser")
            console.print("  /status      Refresh hub with live status")
            console.print("  /new         Clear chat, refresh hub")
            console.print("  /quit        Disconnect from the web\n")
            continue

        # Show spider activity
        if force_agent and force_agent in SPIDER_WORKING:
            console.print(f"  [dim]{SPIDER_WORKING[force_agent]}[/dim]")

        # Stream response
        params = {"message": user_input}
        if session_id:
            params["session_id"] = session_id
        if force_agent:
            params["force_agent"] = force_agent

        agent = ""
        try:
            async with httpx.AsyncClient(timeout=httpx.Timeout(connect=10, read=300, write=10, pool=10)) as client:
                async with client.stream("GET", f"{HUB_BASE}/api/chat/stream", params=params, headers=AUTH_HEADERS) as resp:
                    current_event = ""
                    async for line in resp.aiter_lines():
                        if line.startswith("event:"):
                            current_event = line[6:].strip()
                        elif line.startswith("data:"):
                            import json
                            try:
                                data = json.loads(line[5:].strip())
                            except Exception:
                                continue

                            if current_event == "approve":
                                level = data.get("level", "")
                                spider = data.get("spider", "")
                                command = data.get("command", "")
                                label = MINI_SPIDER.get(spider, spider)
                                icon = "🔐" if level == "privileged" else "🔒"
                                console.print(Panel(
                                    f"[bold yellow]{command}[/bold yellow]",
                                    title=f"{icon} {label} — {'PRIVILEGED' if level=='privileged' else 'APPROVAL NEEDED'}",
                                    border_style="yellow" if level == "privileged" else "red",
                                    padding=(0, 1),
                                ))

                            elif current_event == "exec":
                                action = data.get("action", "")
                                spider = data.get("spider", "")
                                detail = data.get("detail", "")
                                label = MINI_SPIDER.get(spider, spider)
                                if action == "start":
                                    console.print(Panel(
                                        f"[bold]{detail}[/bold]",
                                        title=f"▶ {label} executing",
                                        border_style="yellow",
                                        padding=(0, 1),
                                    ))
                                elif action == "stdout" and detail.strip():
                                    console.print(f"  [dim]{detail[:300]}[/dim]")
                                elif action == "error":
                                    console.print(f"  [red]ERROR: {detail}[/red]")
                                elif action == "timeout":
                                    console.print(f"  [yellow]TIMEOUT: {detail}[/yellow]")
                                elif action == "done":
                                    console.print(f"  [green]{detail}[/green]")

                            elif current_event == "spider":
                                spider = data.get("spider", "")
                                text = data.get("text", "")
                                label = MINI_SPIDER.get(spider, spider)
                                console.print(f"  {label}: [dim]{text}[/dim]")

                            elif current_event == "token":
                                chunk = data.get("text", "")
                                if not session_id:
                                    session_id = data.get("session_id", "")

                                # Detect and skip routing tag
                                if chunk.startswith("*["):
                                    end = chunk.find("]*\n")
                                    if end > 0:
                                        agent = chunk[2:end].split("·")[0].strip()
                                        label = MINI_SPIDER.get(agent, agent)
                                        console.print(f"\n  {label}")
                                        continue

                                console.print(chunk, end="", highlight=False)

                            elif current_event == "done":
                                session_id = data.get("session_id", session_id)
                                xp = data.get("xp", {})
                                if xp and xp.get("xp_earned"):
                                    mult = f" ({xp['multiplier']}x)" if xp.get('multiplier', 1) > 1 else ""
                                    console.print(
                                        f"\n  [green]+{xp['xp_earned']} XP{mult}[/green] · "
                                        f"[red]Lv {xp.get('level', 0)}[/red] · "
                                        f"[white]{xp.get('total_xp', 0):,}[/white]"
                                    )
                                achs = data.get("achievements", [])
                                for a in achs:
                                    console.print(f"  [bold yellow]{a.get('icon', '🏆')} {a.get('name', '')}[/bold yellow]")

        except Exception as e:
            console.print(f"\n[red]Error: {e}[/red]")

        console.print()
