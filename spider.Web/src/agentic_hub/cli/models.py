"""Model management CLI commands."""
from __future__ import annotations

import asyncio
from pathlib import Path

import httpx
import typer
import yaml
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

console = Console()
models_app = typer.Typer(help="Manage local models")

HUB_BASE = "http://localhost:8420"
MODELS_YAML = Path(__file__).parent.parent.parent.parent / "config" / "models.yaml"


def _format_size(size_bytes: int) -> str:
    if size_bytes == 0:
        return "—"
    gb = size_bytes / (1024 ** 3)
    if gb >= 1:
        return f"{gb:.1f} GB"
    return f"{size_bytes / (1024 ** 2):.0f} MB"


async def _list_models():
    async with httpx.AsyncClient(timeout=10) as client:
        resp = await client.get(f"{HUB_BASE}/api/models")
        resp.raise_for_status()
        data = resp.json()

    # Also load agent assignments
    try:
        with open(MODELS_YAML) as f:
            config = yaml.safe_load(f)
        agent_models = {
            cfg["local_model"]: name
            for name, cfg in config.get("agents", {}).items()
        }
    except Exception:
        agent_models = {}

    table = Table(title="Ollama Models", border_style="cyan")
    table.add_column("Name", style="bold green")
    table.add_column("Size", justify="right")
    table.add_column("Family", style="dim")
    table.add_column("Params", style="dim")
    table.add_column("Assigned To", style="cyan")

    for m in data["models"]:
        details = m.get("details", {})
        name = m["name"]
        assigned = agent_models.get(name, "")
        table.add_row(
            name,
            _format_size(m.get("size", 0)),
            details.get("family", "—"),
            details.get("parameter_size", "—"),
            assigned,
        )

    console.print(table)


async def _running_models():
    async with httpx.AsyncClient(timeout=10) as client:
        resp = await client.get(f"{HUB_BASE}/api/models/running")
        resp.raise_for_status()
        data = resp.json()

    tracked = data.get("tracked_model", "none")
    running = data.get("running_models", [])
    console.print(f"[bold]Tracked:[/bold] {tracked}")
    console.print(f"[bold]In VRAM:[/bold] {', '.join(running) or 'none'}")


@models_app.command("list")
def list_models():
    """List all locally available models."""
    asyncio.run(_list_models())


@models_app.command("running")
def running():
    """Show which models are currently loaded in GPU memory."""
    asyncio.run(_running_models())


@models_app.command("pull")
def pull_model(
    name: str = typer.Argument(..., help="Model name to pull (e.g., qwen2.5:7b)"),
):
    """Pull a model from the Ollama registry."""
    from agentic_hub.core.ollama_client import OllamaClient

    async def _pull():
        client = OllamaClient()
        console.print(f"[cyan]Pulling {name}...[/cyan]")
        try:
            async for status in client.pull_model(name):
                console.print(f"  {status}", end="\r")
            console.print(f"\n[green]✓ {name} pulled successfully[/green]")
        except Exception as e:
            console.print(f"[red]Error: {e}[/red]")
        finally:
            await client.close()

    asyncio.run(_pull())


