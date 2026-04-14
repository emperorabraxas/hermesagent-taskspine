"""Main CLI application — the `hub` command."""
from __future__ import annotations

import subprocess
import sys
import time
import webbrowser

import httpx
import typer

from agentic_hub.cli.chat import chat_command
from agentic_hub.cli.agents import agents_app
from agentic_hub.cli.models import models_app
from agentic_hub.cli.stats import stats_command
from agentic_hub.cli.setup import needs_setup, run_setup

app = typer.Typer(
    name="hub",
    help="spider.Web — Local multi-agent AI platform with Opus orchestration",
    invoke_without_command=True,
)


@app.callback(invoke_without_command=True)
def main_callback(ctx: typer.Context):
    """spider.Web — auto-launches the server and web UI when run with no args."""
    if needs_setup():
        run_setup()

    # If a subcommand is being invoked, let it handle things
    if ctx.invoked_subcommand is not None:
        return

    # No subcommand — launch the full spider.Web experience
    _launch_spider_web()


def _is_server_running() -> bool:
    try:
        resp = httpx.get("http://localhost:8420/health", timeout=3)
        return resp.status_code == 200
    except Exception:
        return False


def _launch_spider_web():
    """Start the API server and open the web UI."""
    from rich.console import Console
    from rich.panel import Panel
    console = Console()

    console.print(
        Panel(
            "[bold cyan]🕸  spider.Web[/bold cyan]\n"
            "[dim]Starting your multi-agent AI platform...[/dim]",
            border_style="cyan",
        )
    )

    if not _is_server_running():
        console.print("[dim]Starting API server on :8420...[/dim]")
        # Start server in background
        subprocess.Popen(
            [sys.executable, "-m", "uvicorn", "agentic_hub.main:app",
             "--host", "127.0.0.1", "--port", "8420"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            start_new_session=True,
        )
        # Wait for server to be ready
        for _ in range(20):
            time.sleep(0.5)
            if _is_server_running():
                break
        else:
            console.print("[red]Server failed to start. Run 'hub serve' for details.[/red]")
            raise typer.Exit(1)

        console.print("[green]✓ Server running on http://localhost:8420[/green]")
    else:
        console.print("[green]✓ Server already running[/green]")

    # Open web UI
    web_url = "http://localhost:8420"
    console.print(f"[dim]Opening {web_url} in browser...[/dim]")
    webbrowser.open(web_url)

    console.print()
    console.print("[dim]Other commands:[/dim]")
    console.print("  [bold]hub chat[/bold]      — CLI chat REPL")
    console.print("  [bold]hub stats[/bold]     — Gamification stats")
    console.print("  [bold]hub agents list[/bold] — Show agents")
    console.print("  [bold]hub models list[/bold] — Show models")
    console.print()


# Register sub-commands
app.command("chat")(chat_command)
app.command("stats")(stats_command)
app.add_typer(agents_app, name="agents")
app.add_typer(models_app, name="models")


@app.command("tui")
def tui_command():
    """Launch the terminal UI — ASCII art spider.Web with persistent header."""
    import asyncio
    from agentic_hub.cli.tui import tui_chat
    asyncio.run(tui_chat())


@app.command("setup")
def setup_command():
    """Re-run the first-launch setup wizard."""
    run_setup()


@app.command("index")
def index_command(
    directory: str = typer.Argument(".", help="Directory to index for RAG"),
    force: bool = typer.Option(False, help="Re-index all files even if unchanged"),
):
    """Index local files for Scholar's RAG pipeline."""
    import asyncio
    from rich.console import Console
    console = Console()

    async def _index():
        from agentic_hub.core.rag import RAGPipeline
        rag = RAGPipeline()
        console.print(f"[cyan]Indexing {directory}...[/cyan]")
        result = await rag.index_directory(directory, force=force)
        if "error" in result:
            console.print(f"[red]{result['error']}[/red]")
            return
        console.print(f"[green]✓ Indexed {result['files_indexed']} files ({result['chunks_created']} chunks)[/green]")
        if result['files_skipped']:
            console.print(f"  [dim]{result['files_skipped']} files unchanged (skipped)[/dim]")
        stats = rag.get_stats()
        console.print(f"  [dim]Total index: {stats['total_files']} files, {stats['total_chunks']} chunks[/dim]")

    asyncio.run(_index())


@app.command("serve")
def serve(
    host: str = typer.Option("127.0.0.1", help="Host to bind to (use 0.0.0.0 for LAN access)"),
    port: int = typer.Option(8420, help="Port to listen on"),
    reload: bool = typer.Option(False, help="Enable auto-reload for development"),
):
    """Start the spider.Web API server."""
    import uvicorn
    uvicorn.run(
        "agentic_hub.main:app",
        host=host,
        port=port,
        reload=reload,
    )


if __name__ == "__main__":
    app()
