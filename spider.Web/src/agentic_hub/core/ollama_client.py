"""Async HTTP client for the Ollama REST API."""
from __future__ import annotations

import json
import time
from typing import AsyncIterator

import httpx

from agentic_hub.config import get_settings
from agentic_hub.core.tools.llm_response import LLMResponse, ToolCall


def _extract_from_thinking(thinking: str) -> str:
    """Extract usable content from a thinking-mode model's internal reasoning.

    When models like qwen3.5 exhaust their output budget on thinking,
    this extracts the final refined lists/conclusions from the thinking text.
    """
    import re

    # Strategy 1: Look for final refined/polished lists (models often refine multiple times)
    # Find the LAST numbered list in the thinking text
    sections = re.split(r'\n(?=\s*(?:\d+\.|#{1,3}\s|\*\*[A-Z]))', thinking)

    # Find sections that look like final output (numbered lists, headers)
    final_sections = []
    for i, section in enumerate(sections):
        # Prefer later sections (model refines progressively)
        if re.match(r'\s*\d+\.', section) or re.match(r'\s*#{1,3}\s', section):
            final_sections.append(section)

    if final_sections:
        # Take the last chunk of refined content (last ~3000 chars of list content)
        result = "\n".join(final_sections[-10:])
        if len(result) > 100:
            return result.strip()

    # Strategy 2: Extract all "**Bold Title**:" patterns with their descriptions
    bold_items = re.findall(r'\d+\.\s+\*\*([^*]+)\*\*[:\.]?\s*([^\n]+)', thinking)
    if len(bold_items) >= 5:
        # Take the last set of items (most refined)
        items = bold_items[-min(len(bold_items), 20):]
        lines = [f"{i}. **{name.strip()}**: {desc.strip()}" for i, (name, desc) in enumerate(items, 1)]
        return "\n".join(lines)

    # Strategy 3: Last resort — return last 2000 chars of thinking, cleaned up
    tail = thinking[-2000:].strip()
    # Clean up markdown artifacts
    tail = re.sub(r'\s*\.\.\.\s*', ' ', tail)
    return tail if len(tail) > 50 else "(Model produced only internal reasoning — no extractable output)"


