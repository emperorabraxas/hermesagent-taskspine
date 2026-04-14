"""Multi-agent chains — same model, critic persona, zero GPU swaps.

The primary model answers, then immediately re-runs with a critic prompt
to catch its own mistakes. No model swapping = fast. User only sees
the final refined answer.

Flow (invisible to user):
1. Primary agent answers (model already loaded)
2. Same model critiques with adversarial prompt (no swap!)
3. Same model revises based on critique (no swap!)
4. User sees only the refined answer
"""
from __future__ import annotations

import logging

from agentic_hub.config import get_settings, load_models_config
from agentic_hub.core.ollama_client import get_ollama

logger = logging.getLogger(__name__)

CRITIC_PROMPT = (
    "You are now a harsh critic reviewing your own previous answer. "
    "Forget you wrote it. Attack it.\n"
    "Find: factual errors, missing edge cases, bad assumptions, "
    "oversimplification, or important things missed.\n"
    "List specific problems as bullet points. "
    "If genuinely perfect, say only 'NO ISSUES'."
)

REFINE_PROMPT = (
    "You found issues with your previous answer. Rewrite it to fix them. "
    "Do NOT mention the review — just give the best answer as if it was "
    "your first try. Same format, better content."
)


async def refine_with_review(
    primary_agent: str,
    primary_response: str,
    user_message: str,
) -> str | None:
    """Self-critique chain using the SAME model. Zero GPU swaps."""
    config = load_models_config()
    settings = get_settings()
    ollama = get_ollama()

    # Use the same model that's already loaded — no swap
    agent_cfg = config.get("agents", {}).get(primary_agent, {})
    model = getattr(settings, f"{primary_agent}_model", "") or agent_cfg.get("local_model", "")
    if not model:
        return None

    # Step 1: Self-critique (invisible, same model, no swap)
    logger.info(f"Chain: {primary_agent} self-critiquing (same model, no swap)")

    review = await ollama.chat(
        model=model,
        messages=[
            {"role": "system", "content": CRITIC_PROMPT},
            {"role": "user", "content": (
                f"## Question\n{user_message}\n\n"
                f"## Your previous answer\n{primary_response}"
            )},
        ],
        stream=False,
        keep_alive=settings.model_keep_alive,
    )

    # If no issues, keep original
    if "NO ISSUES" in review.upper() or len(review.strip()) < 20:
        logger.info("Chain: self-critique found no issues")
        return None

    # Step 2: Refine (invisible, same model, no swap)
    logger.info(f"Chain: {primary_agent} refining")

    refined = await ollama.chat(
        model=model,
        messages=[
            {"role": "system", "content": agent_cfg.get("system_prompt", "")},
            {"role": "user", "content": user_message},
            {"role": "assistant", "content": primary_response},
            {"role": "user", "content": f"{REFINE_PROMPT}\n\nIssues found:\n{review}"},
        ],
        stream=False,
        keep_alive=settings.model_keep_alive,
    )

    logger.info("Chain: refined response ready")
    return refined


def should_chain(agent: str, response: str) -> bool:
    """Chain on substantial responses from Scholar or Automator."""
    if agent not in ("scholar", "automator"):
        return False
    if len(response) < 400:
        return False
    return True
