"""Model pricing — cost calculation for cloud API usage."""
from __future__ import annotations

# Pricing per 1M tokens (input, output) in USD
# Updated April 2026
MODEL_PRICING: dict[str, tuple[float, float]] = {
    # Anthropic
    "claude-opus-4-6-20250819": (15.0, 75.0),
    "claude-sonnet-4-6": (3.0, 15.0),
    "claude-haiku-4-5": (0.80, 4.0),
    # OpenAI
    "gpt-5.4": (2.0, 8.0),
    "gpt-4.1": (2.0, 8.0),
    # Google
    "gemini-3.1-pro": (1.25, 5.0),
    "gemini-2.5-pro": (1.25, 5.0),
    # DeepSeek
    "deepseek-v3.2": (0.14, 0.28),
    "deepseek-chat": (0.14, 0.28),
    # xAI
    "grok-4.20": (2.0, 6.0),
    "grok-3": (3.0, 15.0),
}


def calculate_cost(model: str, tokens_in: int, tokens_out: int) -> float:
    """Calculate cost in USD for a given model and token counts.

    Returns 0.0 for local/unknown models (Ollama models are free).
    """
    # Ollama local models are free — identified by ":" (tag separator) or "/" (namespace)
    if ":" in model or "/" in model:
        return 0.0

    pricing = MODEL_PRICING.get(model)
    if not pricing:
        # Check partial match (e.g., "claude-opus-4" matches "claude-opus-4-6-20250819")
        for key, val in MODEL_PRICING.items():
            if model.startswith(key.rsplit("-", 1)[0]) or key.startswith(model.rsplit("-", 1)[0]):
                pricing = val
                break
    if not pricing:
        return 0.0  # Local model or unknown = free

    input_cost_per_token = pricing[0] / 1_000_000
    output_cost_per_token = pricing[1] / 1_000_000
    return (tokens_in * input_cost_per_token) + (tokens_out * output_cost_per_token)
