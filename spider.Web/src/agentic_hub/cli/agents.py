"""Agent management CLI commands."""
from __future__ import annotations

import asyncio

import httpx
import typer
from rich.console import Console
from rich.table import Table

console = Console()
agents_app = typer.Typer(help="Manage agents")

HUB_BASE = "http://localhost:8420"


async def _list_agents():
    async with httpx.AsyncClient(timeout=10) as client:
        resp = await client.get(f"{HUB_BASE}/api/agents")
        resp.raise_for_status()
        data = resp.json()

    table = Table(title="spider.Web — Agents", border_style="cyan")
    table.add_column("Agent", style="bold cyan")
    table.add_column("Type", style="dim")
    table.add_column("Model", style="green")
    table.add_column("Description")
    table.add_column("XP", justify="right", style="yellow")

    for agent in data["agents"]:
        model = agent.get("local_model") or ", ".join(agent.get("cloud_models", []))
        table.add_row(
            agent["display_name"],
            agent["type"],
            model,
            agent["description"],
            str(agent["xp_base"]),
        )

    console.print(table)


async def _agent_status():
    async with httpx.AsyncClient(timeout=10) as client:
        resp = await client.get(f"{HUB_BASE}/api/agents/status")
        resp.raise_for_status()
        data = resp.json()

    gpu = data.get("gpu", {})
    console.print(f"[bold]GPU Model:[/bold] {gpu.get('tracked_model', 'none')}")
    console.print(f"[bold]Running:[/bold] {', '.join(gpu.get('running_models', [])) or 'none'}")
    console.print(f"[bold]Lock held:[/bold] {gpu.get('lock_held', False)}")


@agents_app.command("list")
def list_agents():
    """List all available agents."""
    asyncio.run(_list_agents())


@agents_app.command("status")
def agent_status():
    """Show current agent and GPU status."""
    asyncio.run(_agent_status())
