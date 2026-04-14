"""Stats CLI command — live gamification data."""
from __future__ import annotations

import asyncio

import httpx
import typer
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.progress_bar import ProgressBar
from rich.text import Text

console = Console()

HUB_BASE = "http://localhost:8420"


def _level_bar(xp_progress: int, xp_total: int, width: int = 30) -> str:
    """Render a text-based XP progress bar."""
    if xp_total <= 0:
        return "█" * width
    filled = int((xp_progress / xp_total) * width)
    empty = width - filled
    return f"[cyan]{'█' * filled}[/cyan][dim]{'░' * empty}[/dim]"


async def _show_stats():
    try:
        async with httpx.AsyncClient(timeout=10) as client:
            stats_resp = await client.get(f"{HUB_BASE}/api/game/stats")
            stats_resp.raise_for_status()
            stats = stats_resp.json()

            ach_resp = await client.get(f"{HUB_BASE}/api/game/achievements")
            ach_resp.raise_for_status()
            achievements = ach_resp.json()["achievements"]
    except Exception as e:
        console.print(f"[red]Error connecting to spider.Web server: {e}[/red]")
        console.print("[dim]Make sure the server is running: hub serve[/dim]")
        raise typer.Exit(1)

    level = stats["level"]
    total_xp = stats["total_xp"]
    xp_to_next = stats["xp_to_next_level"]
    xp_progress = stats["xp_progress_in_level"]
    next_total = stats["next_level_total_xp"]
    streak = stats["streak"]

    # Header
    console.print()
    console.print(
        Panel(
            f"[bold cyan]🕸  spider.BOB[/bold cyan]  ·  Level [bold yellow]{level}[/bold yellow]  ·  "
            f"[bold]{total_xp:,}[/bold] XP",
            border_style="cyan",
        )
    )

    # XP Progress bar
    bar_width = 40
    if next_total > 0 and xp_progress >= 0:
        bar = _level_bar(xp_progress, next_total - (next_total - xp_to_next - xp_progress), bar_width)
    else:
        bar = _level_bar(0, 1, bar_width)
    console.print(f"  Level {level} {bar} Level {level + 1}  ({xp_to_next:,} XP to go)")
    console.print()

    # Streak
    streak_icon = "🔥" if streak["current"] > 0 else "❄️"
    console.print(f"  {streak_icon} Streak: [bold]{streak['current']}[/bold] days  ·  "
                  f"Best: [bold]{streak['longest']}[/bold] days")
    console.print()

    # Agent breakdown
    if stats.get("agents"):
        table = Table(title="Agent Stats", border_style="cyan", show_lines=False)
        table.add_column("Agent", style="cyan")
        table.add_column("Uses", justify="right")
        table.add_column("XP Earned", justify="right", style="yellow")

        for agent, data in stats["agents"].items():
            table.add_row(agent, str(data["count"]), f"{data['total_xp']:,}")
        console.print(table)
        console.print()

    # Source breakdown
    sources = stats.get("sources", {})
    local = sources.get("local", 0)
    cloud = sources.get("cloud", 0)
    total = local + cloud
    if total > 0:
        local_pct = int(local / total * 100)
        console.print(f"  🔒 Local: {local_pct}% ({local})  ·  ☁️  Cloud: {100 - local_pct}% ({cloud})")
        console.print()

    # Achievements
    unlocked = [a for a in achievements if a["unlocked"]]
    locked = [a for a in achievements if not a["unlocked"]]

    if unlocked:
        ach_text = "  ".join(f"{a['icon']} {a['name']}" for a in unlocked)
        console.print(Panel(ach_text, title=f"[bold]Achievements ({len(unlocked)}/{len(achievements)})[/bold]",
                           border_style="yellow"))
    else:
        console.print(f"  [dim]No achievements yet. Keep chatting![/dim]")

    console.print()


def stats_command():
    """Show your gamification stats (XP, level, streaks, achievements)."""
    asyncio.run(_show_stats())
