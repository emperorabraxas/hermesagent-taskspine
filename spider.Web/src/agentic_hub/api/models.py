"""Model management endpoints."""
from __future__ import annotations

import asyncio
from pathlib import Path

import yaml
from fastapi import APIRouter, BackgroundTasks
from pydantic import BaseModel

from agentic_hub.core.gpu_scheduler import get_gpu_scheduler
from agentic_hub.core.ollama_client import get_ollama

router = APIRouter(prefix="/api/models", tags=["models"])

MODELS_YAML = Path(__file__).parent.parent.parent.parent / "config" / "models.yaml"


@router.get("")
async def list_models():
    """List all locally available Ollama models."""
    ollama = get_ollama()
    models = await ollama.list_models()

    # Load agent assignments
    try:
        with open(MODELS_YAML) as f:
            config = yaml.safe_load(f)
        agent_models = {
            cfg["local_model"]: name
            for name, cfg in config.get("agents", {}).items()
        }
    except Exception:
        agent_models = {}

    return {
        "models": [
            {
                "name": m.get("name", ""),
                "size": m.get("size", 0),
                "modified_at": m.get("modified_at", ""),
                "details": m.get("details", {}),
                "assigned_to": agent_models.get(m.get("name", ""), ""),
            }
            for m in models
        ]
    }


@router.get("/running")
async def running_models():
    """Show which models are currently loaded in memory."""
    scheduler = get_gpu_scheduler()
    return await scheduler.get_status()


class HFSearchRequest(BaseModel):
    query: str
    limit: int = 10


@router.post("/search-hf")
async def search_hf(req: HFSearchRequest):
    """Search HuggingFace for GGUF models."""
    from huggingface_hub import HfApi

    api = HfApi()
    results = api.list_models(
        search=req.query,
        sort="downloads",
        limit=req.limit,
    )

    return {
        "models": [
            {
                "id": m.id,
                "downloads": m.downloads or 0,
                "tags": m.tags[:5] if m.tags else [],
            }
            for m in results
        ]
    }


class HFImportRequest(BaseModel):
    repo_id: str
    quant: str = "Q4_K_M"
    model_name: str | None = None
    max_size_gb: float = 6.0
    template: str | None = None


@router.post("/import-hf")
async def import_hf_model(req: HFImportRequest):
    """Import a GGUF model from HuggingFace (runs synchronously — may take a while)."""
    from agentic_hub.core.hf_importer import HFImporter

    importer = HFImporter()

    # Run the blocking import in a thread
    result = await asyncio.to_thread(
        importer.import_model,
        repo_id=req.repo_id,
        model_name=req.model_name,
        preferred_quant=req.quant,
        max_size_gb=req.max_size_gb,
        template_family=req.template,
    )

    return result


class AssignRequest(BaseModel):
    model: str
    agent: str


@router.post("/assign")
async def assign_model(req: AssignRequest):
    """Assign a model to an agent."""
    valid_agents = ["scholar", "automator", "oracle"]
    if req.agent not in valid_agents:
        return {"error": f"Invalid agent. Choose from: {valid_agents}"}

    try:
        with open(MODELS_YAML) as f:
            config = yaml.safe_load(f)

        old_model = config["agents"][req.agent].get("local_model", "")
        config["agents"][req.agent]["local_model"] = req.model

        with open(MODELS_YAML, "w") as f:
            yaml.dump(config, f, default_flow_style=False, sort_keys=False)

        return {
            "status": "ok",
            "agent": req.agent,
            "model": req.model,
            "previous_model": old_model,
        }
    except Exception as e:
        return {"error": str(e)}