class OllamaClient:
    def __init__(self, base_url: str | None = None):
        self.base_url = base_url or get_settings().ollama_base_url
        self._client: httpx.AsyncClient | None = None

    async def _get_client(self) -> httpx.AsyncClient:
        if self._client is None or self._client.is_closed:
            self._client = httpx.AsyncClient(
                base_url=self.base_url,
                # 5 min read timeout — thinking-mode models (qwen3.5) need time
                timeout=httpx.Timeout(connect=10.0, read=300.0, write=10.0, pool=10.0),
            )
        return self._client

    async def close(self):
        if self._client and not self._client.is_closed:
            await self._client.aclose()

    async def chat(
        self,
        model: str,
        messages: list[dict],
        stream: bool = False,
        keep_alive: str = "10m",
        temperature: float = 0.7,
        num_ctx: int = 4096,
        num_predict: int | None = None,
    ) -> str | AsyncIterator[str]:
        """Send a chat completion. Returns full text or async token stream."""
        client = await self._get_client()
        options = {
            "temperature": temperature,
            "num_ctx": num_ctx,
        }
        if num_predict is not None:
            options["num_predict"] = num_predict

        payload = {
            "model": model,
            "messages": messages,
            "stream": stream,
            "keep_alive": keep_alive,
            "options": options,
        }

        if not stream:
            resp = await client.post("/api/chat", json=payload)
            resp.raise_for_status()
            data = resp.json()
            content = data["message"]["content"]
            # Thinking-mode models (qwen3.5, etc.) may return empty content
            # with all output in the "thinking" field. Extract from thinking.
            if not content.strip():
                thinking = data["message"].get("thinking", "")
                if thinking:
                    content = _extract_from_thinking(thinking)
            return content

        return self._stream_chat(client, payload)

    async def _stream_chat(
        self, client: httpx.AsyncClient, payload: dict
    ) -> AsyncIterator[str]:
        """Stream tokens from Ollama chat endpoint."""
        async with client.stream("POST", "/api/chat", json=payload) as resp:
            resp.raise_for_status()
            async for line in resp.aiter_lines():
                if not line:
                    continue
                data = json.loads(line)
                if content := data.get("message", {}).get("content", ""):
                    yield content
                if data.get("done", False):
                    return

    async def chat_completion(
        self,
        model: str,
        messages: list[dict],
        tools: list[dict] | None = None,
        keep_alive: str = "10m",
        temperature: float = 0.7,
        num_ctx: int = 4096,
        num_predict: int | None = None,
    ) -> LLMResponse:
        """Chat with structured response — supports tool calling and returns metadata.

        When tools are provided, Ollama uses native tool calling (OpenAI-compatible format).
        Returns LLMResponse with text, tool_calls, and token counts.
        """
        client = await self._get_client()
        options = {"temperature": temperature, "num_ctx": num_ctx}
        if num_predict is not None:
            options["num_predict"] = num_predict

        payload = {
            "model": model,
            "messages": messages,
            "stream": False,
            "keep_alive": keep_alive,
            "options": options,
        }
        if tools:
            payload["tools"] = tools

        start = time.monotonic()
        resp = await client.post("/api/chat", json=payload)
        resp.raise_for_status()
        data = resp.json()
        elapsed_ms = int((time.monotonic() - start) * 1000)

        msg = data.get("message", {})
        text = msg.get("content", "")

        # Handle thinking-mode models with empty content
        if not text.strip():
            thinking = msg.get("thinking", "")
            if thinking:
                text = _extract_from_thinking(thinking)

        # Parse tool calls from Ollama's native format
        tool_calls = []
        for tc in msg.get("tool_calls", []):
            fn = tc.get("function", {})
            args = fn.get("arguments", {})
            if isinstance(args, str):
                try:
                    args = json.loads(args)
                except json.JSONDecodeError:
                    args = {"raw": args}
            tool_calls.append(ToolCall(
                name=fn.get("name", ""),
                arguments=args,
            ))

        return LLMResponse(
            text=text,
            tool_calls=tool_calls,
            tokens_in=data.get("prompt_eval_count", 0),
            tokens_out=data.get("eval_count", 0),
            model=model,
            provider="ollama",
        )

    async def list_models(self) -> list[dict]:
        """List locally available models."""
        client = await self._get_client()
        resp = await client.get("/api/tags")
        resp.raise_for_status()
        return resp.json().get("models", [])

    async def get_running_models(self) -> list[dict]:
        """Check which models are currently loaded in memory."""
        client = await self._get_client()
        resp = await client.get("/api/ps")
        resp.raise_for_status()
        return resp.json().get("models", [])

    async def pull_model(self, model_name: str) -> AsyncIterator[str]:
        """Pull a model, streaming progress updates."""
        client = await self._get_client()
        payload = {"name": model_name, "stream": True}
        async with client.stream("POST", "/api/pull", json=payload) as resp:
            resp.raise_for_status()
            async for line in resp.aiter_lines():
                if not line:
                    continue
                data = json.loads(line)
                status = data.get("status", "")
                if "completed" in data and "total" in data:
                    pct = int(data["completed"] / data["total"] * 100) if data["total"] else 0
                    yield f"{status} {pct}%"
                else:
                    yield status

    async def embed(self, text: str, model: str = "mxbai-embed-large") -> list[float]:
        """Get embedding vector for text."""
        client = await self._get_client()
        resp = await client.post("/api/embed", json={
            "model": model,
            "input": text,
            "keep_alive": "30s",  # Short TTL — embed model must vacate VRAM for chat models
        })
        resp.raise_for_status()
        data = resp.json()
        # Ollama returns {"embeddings": [[...]]} for single input
        embeddings = data.get("embeddings", [])
        if embeddings and isinstance(embeddings[0], list):
            return embeddings[0]
        return embeddings

    async def unload_model(self, model_name: str) -> None:
        """Unload a model from VRAM by setting keep_alive to 0."""
        client = await self._get_client()
        payload = {
            "model": model_name,
            "messages": [],
            "keep_alive": 0,
        }
        resp = await client.post("/api/chat", json=payload)
        # Some models may return error on empty messages, that's ok
        # The keep_alive=0 still triggers unload

    # ── Generate (raw prompt, no chat format) ─────────────────────

    async def generate(
        self, model: str, prompt: str, system: str = "",
        stream: bool = False, temperature: float = 0.7,
        num_ctx: int = 4096, num_predict: int | None = None,
        images: list[str] | None = None,
        format_schema: str | dict | None = None,
    ) -> str | AsyncIterator[str]:
        """Raw text generation from a prompt (not chat format).

        Supports: images (vision), format (JSON/schema), streaming.
        """
        client = await self._get_client()
        options = {"temperature": temperature, "num_ctx": num_ctx}
        if num_predict is not None:
            options["num_predict"] = num_predict

        payload: dict = {
            "model": model, "prompt": prompt, "stream": stream,
            "options": options,
        }
        if system:
            payload["system"] = system
        if images:
            payload["images"] = images
        if format_schema:
            payload["format"] = format_schema

        if not stream:
            resp = await client.post("/api/generate", json=payload)
            resp.raise_for_status()
            return resp.json().get("response", "")
        return self._stream_generate(client, payload)

    async def _stream_generate(
        self, client: httpx.AsyncClient, payload: dict,
    ) -> AsyncIterator[str]:
        """Stream tokens from /api/generate."""
        async with client.stream("POST", "/api/generate", json=payload) as resp:
            resp.raise_for_status()
            async for line in resp.aiter_lines():
                if not line:
                    continue
                data = json.loads(line)
                if token := data.get("response", ""):
                    yield token
                if data.get("done", False):
                    return

    # ── Vision / Image Analysis ───────────────────────────────────
    # Spider: Scholar, Zero — analyze images with local models

    async def vision(
        self, model: str, prompt: str, images: list[str],
        temperature: float = 0.3, num_ctx: int = 4096,
    ) -> str:
        """Analyze images with a vision-capable model (e.g., gemma3, llava).

        images: list of base64-encoded image strings or file paths.
        """
        client = await self._get_client()
        payload = {
            "model": model, "stream": False,
            "messages": [{
                "role": "user",
                "content": prompt,
                "images": images,
            }],
            "options": {"temperature": temperature, "num_ctx": num_ctx},
        }
        resp = await client.post("/api/chat", json=payload)
        resp.raise_for_status()
        return resp.json().get("message", {}).get("content", "")

    # ── Structured Output ─────────────────────────────────────────
    # Spider: Router (JSON classification), ALL spiders

    async def structured_output(
        self, model: str, messages: list[dict], schema: dict | str = "json",
        temperature: float = 0.3, num_ctx: int = 4096,
    ) -> dict:
        """Get guaranteed JSON output from a local model.

        schema: "json" for free-form JSON, or a JSON schema dict for strict structure.
        Pydantic .model_json_schema() works directly.
        """
        client = await self._get_client()
        payload = {
            "model": model, "messages": messages, "stream": False,
            "format": schema,
            "options": {"temperature": temperature, "num_ctx": num_ctx},
        }
        resp = await client.post("/api/chat", json=payload)
        resp.raise_for_status()
        text = resp.json().get("message", {}).get("content", "{}")
        return json.loads(text)

    # ── Thinking Mode ─────────────────────────────────────────────
    # Spider: Proxy (deep reasoning), Exploit (strategy)

    async def think(
        self, model: str, messages: list[dict],
        temperature: float = 0.7, num_ctx: int = 8192,
    ) -> dict:
        """Chat with thinking mode enabled — model shows chain-of-thought.

        Returns: {"thinking": "...", "content": "...", "tokens_in": N, "tokens_out": N}
        Compatible with qwen3, qwen3.5, deepseek-r1, and other thinking models.
        """
        client = await self._get_client()
        payload = {
            "model": model, "messages": messages, "stream": False,
            "think": True,
            "options": {"temperature": temperature, "num_ctx": num_ctx},
        }
        resp = await client.post("/api/chat", json=payload)
        resp.raise_for_status()
        data = resp.json()
        msg = data.get("message", {})
        return {
            "thinking": msg.get("thinking", ""),
            "content": msg.get("content", ""),
            "tokens_in": data.get("prompt_eval_count", 0),
            "tokens_out": data.get("eval_count", 0),
        }

    # ── Show Model Info ───────────────────────────────────────────

    async def show_model(self, model_name: str) -> dict:
        """Get detailed model info: parameters, architecture, context length, license."""
        client = await self._get_client()
        resp = await client.post("/api/show", json={"name": model_name})
        resp.raise_for_status()
        return resp.json()

    # ── Create Model (from Modelfile) ─────────────────────────────

    async def create_model(
        self, name: str, modelfile: str, stream: bool = False,
    ) -> str | AsyncIterator[str]:
        """Create a new model from a Modelfile definition.

        Modelfile example:
            FROM llama3.2
            PARAMETER temperature 0.8
            SYSTEM You are a helpful assistant.
        """
        client = await self._get_client()
        payload = {"name": name, "modelfile": modelfile, "stream": stream}
        if not stream:
            resp = await client.post("/api/create", json=payload)
            resp.raise_for_status()
            return resp.json().get("status", "success")
        return self._stream_create(client, payload)

    async def _stream_create(
        self, client: httpx.AsyncClient, payload: dict,
    ) -> AsyncIterator[str]:
        """Stream model creation progress."""
        async with client.stream("POST", "/api/create", json=payload) as resp:
            resp.raise_for_status()
            async for line in resp.aiter_lines():
                if not line:
                    continue
                data = json.loads(line)
                yield data.get("status", "")

    # ── Copy Model ────────────────────────────────────────────────

    async def copy_model(self, source: str, destination: str) -> bool:
        """Copy/clone a model to a new name."""
        client = await self._get_client()
        resp = await client.post("/api/copy", json={
            "source": source, "destination": destination,
        })
        return resp.status_code == 200

    # ── Delete Model ──────────────────────────────────────────────

    async def delete_model(self, model_name: str) -> bool:
        """Delete a model from the local system."""
        client = await self._get_client()
        resp = await client.request("DELETE", "/api/delete", json={"name": model_name})
        return resp.status_code == 200

    # ── Push Model ────────────────────────────────────────────────

    async def push_model(self, model_name: str, stream: bool = False) -> str | AsyncIterator[str]:
        """Push a model to the Ollama registry."""
        client = await self._get_client()
        payload = {"name": model_name, "stream": stream}
        if not stream:
            resp = await client.post("/api/push", json=payload)
            resp.raise_for_status()
            return resp.json().get("status", "success")
        return self._stream_push(client, payload)

    async def _stream_push(
        self, client: httpx.AsyncClient, payload: dict,
    ) -> AsyncIterator[str]:
        """Stream push progress."""
        async with client.stream("POST", "/api/push", json=payload) as resp:
            resp.raise_for_status()
            async for line in resp.aiter_lines():
                if not line:
                    continue
                data = json.loads(line)
                status = data.get("status", "")
                if "completed" in data and "total" in data:
                    pct = int(data["completed"] / data["total"] * 100) if data["total"] else 0
                    yield f"{status} {pct}%"
                else:
                    yield status

    # ── Batch Embed ───────────────────────────────────────────────

    async def embed_batch(
        self, texts: list[str], model: str = "mxbai-embed-large",
    ) -> list[list[float]]:
        """Get embeddings for multiple texts in one call."""
        client = await self._get_client()
        resp = await client.post("/api/embed", json={
            "model": model, "input": texts,
            "keep_alive": "30s",  # Short TTL — embed model must vacate VRAM for chat models
        })
        resp.raise_for_status()
        return resp.json().get("embeddings", [])


# Singleton
_ollama: OllamaClient | None = None


def get_ollama() -> OllamaClient:
    global _ollama
    if _ollama is None:
        _ollama = OllamaClient()
    return _ollama
