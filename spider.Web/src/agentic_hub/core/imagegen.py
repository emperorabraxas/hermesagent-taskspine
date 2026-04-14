"""Image generation — DALL-E primary, local Stable Diffusion fallback.

Generates images from text prompts. Tries OpenAI DALL-E first,
falls back to local CPU-based Stable Diffusion if no credits.
"""
from __future__ import annotations

import base64
import logging
import time
from pathlib import Path

from agentic_hub.config import get_settings

logger = logging.getLogger(__name__)

OUTPUT_DIR = Path(__file__).parent.parent.parent.parent / "data" / "images"


async def generate_image(prompt: str, size: str = "1024x1024") -> dict:
    """Generate an image. Returns {url, source, time_ms}."""
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    timestamp = int(time.time())
    filename = f"img_{timestamp}.png"
    filepath = OUTPUT_DIR / filename

    # Try DALL-E first
    settings = get_settings()
    if settings.openai_api_key:
        try:
            result = await _dalle(prompt, size, filepath, settings)
            return result
        except Exception as e:
            logger.warning(f"DALL-E failed: {e}")

    # Fallback to local
    try:
        result = await _local_sd(prompt, filepath)
        return result
    except Exception as e:
        logger.error(f"Local image gen failed: {e}")
        return {"error": str(e), "source": "none"}


async def _dalle(prompt: str, size: str, filepath: Path, settings) -> dict:
    """Generate via DALL-E 3."""
    import openai
    client = openai.AsyncOpenAI(api_key=settings.openai_api_key)

    start = time.time()
    response = await client.images.generate(
        model="dall-e-3",
        prompt=prompt,
        size=size,
        quality="standard",
        n=1,
        response_format="b64_json",
    )

    # Save image
    img_data = base64.b64decode(response.data[0].b64_json)
    filepath.write_bytes(img_data)

    elapsed = int((time.time() - start) * 1000)
    return {
        "path": str(filepath),
        "filename": filepath.name,
        "source": "dall-e-3",
        "time_ms": elapsed,
        "revised_prompt": response.data[0].revised_prompt or prompt,
    }


async def _local_sd(prompt: str, filepath: Path) -> dict:
    """Generate via local Stable Diffusion on CPU."""
    import asyncio

    def _generate():
        start = time.time()
        try:
            from diffusers import AutoPipelineForText2Image
            import torch

            pipe = AutoPipelineForText2Image.from_pretrained(
                "stabilityai/sdxl-turbo",
                torch_dtype=torch.float32,
                variant="fp16" if torch.cuda.is_available() else None,
            )
            pipe.to("cpu")

            image = pipe(
                prompt=prompt,
                num_inference_steps=4,  # SDXL Turbo needs only 1-4 steps
                guidance_scale=0.0,     # Turbo doesn't need guidance
            ).images[0]

            image.save(str(filepath))
            elapsed = int((time.time() - start) * 1000)
            return {
                "path": str(filepath),
                "filename": filepath.name,
                "source": "sdxl-turbo-cpu",
                "time_ms": elapsed,
            }
        except ImportError:
            # diffusers not installed — try a simpler approach
            return {"error": "diffusers not installed. Run: pip install diffusers transformers accelerate torch", "source": "none"}

    return await asyncio.to_thread(_generate)
