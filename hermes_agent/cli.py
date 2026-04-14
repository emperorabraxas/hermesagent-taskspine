from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Optional

import typer
from rich.console import Console
from rich.panel import Panel

from hermes_agent.config import HermesConfig, ensure_config
from hermes_agent.models_suggest import suggest_low_tier_model
from hermes_agent.orchestrator import run_task

app = typer.Typer(add_completion=False, no_args_is_help=True)
console = Console()


@app.command()
def init(
    remote: Optional[str] = typer.Option(None, "--remote", help="Git remote URL to set as origin"),
    config_path: Optional[Path] = typer.Option(None, "--config", help="Override config path"),
):
    """Initialize HermesAgent config (and optionally set git remote)."""
    cfg_path = ensure_config(config_path)
    cfg = HermesConfig.load(cfg_path)

    if remote:
        cfg.git.remote = remote
        cfg.save(cfg_path)

    console.print(
        Panel(
            f"[bold green]✓ HermesAgent initialized[/bold green]\n\n"
            f"Config: [bold]{cfg_path}[/bold]\n"
            + (f"Remote: {cfg.git.remote}\n" if cfg.git.remote else ""),
            border_style="green",
        )
    )


repo_app = typer.Typer(add_completion=False, help="Manage the HermesAgent repo itself")
app.add_typer(repo_app, name="repo")


@repo_app.command("set-remote")
def repo_set_remote(
    remote: str = typer.Argument(..., help="Git remote URL to set as origin"),
    path: Path = typer.Option(Path.cwd(), "--path", help="Path to the HermesAgent git repo"),
):
    """Set `origin` remote for the HermesAgent git repo (explicit path; never guesses)."""
    from hermes_agent.git_utils import set_origin_remote

    set_origin_remote(repo_path=path, remote_url=remote)
    console.print(Panel(f"[bold green]✓ Set origin remote[/bold green]\n{remote}\n\nRepo: {path}", border_style="green"))


models_app = typer.Typer(add_completion=False, help="Model suggestion utilities")
app.add_typer(models_app, name="models")


@models_app.command("suggest")
def models_suggest(
    task: str = typer.Argument(..., help="What you want the low-tier model to do"),
    goal: str = typer.Option(
        "general",
        "--goal",
        help="Task goal: general|summarize|classify|extract|code",
    ),
    config_path: Optional[Path] = typer.Option(None, "--config", help="Override config path"),
    json_out: bool = typer.Option(False, "--json", help="Print machine-readable JSON"),
):
    """Suggest the best low-tier local model using benchmark signals (not likes/downloads)."""
    cfg_path = ensure_config(config_path)
    cfg = HermesConfig.load(cfg_path)
    rec = suggest_low_tier_model(task=task, goal=goal, cfg=cfg)
    if json_out:
        console.print_json(json.dumps(rec, indent=2))
    else:
        console.print(rec["report"])


@app.command()
def run(
    task: str = typer.Argument(..., help="The task to execute"),
    repo: Optional[Path] = typer.Option(None, "--repo", help="Target repo path (default: git root of CWD)"),
    config_path: Optional[Path] = typer.Option(None, "--config", help="Override config path"),
    no_paid: bool = typer.Option(False, "--no-paid", help="Disallow paid model usage"),
):
    """Run the Hermes pipeline: low-tier → Codex plan packet → (optional) Claude execution."""
    cfg_path = ensure_config(config_path)
    cfg = HermesConfig.load(cfg_path)
    run_task(task=task, repo=repo, cfg=cfg, no_paid=no_paid)


webhook_app = typer.Typer(add_completion=False, help="GitHub webhook receiver utilities")
app.add_typer(webhook_app, name="webhook")


@webhook_app.command("serve")
def webhook_serve(
    host: str = typer.Option("127.0.0.1", "--host", help="Bind host"),
    port: int = typer.Option(8787, "--port", help="Bind port"),
    path: str = typer.Option("/github/webhook", "--path", help="Webhook path"),
    inbox: Optional[Path] = typer.Option(None, "--inbox", help="Override inbox directory"),
):
    """Run a minimal GitHub webhook HTTP receiver (stdlib, no dependencies)."""
    from hermes_agent.webhook_receiver import serve

    serve(host=host, port=port, path=path, inbox_dir=inbox)


@webhook_app.command("list")
def webhook_list(
    inbox: Optional[Path] = typer.Option(None, "--inbox", help="Override inbox directory"),
    limit: int = typer.Option(20, "--limit", help="Max events to show"),
):
    """List received webhook events (most recent first)."""
    from hermes_agent.webhook_receiver import list_events

    events = list_events(inbox_dir=inbox, limit=limit)
    if not events:
        console.print("[dim]No webhook events yet.[/dim]")
        raise typer.Exit(0)
    for e in events:
        console.print(f"{e}")


@webhook_app.command("show")
def webhook_show(
    filename: str = typer.Argument(..., help="Event filename from `hermes webhook list`"),
    inbox: Optional[Path] = typer.Option(None, "--inbox", help="Override inbox directory"),
):
    """Show one stored webhook event JSON."""
    from hermes_agent.webhook_receiver import read_event

    console.print_json(read_event(filename=filename, inbox_dir=inbox))


def main():
    app()


if __name__ == "__main__":
    main()
