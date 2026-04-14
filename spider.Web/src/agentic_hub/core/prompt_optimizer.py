"""Auto-Prompt Optimization — score and improve agent system prompts.

Uses trace data to analyze prompt effectiveness:
  - R1 validation pass/fail (strongest signal)
  - Tool call success rate
  - Response quality indicators (length, coherence)
  - Token efficiency

Generates improved prompts via LLM, stored as candidates for review.
Never auto-applies — manual review required.
"""
from __future__ import annotations

import json
import logging
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from agentic_hub.core.trace import load_recent_traces

logger = logging.getLogger(__name__)

DATA_DIR = Path(__file__).parent.parent.parent.parent / "data"
OPTIMIZED_DIR = DATA_DIR / "optimized_prompts"


@dataclass
class PromptScore:
    """Score for a single prompt execution."""
    trace_id: str
    agent: str
    prompt_preview: str  # First 200 chars
    score: float         # 0.0 to 1.0
    signals: dict        # Individual scoring signals
    tokens_total: int
    timestamp: float


class PromptScorer:
    """Score prompt effectiveness using trace data.

    Scoring signals (weighted):
      - r1_validated: +0.35 (strongest positive signal)
      - r1_rejected: -0.30 (strong negative)
      - tool_success_rate: +0.20 (tools worked correctly)
      - response_length: +0.10 (not too short, not too long)
      - token_efficiency: +0.05 (quality per token)
    """

    WEIGHTS = {
        "r1_validated": 0.35,
        "r1_rejected": -0.30,
        "tool_success_rate": 0.20,
        "response_length": 0.10,
        "token_efficiency": 0.05,
    }

    def score_trace(self, trace: dict) -> PromptScore | None:
        """Score a single trace's prompt effectiveness."""
        agent = trace.get("agent", "")
        prompt = trace.get("prompt", "")
        if not agent:
            return None

        signals: dict[str, float] = {}

        # R1 validation signals
        spans = trace.get("spans", [])
        has_r1_pass = any(s.get("name") == "r1_validation" and s.get("status") == "ok" for s in spans)
        has_r1_fail = any(s.get("name") == "r1_validation" and s.get("status") == "rejected" for s in spans)
        signals["r1_validated"] = 1.0 if has_r1_pass else 0.0
        signals["r1_rejected"] = 1.0 if has_r1_fail else 0.0

        # Tool success rate
        tool_spans = [s for s in spans if s.get("tool_name")]
        if tool_spans:
            successes = sum(1 for s in tool_spans if s.get("tool_success", True))
            signals["tool_success_rate"] = successes / len(tool_spans)
        else:
            signals["tool_success_rate"] = 0.5  # Neutral if no tools used

        # Response length signal (sweet spot: 200-2000 chars)
        total_tokens_out = trace.get("total_tokens_out", 0)
        if total_tokens_out < 50:
            signals["response_length"] = 0.2  # Too short
        elif total_tokens_out > 3000:
            signals["response_length"] = 0.4  # Too long
        else:
            signals["response_length"] = 1.0  # Good range

        # Token efficiency (output quality per input token)
        total_tokens_in = trace.get("total_tokens_in", 0)
        if total_tokens_in > 0:
            ratio = total_tokens_out / total_tokens_in
            signals["token_efficiency"] = min(ratio, 1.0)  # Cap at 1.0
        else:
            signals["token_efficiency"] = 0.5

        # Compute weighted score
        score = 0.0
        for signal_name, weight in self.WEIGHTS.items():
            score += signals.get(signal_name, 0.0) * weight
        score = max(0.0, min(1.0, score + 0.5))  # Normalize to 0-1

        return PromptScore(
            trace_id=trace.get("trace_id", ""),
            agent=agent,
            prompt_preview=prompt[:200],
            score=round(score, 3),
            signals=signals,
            tokens_total=total_tokens_in + total_tokens_out,
            timestamp=trace.get("timestamp", 0),
        )

    def score_all(self, limit: int = 100) -> list[PromptScore]:
        """Score all recent traces."""
        traces = load_recent_traces(limit=limit)
        scores = []
        for trace in traces:
            score = self.score_trace(trace)
            if score:
                scores.append(score)
        return scores

    def score_by_agent(self, agent: str, limit: int = 100) -> list[PromptScore]:
        """Score traces for a specific agent."""
        all_scores = self.score_all(limit)
        return [s for s in all_scores if s.agent == agent]


