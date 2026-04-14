"""Agent status and info endpoints."""
from __future__ import annotations

from fastapi import APIRouter

from agentic_hub.config import load_models_config
from agentic_hub.core.gpu_scheduler import get_gpu_scheduler

router = APIRouter(prefix="/api/agents", tags=["agents"])


@router.get("")
async def list_agents():
    """List all available agents and their config."""
    config = load_models_config()
    agents = []

    for name, cfg in config.get("agents", {}).items():
        agents.append({
            "name": name,
            "display_name": cfg["display_name"],
            "description": cfg["description"],
            "local_model": cfg["local_model"],
            "xp_base": cfg.get("xp_base", 0),
            "type": "local",
        })

    # Add code team
    ct = config.get("code_team", {})
    agents.append({
        "name": "code_team",
        "display_name": ct.get("display_name", "Code Team"),
        "description": ct.get("description", "Opus + Codex collaborative coding"),
        "local_model": None,
        "cloud_models": [ct.get("opus_model", ""), ct.get("codex_model", "")],
        "xp_base": ct.get("xp_base", 20),
        "type": "cloud",
    })

    return {"agents": agents}


@router.get("/status")
async def agent_status():
    """Get current agent/model status including GPU state."""
    scheduler = get_gpu_scheduler()
    gpu_status = await scheduler.get_status()
    return {
        "gpu": gpu_status,
    }
