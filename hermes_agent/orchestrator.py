from __future__ import annotations

import os
import subprocess
from pathlib import Path

import typer
from rich.console import Console
from rich.panel import Panel

import time
import shlex

from hermes_agent.claude_executor import build_claude_command, run_claude
from hermes_agent.config import HermesConfig
from hermes_agent.models_suggest import suggest_low_tier_model
from hermes_agent.ollama_local import is_ollama_reachable, run_local_ideation
from hermes_agent.openai_planner import generate_plan_packet
from hermes_agent.repo_inspect import resolve_repo_root, summarize_repo

console = Console()


def _confirm(prompt: str) -> bool:
    return bool(typer.confirm(prompt, default=False))


def _run_make_test(repo_root: Path) -> tuple[int, str]:
    try:
        p = subprocess.run(["make", "test"], cwd=str(repo_root), capture_output=True, text=True)
        out = (p.stdout or "") + ("\n" + p.stderr if p.stderr else "")
        return int(p.returncode), out.strip()
    except FileNotFoundError:
        return 127, "make not found"
    except Exception as e:
        return 1, f"make test failed to run: {e}"


def run_task(*, task: str, repo: Path | None, cfg: HermesConfig, no_paid: bool) -> None:
    repo_root = resolve_repo_root(Path.cwd() if repo is None else repo)

    console.print(Panel(f"[bold]Task[/bold]\n{task}\n\n[bold]Repo[/bold]\n{repo_root}", border_style="cyan"))

    local_notes = ""
    if cfg.low.local_model:
        if is_ollama_reachable(cfg.low.ollama_base_url):
            try:
                local_notes = run_local_ideation(
                    base_url=cfg.low.ollama_base_url,
                    model=cfg.low.local_model,
                    task=task,
                )
                if local_notes:
                    console.print(Panel(local_notes, title="Low Tier (local) — ideation only", border_style="magenta"))
            except Exception as e:
                console.print(f"[yellow]Local ideation failed (non-fatal): {e}[/yellow]")
        else:
            console.print("[yellow]Ollama not reachable; skipping local ideation.[/yellow]")
            console.print(suggest_low_tier_model(task=task, goal="general", cfg=cfg)["report"])
    else:
        # No local model configured; still give a benchmark-based suggestion.
        console.print(suggest_low_tier_model(task=task, goal="general", cfg=cfg)["report"])

    if no_paid:
        console.print("[yellow]Paid models disabled via --no-paid. Stopping after local guidance.[/yellow]")
        return

    # Paid-gate: always ask before calling OpenAI.
    if not _confirm(f"Call OpenAI ({cfg.openai.model}) to generate a Claude execution packet?"):
        console.print("[dim]Aborted before paid call.[/dim]")
        return

    repo_summary = summarize_repo(repo_root)
    extra = local_notes.strip()

    packet = generate_plan_packet(
        model=cfg.openai.model,
        task=task,
        repo_summary=repo_summary,
        extra_context=extra,
        max_tokens=cfg.openai.max_tokens,
    )

    console.print(Panel(packet.plan, title=f"Plan (confidence {packet.confidence:.2f})", border_style="green"))

    while True:
        if packet.blocking_questions:
            console.print(
                Panel(
                    "\n".join(f"- {q}" for q in packet.blocking_questions),
                    title="Blocking Questions",
                    border_style="yellow",
                )
            )

        if packet.confidence >= cfg.openai.confidence_threshold and not packet.blocking_questions:
            break

        console.print(
            f"[yellow]Not ready[/yellow] (confidence {packet.confidence:.2f} < {cfg.openai.confidence_threshold:.2f} "
            f"or blocking questions remain)."
        )
        if not _confirm("Answer questions now and regenerate the plan packet (paid call)?"):
            console.print("[dim]Stopping before further paid calls.[/dim]")
            return

        answers = []
        for q in packet.blocking_questions:
            a = typer.prompt(q, default="")
            if a.strip():
                answers.append(f"Q: {q}\nA: {a.strip()}")
        extra = (extra + "\n\n" + "\n\n".join(answers)).strip()

        if not _confirm(f"Call OpenAI ({cfg.openai.model}) again with your answers?"):
            console.print("[dim]Stopping before paid call.[/dim]")
            return

        packet = generate_plan_packet(
            model=cfg.openai.model,
            task=task,
            repo_summary=repo_summary,
            extra_context=extra,
            max_tokens=cfg.openai.max_tokens,
        )
        console.print(Panel(packet.plan, title=f"Plan (confidence {packet.confidence:.2f})", border_style="green"))

    # Prepare prompt file for Claude
    if not _confirm("Approve this plan and generate the Claude Code execution prompt?"):
        console.print("[dim]Stopped before generating Claude prompt.[/dim]")
        return

    runs_dir = Path.home() / ".config" / "hermes-agent" / "runs"
    runs_dir.mkdir(parents=True, exist_ok=True)
    ts = time.strftime("%Y%m%d-%H%M%S")
    prompt_path = runs_dir / f"{ts}-claude_prompt.txt"
    prompt_path.write_text(packet.claude_prompt)

    console.print(Panel(f"Wrote Claude prompt to:\n{prompt_path}", border_style="cyan"))

    if not cfg.claude.enabled:
        console.print("[dim]Claude execution disabled in config. Done.[/dim]")
        return

    if not _confirm("Run Claude Code now? (This will edit files in the target repo)"):
        # Print copy/paste command
        cmd = [cfg.claude.command, "-p", "--add-dir", str(repo_root), "--permission-mode", cfg.claude.permission_mode]
        if cfg.claude.model:
            cmd += ["--model", cfg.claude.model]
        cmd_str = shlex.join(cmd + [f"$(cat {shlex.quote(str(prompt_path))})"])
        console.print("[bold]Run manually:[/bold]")
        console.print(cmd_str)
        return

    claude = build_claude_command(
        claude_bin=cfg.claude.command,
        repo_path=repo_root,
        prompt_path=prompt_path,
        permission_mode=cfg.claude.permission_mode,
        model=cfg.claude.model,
    )
    rc = run_claude(claude.command)
    console.print(f"[bold]Claude exit code:[/bold] {rc}")

    # Validation gate: always attempt make test.
    test_rc, output = _run_make_test(repo_root)
    style = "green" if test_rc == 0 else "red"
    console.print(Panel(output or "(no output)", title=f"make test (rc={test_rc})", border_style=style))
