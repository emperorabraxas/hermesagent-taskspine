"""Execution tracing — spans, token counting, cost tracking, latency breakdown."""
from __future__ import annotations

import json
import logging
import time
import uuid
from dataclasses import dataclass, field, asdict
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)

DATA_DIR = Path(__file__).parent.parent.parent.parent / "data"
TRACES_DIR = DATA_DIR / "traces"


@dataclass
class Span:
    """One step in an execution trace — an LLM call, tool exec, or routing decision."""
    span_id: str = field(default_factory=lambda: uuid.uuid4().hex[:12])
    trace_id: str = ""
    parent_span_id: str = ""
    name: str = ""              # "llm_call", "tool_exec", "routing", "validation", "model_load"
    agent: str = ""
    started_at: float = 0.0     # time.monotonic()
    ended_at: float = 0.0

    # LLM-specific
    model: str = ""
    provider: str = ""          # "ollama", "anthropic", "openai", "google", "deepseek", "xai"
    tokens_in: int = 0
    tokens_out: int = 0

    # Cost
    cost_usd: float = 0.0

    # Tool-specific
    tool_name: str = ""
    tool_input: dict = field(default_factory=dict)
    tool_output: str = ""
    tool_success: bool = True

    # Prompt (for optimization analysis)
    prompt: str = ""

    # Status
    status: str = "ok"          # "ok", "error", "timeout"
    error: str = ""

    @property
    def duration_ms(self) -> int:
        if self.ended_at and self.started_at:
            return int((self.ended_at - self.started_at) * 1000)
        return 0

    def to_dict(self) -> dict:
        d = asdict(self)
        d["duration_ms"] = self.duration_ms
        return d


@dataclass
class Trace:
    """A complete execution trace — all spans from one user interaction."""
    trace_id: str = field(default_factory=lambda: uuid.uuid4().hex[:16])
    user_message: str = ""
    agent: str = ""
    started_at: float = field(default_factory=time.monotonic)
    ended_at: float = 0.0
    spans: list[Span] = field(default_factory=list)

    # Aggregated stats
    total_tokens_in: int = 0
    total_tokens_out: int = 0
    total_cost_usd: float = 0.0
    tool_calls_count: int = 0

    def start_span(self, name: str, agent: str = "", **kwargs) -> Span:
        """Create and register a new span."""
        span = Span(
            trace_id=self.trace_id,
            name=name,
            agent=agent or self.agent,
            started_at=time.monotonic(),
            **kwargs,
        )
        self.spans.append(span)
        return span

    def end_span(self, span: Span, **kwargs):
        """Finalize a span with end time and optional extra data."""
        span.ended_at = time.monotonic()
        for k, v in kwargs.items():
            if hasattr(span, k):
                setattr(span, k, v)
        # Aggregate
        if span.tokens_in:
            self.total_tokens_in += span.tokens_in
        if span.tokens_out:
            self.total_tokens_out += span.tokens_out
        if span.cost_usd:
            self.total_cost_usd += span.cost_usd
        if span.tool_name:
            self.tool_calls_count += 1

    def finalize(self):
        """Mark trace as complete."""
        self.ended_at = time.monotonic()

    @property
    def duration_ms(self) -> int:
        if self.ended_at and self.started_at:
            return int((self.ended_at - self.started_at) * 1000)
        return 0

    def to_dict(self) -> dict:
        return {
            "trace_id": self.trace_id,
            "user_message": self.user_message[:200],
            "agent": self.agent,
            "duration_ms": self.duration_ms,
            "total_tokens_in": self.total_tokens_in,
            "total_tokens_out": self.total_tokens_out,
            "total_cost_usd": round(self.total_cost_usd, 6),
            "tool_calls_count": self.tool_calls_count,
            "spans": [s.to_dict() for s in self.spans],
        }

    def save(self):
        """Persist trace to JSONL file."""
        TRACES_DIR.mkdir(parents=True, exist_ok=True)
        trace_file = TRACES_DIR / "traces.jsonl"
        try:
            with open(trace_file, "a") as f:
                f.write(json.dumps(self.to_dict(), default=str) + "\n")
            # Trim to last 1000 traces
            _trim_traces(trace_file, max_lines=1000)
        except Exception as e:
            logger.warning(f"Failed to save trace: {e}")


def _trim_traces(filepath: Path, max_lines: int = 1000):
    """Keep only the last N traces in the JSONL file."""
    try:
        lines = filepath.read_text().strip().split("\n")
        if len(lines) > max_lines:
            filepath.write_text("\n".join(lines[-max_lines:]) + "\n")
    except Exception:
        pass


def load_recent_traces(limit: int = 50) -> list[dict]:
    """Load the most recent traces."""
    trace_file = TRACES_DIR / "traces.jsonl"
    if not trace_file.exists():
        return []
    try:
        lines = trace_file.read_text().strip().split("\n")
        traces = []
        for line in lines[-limit:]:
            if line.strip():
                traces.append(json.loads(line))
        return list(reversed(traces))  # Most recent first
    except Exception as e:
        logger.warning(f"Failed to load traces: {e}")
        return []


def get_trace_stats() -> dict:
    """Aggregate stats across all stored traces."""
    traces = load_recent_traces(limit=1000)
    if not traces:
        return {"total_traces": 0, "total_tokens_in": 0, "total_tokens_out": 0,
                "total_cost_usd": 0.0, "avg_duration_ms": 0, "total_tool_calls": 0}

    total_in = sum(t.get("total_tokens_in", 0) for t in traces)
    total_out = sum(t.get("total_tokens_out", 0) for t in traces)
    total_cost = sum(t.get("total_cost_usd", 0) for t in traces)
    total_tools = sum(t.get("tool_calls_count", 0) for t in traces)
    durations = [t.get("duration_ms", 0) for t in traces if t.get("duration_ms", 0) > 0]
    avg_dur = int(sum(durations) / len(durations)) if durations else 0

    return {
        "total_traces": len(traces),
        "total_tokens_in": total_in,
        "total_tokens_out": total_out,
        "total_cost_usd": round(total_cost, 4),
        "avg_duration_ms": avg_dur,
        "total_tool_calls": total_tools,
    }
