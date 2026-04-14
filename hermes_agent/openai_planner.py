from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Any

from openai import OpenAI


PLANNER_SYSTEM = """You are HermesAgent's planning brain.

You do NOT execute. You do NOT edit files. You produce an execution packet for Claude Code.

Git policy:
- HermesAgent itself never runs `git commit` or `git push`.
- Claude Code may `git commit` and `git push` ONLY after tests pass.

Return ONLY valid JSON that matches the schema exactly.
"""

PLANNER_SCHEMA = {
    "type": "object",
    "additionalProperties": False,
    "properties": {
        "confidence": {"type": "number", "minimum": 0, "maximum": 1},
        "blocking_questions": {"type": "array", "items": {"type": "string"}},
        "plan": {"type": "string"},
        "claude_prompt": {"type": "string"},
        "validation": {"type": "array", "items": {"type": "string"}},
        "risk_notes": {"type": "array", "items": {"type": "string"}},
    },
    "required": ["confidence", "blocking_questions", "plan", "claude_prompt", "validation", "risk_notes"],
}


@dataclass
class PlanPacket:
    confidence: float
    blocking_questions: list[str]
    plan: str
    claude_prompt: str
    validation: list[str]
    risk_notes: list[str]

    @staticmethod
    def from_dict(d: dict[str, Any]) -> "PlanPacket":
        return PlanPacket(
            confidence=float(d["confidence"]),
            blocking_questions=list(d.get("blocking_questions") or []),
            plan=str(d["plan"]),
            claude_prompt=str(d["claude_prompt"]),
            validation=list(d.get("validation") or []),
            risk_notes=list(d.get("risk_notes") or []),
        )


def generate_plan_packet(
    *,
    model: str,
    task: str,
    repo_summary: str,
    extra_context: str = "",
    max_tokens: int = 1800,
) -> PlanPacket:
    client = OpenAI()
    user = {
        "task": task,
        "repo_summary": repo_summary,
        "constraints": [
            "All code edits must be done by Claude Code, not by HermesAgent.",
            "Ask blocking questions instead of guessing.",
            "Validation must include `make test` (or explicitly state why it cannot be run).",
            "Git: Claude Code may `git commit` and `git push` ONLY after tests pass.",
        ],
        "extra_context": extra_context,
    }
    prompt = (
        "Generate a decision-complete plan and a Claude Code prompt to implement it.\n"
        "Set confidence low if important unknowns remain.\n\n"
        f"Input:\n{json.dumps(user, indent=2)}"
    )

    resp = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": PLANNER_SYSTEM},
            {"role": "user", "content": prompt},
        ],
        response_format={
            "type": "json_schema",
            "json_schema": {
                "name": "plan_packet",
                "strict": True,
                "schema": PLANNER_SCHEMA,
            },
        },
        max_tokens=max_tokens,
        temperature=0.2,
    )
    text = resp.choices[0].message.content or "{}"
    data = json.loads(text)
    return PlanPacket.from_dict(data)
