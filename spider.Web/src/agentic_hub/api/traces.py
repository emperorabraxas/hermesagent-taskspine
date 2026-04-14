"""Trace API — execution traces, token counts, cost tracking."""
from __future__ import annotations

from fastapi import APIRouter

from agentic_hub.core.trace import load_recent_traces, get_trace_stats

router = APIRouter(prefix="/api", tags=["traces"])


@router.get("/traces")
async def list_traces(limit: int = 50):
    """List recent execution traces."""
    traces = load_recent_traces(limit=min(limit, 200))
    # Return summary only (no full spans) for listing
    return [
        {
            "trace_id": t["trace_id"],
            "user_message": t.get("user_message", "")[:100],
            "agent": t.get("agent", ""),
            "duration_ms": t.get("duration_ms", 0),
            "total_tokens_in": t.get("total_tokens_in", 0),
            "total_tokens_out": t.get("total_tokens_out", 0),
            "total_cost_usd": t.get("total_cost_usd", 0),
            "tool_calls_count": t.get("tool_calls_count", 0),
        }
        for t in traces
    ]


@router.get("/traces/stats")
async def trace_stats():
    """Aggregated stats across all stored traces."""
    stats = get_trace_stats()

    # Include semantic cache stats
    try:
        from agentic_hub.core.semantic_cache import get_semantic_cache
        cache = await get_semantic_cache()
        stats["semantic_cache"] = cache.get_stats()
    except Exception:
        stats["semantic_cache"] = {"status": "unavailable"}

    return stats


@router.get("/traces/prompt-analysis")
async def prompt_analysis(agent: str = ""):
    """Analyze prompt effectiveness across traces."""
    from agentic_hub.core.prompt_optimizer import get_prompt_optimizer
    optimizer = get_prompt_optimizer()
    if agent:
        return {"status": "ok", "analysis": optimizer.analyze_agent(agent)}
    return {"status": "ok", "analysis": optimizer.analyze_all_agents()}


@router.get("/traces/prompt-candidates")
async def prompt_candidates(agent: str = ""):
    """List saved prompt optimization candidates."""
    from agentic_hub.core.prompt_optimizer import get_prompt_optimizer
    optimizer = get_prompt_optimizer()
    return {"status": "ok", "candidates": optimizer.get_candidates(agent)}


@router.post("/traces/prompt-optimize/{agent_name}")
async def optimize_prompt(agent_name: str):
    """Generate an improved prompt for an agent (manual review required)."""
    from agentic_hub.core.prompt_optimizer import get_prompt_optimizer
    optimizer = get_prompt_optimizer()
    result = await optimizer.generate_improved_prompt(agent_name)
    if result:
        return {"status": "ok", "agent": agent_name, "candidate": result[:500], "message": "Saved to data/optimized_prompts/"}
    return {"status": "skipped", "agent": agent_name, "message": "Not enough data or already performing well"}


@router.get("/traces/{trace_id}")
async def get_trace(trace_id: str):
    """Get a specific trace with full span detail."""
    traces = load_recent_traces(limit=1000)
    for t in traces:
        if t.get("trace_id") == trace_id:
            return t
    return {"error": "Trace not found"}