class PromptOptimizer:
    """Analyze prompt performance and generate improved candidates.

    Optimization cycle:
      1. Score recent traces per agent
      2. Identify best/worst performing prompts
      3. Use LLM to generate improved system prompt
      4. Save as candidate for manual review
    """

    def __init__(self):
        self._scorer = PromptScorer()

    def analyze_agent(self, agent_name: str, limit: int = 100) -> dict:
        """Analyze prompt performance for an agent."""
        scores = self._scorer.score_by_agent(agent_name, limit)
        if not scores:
            return {
                "agent": agent_name,
                "total_traces": 0,
                "avg_score": 0,
                "best_prompts": [],
                "worst_prompts": [],
                "recommendation": "Not enough data — need more traces",
            }

        avg = sum(s.score for s in scores) / len(scores)
        sorted_scores = sorted(scores, key=lambda s: s.score, reverse=True)

        return {
            "agent": agent_name,
            "total_traces": len(scores),
            "avg_score": round(avg, 3),
            "best_prompts": [
                {"trace_id": s.trace_id, "score": s.score, "preview": s.prompt_preview, "signals": s.signals}
                for s in sorted_scores[:5]
            ],
            "worst_prompts": [
                {"trace_id": s.trace_id, "score": s.score, "preview": s.prompt_preview, "signals": s.signals}
                for s in sorted_scores[-5:]
            ],
            "recommendation": self._get_recommendation(avg, scores),
        }

    def analyze_all_agents(self) -> dict:
        """Analyze all agents."""
        from agentic_hub.config import load_models_config
        config = load_models_config()
        agents = list(config.get("agents", {}).keys())

        results = {}
        for agent in agents:
            results[agent] = self.analyze_agent(agent)
        return results

    async def generate_improved_prompt(self, agent_name: str) -> str | None:
        """Use LLM to generate an improved system prompt based on analysis.

        Returns the improved prompt text, or None if optimization isn't warranted.
        """
        analysis = self.analyze_agent(agent_name)
        if analysis["total_traces"] < 10:
            return None
        if analysis["avg_score"] > 0.85:
            return None  # Already performing well

        # Get current system prompt
        from agentic_hub.config import load_models_config
        config = load_models_config()
        current_prompt = config.get("agents", {}).get(agent_name, {}).get("system_prompt", "")

        optimize_request = f"""You are a prompt optimization expert. Analyze this system prompt and improve it.

CURRENT SYSTEM PROMPT for agent '{agent_name}':
{current_prompt}

PERFORMANCE DATA:
- Average score: {analysis['avg_score']} (out of 1.0)
- Total traces analyzed: {analysis['total_traces']}
- Best performing prompts scored: {[p['score'] for p in analysis['best_prompts']]}
- Worst performing prompts scored: {[p['score'] for p in analysis['worst_prompts']]}
- Recommendation: {analysis['recommendation']}

Generate an improved version of the system prompt that:
1. Keeps the core agent identity and purpose
2. Adds clearer instructions for common failure modes
3. Improves tool usage guidance
4. Is concise but comprehensive

Return ONLY the improved system prompt text, nothing else."""

        # Use local model for optimization (no cloud cost)
        try:
            from agentic_hub.core.ollama_client import get_ollama
            from agentic_hub.core.gpu_scheduler import get_gpu_scheduler
            from agentic_hub.config import get_settings

            settings = get_settings()
            model = "deepseek-r1:7b"
            scheduler = get_gpu_scheduler()
            await scheduler.ensure_model(model)

            ollama = get_ollama()
            result = await ollama.chat_completion(
                model=model,
                messages=[{"role": "user", "content": optimize_request}],
                keep_alive=settings.model_keep_alive,
            )

            if result and result.text:
                # Save as candidate
                self._save_candidate(agent_name, result.text, analysis)
                return result.text

        except Exception as e:
            logger.warning(f"Prompt optimization failed: {e}")

        return None

    def _save_candidate(self, agent_name: str, prompt: str, analysis: dict) -> Path:
        """Save an optimized prompt candidate for review."""
        OPTIMIZED_DIR.mkdir(parents=True, exist_ok=True)
        timestamp = int(time.time())
        path = OPTIMIZED_DIR / f"{agent_name}_{timestamp}.md"
        content = f"""# Optimized Prompt Candidate: {agent_name}

## Timestamp: {timestamp}
## Previous Average Score: {analysis['avg_score']}
## Traces Analyzed: {analysis['total_traces']}

## Candidate Prompt:

{prompt}

## Analysis:

{json.dumps(analysis, indent=2, default=str)}
"""
        path.write_text(content)
        logger.info(f"Saved prompt candidate: {path}")
        return path

    def get_candidates(self, agent_name: str = "") -> list[dict]:
        """List saved prompt optimization candidates."""
        if not OPTIMIZED_DIR.exists():
            return []

        candidates = []
        pattern = f"{agent_name}_*.md" if agent_name else "*.md"
        for f in sorted(OPTIMIZED_DIR.glob(pattern), reverse=True):
            candidates.append({
                "file": f.name,
                "agent": f.stem.rsplit("_", 1)[0],
                "timestamp": int(f.stem.rsplit("_", 1)[-1]) if "_" in f.stem else 0,
                "size": f.stat().st_size,
            })
        return candidates[:20]  # Last 20

    @staticmethod
    def _get_recommendation(avg_score: float, scores: list[PromptScore]) -> str:
        """Generate a human-readable recommendation."""
        if avg_score >= 0.85:
            return "Performing well — no optimization needed"
        if avg_score >= 0.7:
            return "Good performance, minor improvements possible"
        if avg_score >= 0.5:
            return "Moderate performance — optimization recommended"
        return "Poor performance — prompt rewrite strongly recommended"


# Singleton
_optimizer: PromptOptimizer | None = None


def get_prompt_optimizer() -> PromptOptimizer:
    global _optimizer
    if _optimizer is None:
        _optimizer = PromptOptimizer()
    return _optimizer
