"""Interactive chat REPL for the CLI."""
from __future__ import annotations

import asyncio
import sys

import httpx
import typer
from rich.console import Console
from rich.live import Live
from rich.markdown import Markdown
from rich.panel import Panel
from rich.text import Text

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


async def _stream_chat(message: str, session_id: str | None) -> tuple[str, str]:
    """Stream a chat response from the hub API, printing tokens in real-time."""
    params = {"message": message}
    if session_id:
        params["session_id"] = session_id

    full_text = ""
    result_session_id = session_id or ""

    async with httpx.AsyncClient(timeout=httpx.Timeout(connect=10, read=300, write=10, pool=10)) as client:
        async with client.stream("GET", f"{HUB_BASE}/api/chat/stream", params=params, headers=AUTH_HEADERS) as resp:
            if resp.status_code != 200:
                body = await resp.aread()
                console.print(f"[red]Error {resp.status_code}:[/red] {body.decode()}")
                return "", result_session_id

            current_event = ""
            async for line in resp.aiter_lines():
                if line.startswith("event:"):
                    current_event = line[6:].strip()
                elif line.startswith("data:"):
                    import json
                    try:
                        data = json.loads(line[5:].strip())
                    except json.JSONDecodeError:
                        continue

                    if current_event == "token":
                        chunk = data.get("text", "")
                        full_text += chunk
                        console.print(chunk, end="", highlight=False)
                        if not result_session_id:
                            result_session_id = data.get("session_id", "")
                    elif current_event == "done":
                        result_session_id = data.get("session_id", result_session_id)
                        # Show XP earned
                        xp = data.get("xp", {})
                        if xp and xp.get("xp_earned"):
                            xp_text = f"+{xp['xp_earned']} XP"
                            if xp.get("streak_bonus"):
                                xp_text += f" (+{xp['streak_bonus']} streak)"
                            mult = xp.get("multiplier", 1.0)
                            if mult > 1.0:
                                xp_text += f" [dim]({mult}x local bonus)[/dim]"
                            console.print(
                                f"\n[dim cyan]  {xp_text}  ·  "
                                f"Lvl {xp.get('level', 0)}  ·  "
                                f"{xp.get('total_xp', 0):,} XP total[/dim cyan]"
                            )
                        # Show new achievements
                        achievements = data.get("achievements", [])
                        for ach in achievements:
                            console.print(
                                f"  [bold yellow]{ach.get('icon', '🏆')} Achievement Unlocked: "
                                f"{ach.get('name', '')}[/bold yellow]"
                            )

    return full_text, result_session_id


async def _check_server() -> bool:
    """Check if the hub API server is running."""
    try:
        async with httpx.AsyncClient(timeout=5) as client:
            resp = await client.get(f"{HUB_BASE}/health")
            return resp.status_code == 200
    except Exception:
        return False


async def _run_chat(message: str | None):
    """Main chat loop."""
    # Check server
    if not await _check_server():
        console.print(
            Panel(
                "[yellow]Hub server not running.[/yellow]\n"
                "Start it with: [bold]hub serve[/bold]",
                title="Connection Error",
                border_style="red",
            )
        )
        raise typer.Exit(1)

    session_id: str | None = None

    # One-shot mode
    if message:
        console.print()
        _, session_id = await _stream_chat(message, session_id)
        console.print("\n")
        return

    # Interactive REPL
    console.print(
        Panel(
            "[bold cyan]🕸  spider.Web[/bold cyan] — Opus orchestrated multi-agent AI\n"
            "[dim]Type your message. Opus decides which agent handles it.[/dim]\n"
            "[dim]Commands: /quit, /clear, /status[/dim]",
            border_style="cyan",
        )
    )

    while True:
        try:
            user_input = console.input("\n[bold magenta]you >[/bold magenta] ").strip()
        except (EOFError, KeyboardInterrupt):
            console.print("\n[dim]Goodbye.[/dim]")
            break

        if not user_input:
            continue

        if user_input.lower() in ("/quit", "/exit", "/q"):
            console.print("[dim]Goodbye.[/dim]")
            break

        if user_input.lower() == "/clear":
            if session_id:
                async with httpx.AsyncClient() as client:
                    await client.delete(f"{HUB_BASE}/api/chat/{session_id}", headers=AUTH_HEADERS)
            session_id = None
            console.print("[dim]Session cleared.[/dim]")
            continue

        if user_input.lower() == "/status":
            async with httpx.AsyncClient() as client:
                resp = await client.get(f"{HUB_BASE}/api/agents/status", headers=AUTH_HEADERS)
                if resp.status_code == 200:
                    import json
                    console.print_json(json.dumps(resp.json(), indent=2))
                else:
                    console.print(f"[red]Error: {resp.status_code}[/red]")
            continue

        console.print()
        _, session_id = await _stream_chat(user_input, session_id)
        console.print()


def chat_command(
    message: str = typer.Argument(None, help="One-shot message (omit for interactive REPL)"),
):
    """Chat with the Agentic Hub. Opus routes your message to the right agent."""
    asyncio.run(_run_chat(message))