@models_app.command("import")
def import_model(
    hf: str = typer.Option(..., "--hf", help="HuggingFace repo ID (e.g., bartowski/Qwen2.5-Coder-7B-Instruct-GGUF)"),
    quant: str = typer.Option("Q4_K_M", help="Preferred quantization level"),
    name: str = typer.Option(None, help="Custom model name (auto-generated if omitted)"),
    max_size: float = typer.Option(6.0, help="Max file size in GB"),
    template: str = typer.Option(None, help="Chat template family: llama, chatml, mistral, phi, gemma, deepseek"),
):
    """Import a GGUF model from HuggingFace into Ollama."""
    from agentic_hub.core.hf_importer import HFImporter

    importer = HFImporter()

    # Step 1: List available files
    console.print(f"[cyan]Searching {hf} for GGUF files...[/cyan]")
    try:
        files = importer.list_gguf_files(hf)
    except ValueError as e:
        console.print(f"[red]{e}[/red]")
        raise typer.Exit(1)

    if not files:
        console.print(f"[red]No GGUF files found in {hf}[/red]")
        raise typer.Exit(1)

    # Show available files
    table = Table(title=f"GGUF files in {hf}", border_style="cyan")
    table.add_column("File", style="dim")
    table.add_column("Quant", style="green")
    table.add_column("Size", justify="right")

    for f in files:
        style = "bold green" if f.quant == quant.upper() else ""
        table.add_row(f.filename, f.quant, f"{f.size_gb:.1f} GB", style=style)

    console.print(table)

    # Step 2: Find best match
    best = importer.find_best_gguf(hf, quant, max_size)
    if best is None:
        console.print(f"[red]No GGUF file fits under {max_size}GB[/red]")
        raise typer.Exit(1)

    console.print(f"\n[cyan]Selected:[/cyan] {best.filename} ({best.quant}, {best.size_gb:.1f} GB)")

    # Step 3: Import
    console.print(f"[cyan]Downloading and importing...[/cyan]")
    try:
        result = importer.import_model(
            repo_id=hf,
            model_name=name,
            preferred_quant=quant,
            max_size_gb=max_size,
            template_family=template,
        )
    except Exception as e:
        console.print(f"[red]Import failed: {e}[/red]")
        raise typer.Exit(1)

    console.print(
        Panel(
            f"[bold green]✓ Model imported successfully[/bold green]\n\n"
            f"  Name: [bold]{result['model_name']}[/bold]\n"
            f"  Repo: {result['repo_id']}\n"
            f"  File: {result['gguf_file']}\n"
            f"  Quant: {result['quant']}\n"
            f"  Size: {result['size_gb']} GB\n"
            f"  Template: {result['template']}\n\n"
            f"[dim]Assign to an agent: hub models assign {result['model_name']} <agent>[/dim]",
            border_style="green",
        )
    )


@models_app.command("assign")
def assign_model(
    model: str = typer.Argument(..., help="Model name (from 'hub models list')"),
    agent: str = typer.Argument(..., help="Agent to assign to: scholar, automator, oracle"),
):
    """Assign a model to an agent. Updates config/models.yaml."""
    valid_agents = ["scholar", "automator", "oracle"]
    if agent not in valid_agents:
        console.print(f"[red]Invalid agent '{agent}'. Choose from: {', '.join(valid_agents)}[/red]")
        raise typer.Exit(1)

    # Load and update config
    try:
        with open(MODELS_YAML) as f:
            config = yaml.safe_load(f)
    except Exception as e:
        console.print(f"[red]Could not read models.yaml: {e}[/red]")
        raise typer.Exit(1)

    old_model = config["agents"][agent].get("local_model", "")
    config["agents"][agent]["local_model"] = model

    with open(MODELS_YAML, "w") as f:
        yaml.dump(config, f, default_flow_style=False, sort_keys=False)

    console.print(
        f"[green]✓ Assigned [bold]{model}[/bold] to [bold]{agent}[/bold][/green]"
    )
    if old_model:
        console.print(f"  [dim]Previous: {old_model}[/dim]")
    console.print(f"  [dim]Restart the server for changes to take effect.[/dim]")


@models_app.command("search")
def search_hf(
    query: str = typer.Argument(..., help="Search query (e.g., 'qwen2.5 coder GGUF')"),
    limit: int = typer.Option(10, help="Max results"),
):
    """Search HuggingFace for GGUF models."""
    from huggingface_hub import HfApi

    api = HfApi()
    console.print(f"[cyan]Searching HuggingFace for '{query}'...[/cyan]\n")

    results = api.list_models(
        search=query,
        sort="downloads",
        limit=limit,
    )

    table = Table(title="HuggingFace Models", border_style="cyan")
    table.add_column("Repo", style="bold")
    table.add_column("Downloads", justify="right", style="dim")
    table.add_column("Tags", style="dim")

    for model in results:
        tags = ", ".join(model.tags[:3]) if model.tags else "—"
        downloads = f"{model.downloads:,}" if model.downloads else "—"
        table.add_row(model.id, downloads, tags)

    console.print(table)
    console.print(f"\n[dim]Import with: hub models import --hf <repo>[/dim]")
