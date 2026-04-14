"""Cloud API wrappers for Anthropic (Claude), OpenAI (GPT), DeepSeek, Google (Gemini), and xAI (Grok)."""
from __future__ import annotations

import json as _json
import logging
from typing import AsyncIterator

import anthropic
import openai

from agentic_hub.config import get_settings
from agentic_hub.core.tools.llm_response import LLMResponse, ToolCall

logger = logging.getLogger(__name__)


class AnthropicClient:
    """Full Anthropic Claude API integration — all capabilities (26/26).

    Features:
      - Messages: create, stream, tool calling
      - Extended thinking + interleaved thinking
      - Prompt caching with extended TTL
      - Message batches (50% cost)
      - Web search + web fetch (server tools)
      - Code execution (sandboxed)
      - Computer use + bash tool + text editor tool
      - Vision (images — base64, URL, file)
      - PDF document analysis
      - Citations (source attribution)
      - Files API (upload, reference)
      - MCP connectors (external tool servers)
      - Structured JSON output
      - Token counting
      - Model listing
      - Classification
      - Context management + 1M context
      - Fast mode

    Spider allocation:
      - chat/structured_output → ALL
      - vision/pdf/citations → Scholar, Zero
      - code_execution → Payload (Compiler)
      - computer_use/bash/text_editor → Cron (Automator)
      - web_search/web_fetch → Scholar
      - mcp → Root (Orchestrator)
      - thinking → Proxy, Exploit
      - batches → Cron
      - files → ALL
    """

    def __init__(self):
        settings = get_settings()
        self._client = anthropic.AsyncAnthropic(api_key=settings.anthropic_api_key)

    # ── Basic Chat ─────────────────────────────────────────────────

    async def chat(
        self,
        messages: list[dict],
        model: str = "claude-opus-4-6-20250819",
        system: str = "",
        max_tokens: int = 4096,
        temperature: float = 0.7,
        stream: bool = False,
    ) -> str | AsyncIterator[str]:
        """Send a chat completion to Claude."""
        kwargs = {
            "model": model,
            "max_tokens": max_tokens,
            "temperature": temperature,
            "messages": messages,
        }
        if system:
            kwargs["system"] = system

        if not stream:
            resp = await self._client.messages.create(**kwargs)
            return resp.content[0].text

        return self._stream(kwargs)

    async def _stream(self, kwargs: dict) -> AsyncIterator[str]:
        async with self._client.messages.stream(**kwargs) as stream:
            async for text in stream.text_stream:
                yield text

    # ── Chat Completion (structured response + tools) ──────────────

    async def chat_completion(
        self,
        messages: list[dict],
        model: str = "claude-opus-4-6-20250819",
        system: str = "",
        tools: list[dict] | None = None,
        max_tokens: int = 4096,
        temperature: float = 0.7,
        thinking: bool = False,
        cache_system: bool = False,
    ) -> LLMResponse:
        """Chat with structured response — tools, thinking, caching.

        Args:
            thinking: Enable extended thinking (Claude reasons before responding)
            cache_system: Cache the system prompt for repeated use (saves tokens)
        """
        kwargs = {
            "model": model,
            "max_tokens": max_tokens,
            "messages": messages,
        }

        # System prompt with optional caching
        if system:
            if cache_system:
                kwargs["system"] = [
                    {"type": "text", "text": system, "cache_control": {"type": "ephemeral"}}
                ]
            else:
                kwargs["system"] = system

        if tools:
            kwargs["tools"] = tools

        # Extended thinking
        if thinking:
            kwargs["thinking"] = {"type": "enabled", "budget_tokens": min(max_tokens // 2, 8000)}
            # Thinking requires temperature=1
            kwargs["temperature"] = 1
        else:
            kwargs["temperature"] = temperature

        resp = await self._client.messages.create(**kwargs)

        text_parts = []
        thinking_parts = []
        tool_calls = []
        for block in resp.content:
            if block.type == "text":
                text_parts.append(block.text)
            elif block.type == "thinking":
                thinking_parts.append(block.thinking)
            elif block.type == "tool_use":
                tool_calls.append(ToolCall(
                    name=block.name,
                    arguments=block.input if isinstance(block.input, dict) else {},
                    call_id=block.id,
                ))

        text = "\n".join(text_parts)
        thinking_text = "\n".join(thinking_parts)

        return LLMResponse(
            text=text,
            thinking=thinking_text,
            tool_calls=tool_calls,
            tokens_in=resp.usage.input_tokens if resp.usage else 0,
            tokens_out=resp.usage.output_tokens if resp.usage else 0,
            model=model,
            provider="anthropic",
        )

    # ── Extended Thinking ──────────────────────────────────────────

    async def think_and_respond(
        self,
        messages: list[dict],
        model: str = "claude-opus-4-6-20250819",
        system: str = "",
        max_tokens: int = 16000,
        thinking_budget: int = 8000,
    ) -> dict:
        """Extended thinking — Claude reasons internally, then responds.

        Returns: {"thinking": "...", "response": "...", "tokens_in": N, "tokens_out": N}
        """
        kwargs = {
            "model": model,
            "max_tokens": max_tokens,
            "temperature": 1,  # Required for thinking
            "messages": messages,
            "thinking": {"type": "enabled", "budget_tokens": thinking_budget},
        }
        if system:
            kwargs["system"] = system

        resp = await self._client.messages.create(**kwargs)

        thinking = ""
        response = ""
        for block in resp.content:
            if block.type == "thinking":
                thinking += block.thinking
            elif block.type == "text":
                response += block.text

        return {
            "thinking": thinking,
            "response": response,
            "tokens_in": resp.usage.input_tokens if resp.usage else 0,
            "tokens_out": resp.usage.output_tokens if resp.usage else 0,
        }

    # ── Web Search ─────────────────────────────────────────────────

    async def web_search(
        self,
        query: str,
        model: str = "claude-sonnet-4-6-20250514",
        system: str = "",
        max_tokens: int = 4096,
    ) -> str:
        """Use Claude's built-in web search tool.

        Claude searches the web and responds with cited results.
        """
        kwargs = {
            "model": model,
            "max_tokens": max_tokens,
            "messages": [{"role": "user", "content": query}],
            "tools": [{"type": "web_search_20250305"}],
        }
        if system:
            kwargs["system"] = system

        resp = await self._client.messages.create(**kwargs)

        # Extract text from response (may include citations)
        text_parts = []
        for block in resp.content:
            if block.type == "text":
                text_parts.append(block.text)
        return "\n".join(text_parts) or "No results"

    # ── Token Counting ─────────────────────────────────────────────

    async def count_tokens(
        self,
        messages: list[dict],
        model: str = "claude-opus-4-6-20250819",
        system: str = "",
        tools: list[dict] | None = None,
    ) -> int:
        """Count tokens for a message without sending it. Returns token count."""
        kwargs = {
            "model": model,
            "messages": messages,
        }
        if system:
            kwargs["system"] = system
        if tools:
            kwargs["tools"] = tools

        result = await self._client.messages.count_tokens(**kwargs)
        return result.input_tokens

    # ── Model Listing ──────────────────────────────────────────────

    async def list_models(self) -> list[dict]:
        """List all available Claude models."""
        try:
            result = await self._client.models.list()
            return [
                {
                    "id": m.id,
                    "name": m.display_name if hasattr(m, 'display_name') else m.id,
                    "created": str(m.created_at) if hasattr(m, 'created_at') else "",
                }
                for m in result.data
            ]
        except Exception as e:
            logger.warning(f"Model listing failed: {e}")
            return []

    # ── Batches API ────────────────────────────────────────────────

    async def create_batch(self, requests: list[dict]) -> dict:
        """Create a batch of message requests (50% cost discount).

        Each request: {"custom_id": "...", "params": {messages, model, max_tokens, ...}}
        """
        try:
            batch = await self._client.messages.batches.create(
                requests=[
                    {
                        "custom_id": r.get("custom_id", f"req_{i}"),
                        "params": r.get("params", r),
                    }
                    for i, r in enumerate(requests)
                ]
            )
            return {
                "batch_id": batch.id,
                "status": batch.processing_status,
                "counts": {
                    "total": batch.request_counts.total if batch.request_counts else 0,
                    "processing": batch.request_counts.processing if batch.request_counts else 0,
                },
            }
        except Exception as e:
            return {"error": str(e)}

    async def get_batch(self, batch_id: str) -> dict:
        """Check status of a batch."""
        try:
            batch = await self._client.messages.batches.retrieve(batch_id)
            return {
                "batch_id": batch.id,
                "status": batch.processing_status,
                "counts": {
                    "total": batch.request_counts.total if batch.request_counts else 0,
                    "succeeded": batch.request_counts.succeeded if batch.request_counts else 0,
                    "errored": batch.request_counts.errored if batch.request_counts else 0,
                },
            }
        except Exception as e:
            return {"error": str(e)}

    # ── Classifier ─────────────────────────────────────────────────

    async def classify(
        self,
        user_input: str,
        conversation_context: list[dict] | None = None,
    ) -> dict:
        """Use Opus as a lightweight classifier. Returns routing decision."""
        system_prompt = """You are a task router. Classify the user's request into exactly ONE category.
Return ONLY a JSON object with these fields:
- "route": one of "code", "research", "automate", "chat", "direct"
- "reason": one sentence explaining why
- "complexity": "low", "medium", or "high"

Route definitions:
- "code": Writing, editing, debugging, refactoring, or reviewing code
- "research": Looking up information, summarizing documents, analyzing data, answering factual questions
- "automate": Git operations, file management, shell commands, DevOps tasks, system administration
- "chat": General conversation, brainstorming, creative writing, thinking through problems
- "direct": Simple clarifications, greetings, or meta-questions about this system

Return ONLY valid JSON, no markdown fences."""

        messages = []
        if conversation_context:
            messages.extend(conversation_context[-2:])
        messages.append({"role": "user", "content": user_input})

        resp = await self._client.messages.create(
            model="claude-opus-4-6-20250819",
            max_tokens=256,
            temperature=0.0,
            system=system_prompt,
            messages=messages,
        )

        import json
        text = resp.content[0].text.strip()
        if text.startswith("```"):
            text = text.split("\n", 1)[1].rsplit("```", 1)[0].strip()
        return json.loads(text)

    # ── Vision (Image Analysis) ───────────────────────────────────
    # Spider: Scholar (screenshots/charts), Zero (experiments)

    async def vision(
        self, prompt: str, image_data: str, media_type: str = "image/jpeg",
        source_type: str = "base64", model: str = "claude-opus-4-6-20250819",
        max_tokens: int = 1024,
    ) -> str:
        """Analyze an image. source_type: 'base64', 'url', or 'file'."""
        if source_type == "url":
            source = {"type": "url", "url": image_data}
        elif source_type == "file":
            source = {"type": "file", "file_id": image_data}
        else:
            source = {"type": "base64", "media_type": media_type, "data": image_data}
        resp = await self._client.messages.create(
            model=model, max_tokens=max_tokens,
            messages=[{"role": "user", "content": [
                {"type": "image", "source": source},
                {"type": "text", "text": prompt},
            ]}],
        )
        return resp.content[0].text

    # ── PDF Analysis ──────────────────────────────────────────────
    # Spider: Scholar (document research), Proxy (reasoning over docs)

    async def analyze_pdf(
        self, prompt: str, pdf_data: str,
        source_type: str = "base64",
        model: str = "claude-opus-4-6-20250819", max_tokens: int = 4096,
        citations: bool = True,
    ) -> dict:
        """Analyze a PDF document with optional citations.

        source_type: 'base64' (raw data), 'url' (web URL), or 'file' (file_id from Files API)
        """
        if source_type == "url":
            source = {"type": "url", "url": pdf_data}
        elif source_type == "file":
            source = {"type": "file", "file_id": pdf_data}
        else:
            source = {"type": "base64", "media_type": "application/pdf", "data": pdf_data}
        content = [
            {"type": "document", "source": source},
            {"type": "text", "text": prompt},
        ]
        if citations:
            content[0]["citations"] = {"enabled": True}
        resp = await self._client.messages.create(
            model=model, max_tokens=max_tokens,
            messages=[{"role": "user", "content": content}],
        )
        result = {"text": "", "citations": []}
        for block in resp.content:
            if block.type == "text":
                result["text"] += block.text
                if hasattr(block, 'citations') and block.citations:
                    result["citations"].extend([vars(c) if hasattr(c, '__dict__') else c for c in block.citations])
        return result

    # ── Files API ─────────────────────────────────────────────────
    # Spider: ALL — upload and reference documents

    async def upload_file(self, file_path: str) -> str:
        """Upload a file to Anthropic. Returns file ID."""
        with open(file_path, "rb") as f:
            resp = await self._client.files.create(file=f)
        return resp.id

    async def list_files(self) -> list[dict]:
        """List uploaded files."""
        resp = await self._client.files.list()
        return [{"id": f.id, "filename": getattr(f, 'filename', ''), "size": getattr(f, 'size_bytes', 0)} for f in resp.data]

    async def delete_file(self, file_id: str) -> bool:
        """Delete a file."""
        await self._client.files.delete(file_id)
        return True

    # ── Code Execution ────────────────────────────────────────────
    # Spider: Payload (Compiler) — sandboxed code running

    async def code_execute(
        self, prompt: str, model: str = "claude-opus-4-6-20250819",
        max_tokens: int = 8192, system: str = "",
    ) -> dict:
        """Execute code in Claude's sandboxed environment."""
        kwargs = {
            "model": model, "max_tokens": max_tokens,
            "messages": [{"role": "user", "content": prompt}],
            "tools": [{"type": "code_execution_20250522"}],
            "betas": ["code-execution-2025-05-22"],
        }
        if system:
            kwargs["system"] = system
        resp = await self._client.messages.create(**kwargs)
        result = {"text": "", "code": "", "output": ""}
        for block in resp.content:
            if block.type == "text":
                result["text"] += block.text
            elif block.type == "server_tool_use" and getattr(block, 'name', '') == 'code_execution':
                result["code"] += str(getattr(block, 'input', ''))
        return result

    # ── Computer Use ──────────────────────────────────────────────
    # Spider: Cron (Automator) — autonomous computer control

    async def computer_use(
        self, prompt: str, display_width: int = 1920, display_height: int = 1080,
        model: str = "claude-opus-4-6-20250819", max_tokens: int = 4096,
    ) -> dict:
        """Enable computer use — Claude can control mouse, keyboard, screen."""
        resp = await self._client.messages.create(
            model=model, max_tokens=max_tokens,
            messages=[{"role": "user", "content": prompt}],
            tools=[
                {"type": "computer_20251124", "name": "computer", "display_width_px": display_width, "display_height_px": display_height},
                {"type": "bash_20250124", "name": "bash"},
                {"type": "text_editor_20250728", "name": "str_replace_based_edit_tool"},
            ],
            betas=["computer-use-2025-11-24"],
        )
        actions = []
        text = ""
        for block in resp.content:
            if block.type == "text":
                text += block.text
            elif block.type == "tool_use":
                actions.append({"tool": block.name, "input": block.input, "id": block.id})
        return {"text": text, "actions": actions}

    # ── Web Fetch ─────────────────────────────────────────────────
    # Spider: Scholar — fetch and analyze web pages

    async def web_fetch(
        self, url: str, prompt: str = "Summarize this page.",
        model: str = "claude-sonnet-4-6-20250514", max_tokens: int = 4096,
    ) -> str:
        """Fetch a URL and analyze its content."""
        resp = await self._client.messages.create(
            model=model, max_tokens=max_tokens,
            messages=[{"role": "user", "content": f"{prompt}\n\nURL: {url}"}],
            tools=[{"type": "web_fetch_20250305"}],
        )
        text_parts = []
        for block in resp.content:
            if block.type == "text":
                text_parts.append(block.text)
        return "\n".join(text_parts) or "No content fetched"

    # ── Structured JSON Output ────────────────────────────────────
    # Spider: Router (classification), ALL spiders

    async def structured_output(
        self, messages: list[dict], schema: dict,
        model: str = "claude-opus-4-6-20250819", system: str = "",
        max_tokens: int = 4096, temperature: float = 0.3,
    ) -> dict:
        """Get guaranteed JSON output matching a schema.

        Uses tool calling with a single tool whose input_schema IS the desired schema.
        Claude is forced to return structured data matching the schema.
        """
        tool_name = "structured_response"
        resp = await self._client.messages.create(
            model=model, max_tokens=max_tokens, temperature=temperature,
            messages=messages,
            system=system or "Respond using the structured_response tool with the requested data.",
            tools=[{"name": tool_name, "description": "Return structured data", "input_schema": schema}],
            tool_choice={"type": "tool", "name": tool_name},
        )
        for block in resp.content:
            if block.type == "tool_use" and block.name == tool_name:
                return block.input if isinstance(block.input, dict) else {}
        return {}

    # ── MCP Connectors ────────────────────────────────────────────
    # Spider: Root (Orchestrator) — connect to external tool servers

    async def with_mcp(
        self, messages: list[dict], mcp_servers: list[dict],
        model: str = "claude-opus-4-6-20250819", max_tokens: int = 4096,
        system: str = "",
    ) -> LLMResponse:
        """Send a message with MCP server connections.

        mcp_servers: [{"url": "https://...", "name": "server_name", "tool_configuration": {"allowed_tools": [...]}}]
        """
        kwargs = {
            "model": model, "max_tokens": max_tokens,
            "messages": messages, "mcp_servers": mcp_servers,
            "betas": ["mcp-client-2025-04-04"],
        }
        if system:
            kwargs["system"] = system
        resp = await self._client.messages.create(**kwargs)
        text_parts = []
        tool_calls = []
        for block in resp.content:
            if block.type == "text":
                text_parts.append(block.text)
            elif block.type == "tool_use":
                tool_calls.append(ToolCall(name=block.name, arguments=block.input if isinstance(block.input, dict) else {}, call_id=block.id))
        return LLMResponse(
            text="\n".join(text_parts), tool_calls=tool_calls,
            tokens_in=resp.usage.input_tokens if resp.usage else 0,
            tokens_out=resp.usage.output_tokens if resp.usage else 0,
            model=model, provider="anthropic",
        )

    # ── Interleaved Thinking ──────────────────────────────────────
    # Spider: Proxy (Oracle), Exploit — thinking woven into response

    async def interleaved_think(
        self, messages: list[dict], model: str = "claude-opus-4-6-20250819",
        system: str = "", max_tokens: int = 16000, thinking_budget: int = 10000,
    ) -> dict:
        """Interleaved thinking — thoughts woven throughout the response."""
        kwargs = {
            "model": model, "max_tokens": max_tokens, "temperature": 1,
            "messages": messages,
            "thinking": {"type": "enabled", "budget_tokens": thinking_budget},
            "betas": ["interleaved-thinking-2025-05-14"],
        }
        if system:
            kwargs["system"] = system
        resp = await self._client.messages.create(**kwargs)
        parts = []
        for block in resp.content:
            if block.type == "thinking":
                parts.append({"type": "thinking", "text": block.thinking})
            elif block.type == "text":
                parts.append({"type": "text", "text": block.text})
        return {"parts": parts, "tokens_in": resp.usage.input_tokens if resp.usage else 0, "tokens_out": resp.usage.output_tokens if resp.usage else 0}

    # ── Extended Cache TTL ────────────────────────────────────────

    async def chat_with_extended_cache(
        self, messages: list[dict], system: str,
        model: str = "claude-opus-4-6-20250819", max_tokens: int = 4096,
        cache_ttl: str = "1h",
    ) -> str:
        """Chat with extended prompt cache TTL (up to 1 hour)."""
        resp = await self._client.messages.create(
            model=model, max_tokens=max_tokens, temperature=0.7,
            messages=messages,
            system=[{"type": "text", "text": system, "cache_control": {"type": "ephemeral", "ttl": cache_ttl}}],
            betas=["extended-cache-ttl-2025-04-11"],
        )
        return resp.content[0].text

    # ── Fast Mode ─────────────────────────────────────────────────
    # Spider: Router — low-latency classification

    async def fast_chat(
        self, messages: list[dict], model: str = "claude-haiku-4-5-20251001",
        system: str = "", max_tokens: int = 1024,
    ) -> str:
        """Fast mode — optimized for low latency responses."""
        kwargs = {
            "model": model, "max_tokens": max_tokens, "temperature": 0.3,
            "messages": messages,
            "betas": ["fast-mode-2026-02-01"],
        }
        if system:
            kwargs["system"] = system
        resp = await self._client.messages.create(**kwargs)
        return resp.content[0].text

    # ── Context Management ────────────────────────────────────────

    async def chat_1m(
        self, messages: list[dict], model: str = "claude-opus-4-6-20250819",
        system: str = "", max_tokens: int = 8192,
    ) -> str:
        """Chat with 1M token context window."""
        kwargs = {
            "model": model, "max_tokens": max_tokens, "temperature": 0.7,
            "messages": messages,
            "betas": ["context-1m-2025-08-07"],
        }
        if system:
            kwargs["system"] = system
        resp = await self._client.messages.create(**kwargs)
        return resp.content[0].text


class OpenAIClient:
    """Full OpenAI API integration — all capabilities.

    Features:
    - Chat Completions (streaming + non-streaming)
    - Function/Tool Calling
    - Structured Outputs (json_schema response_format)
    - Vision (image input analysis)
    - Embeddings (text-embedding-3-small/large)
    - Image Generation (gpt-image-1 / dall-e-3)
    - Text-to-Speech (gpt-4o-mini-tts)
    - Speech-to-Text / Whisper (whisper-1)
    - Moderation (omni-moderation-latest)

    Spider allocation:
    - chat/chat_completion/structured_output → ALL spiders
    - vision → Scholar (Scraper), Zero (Lab)
    - embeddings → Scholar (Scraper), semantic cache
    - image_generation → Wolf (Money Maker), Zero (Lab)
    - tts → Root (Orchestrator)
    - transcribe → Scholar (Scraper)
    - moderate → Root (Orchestrator) — safety filter on all outputs
    """

    _provider_name: str = "openai"

    def __init__(self):
        settings = get_settings()
        self._client = openai.AsyncOpenAI(api_key=settings.openai_api_key)

    # ── Chat Completions ─────────────────────────────────────────

    async def chat(
        self,
        messages: list[dict],
        model: str = "gpt-5.4",
        max_tokens: int = 4096,
        temperature: float = 0.7,
        stream: bool = False,
    ) -> str | AsyncIterator[str]:
        """Send a chat completion. Returns str or async token iterator."""
        kwargs = {
            "model": model,
            "max_tokens": max_tokens,
            "temperature": temperature,
            "messages": messages,
        }
        if not stream:
            resp = await self._client.chat.completions.create(**kwargs)
            return resp.choices[0].message.content
        return self._stream(kwargs)

    async def chat_completion(
        self,
        messages: list[dict],
        model: str = "gpt-5.4",
        tools: list[dict] | None = None,
        max_tokens: int = 4096,
        temperature: float = 0.7,
    ) -> LLMResponse:
        """Chat with structured response — supports tool calling."""
        kwargs = {
            "model": model,
            "max_tokens": max_tokens,
            "temperature": temperature,
            "messages": messages,
        }
        if tools:
            kwargs["tools"] = tools

        resp = await self._client.chat.completions.create(**kwargs)
        msg = resp.choices[0].message

        tool_calls = []
        if msg.tool_calls:
            for tc in msg.tool_calls:
                args = tc.function.arguments
                if isinstance(args, str):
                    try:
                        args = _json.loads(args)
                    except _json.JSONDecodeError:
                        args = {"raw": args}
                tool_calls.append(ToolCall(
                    name=tc.function.name,
                    arguments=args,
                    call_id=tc.id or "",
                ))

        return LLMResponse(
            text=msg.content or "",
            tool_calls=tool_calls,
            tokens_in=resp.usage.prompt_tokens if resp.usage else 0,
            tokens_out=resp.usage.completion_tokens if resp.usage else 0,
            model=model,
            provider=self._provider_name,
        )

    async def _stream(self, kwargs: dict) -> AsyncIterator[str]:
        kwargs["stream"] = True
        stream = await self._client.chat.completions.create(**kwargs)
        async for chunk in stream:
            if chunk.choices and chunk.choices[0].delta.content:
                yield chunk.choices[0].delta.content

    # ── Structured Outputs ───────────────────────────────────────
    # Spider: Router (guaranteed JSON classification), ALL spiders

    async def structured_output(
        self,
        messages: list[dict],
        schema: dict,
        model: str = "gpt-5.4",
        schema_name: str = "response",
        max_tokens: int = 4096,
        temperature: float = 0.3,
    ) -> dict:
        """Chat completion with guaranteed JSON output matching a schema.

        Uses response_format=json_schema to enforce structure.
        No more regex parsing — the model MUST return valid JSON matching the schema.
        """
        resp = await self._client.chat.completions.create(
            model=model,
            max_tokens=max_tokens,
            temperature=temperature,
            messages=messages,
            response_format={
                "type": "json_schema",
                "json_schema": {
                    "name": schema_name,
                    "strict": True,
                    "schema": schema,
                },
            },
        )
        text = resp.choices[0].message.content or "{}"
        return _json.loads(text)

    # ── Vision ───────────────────────────────────────────────────
    # Spider: Scholar (analyze screenshots/charts), Zero (experiments)

    async def vision(
        self,
        prompt: str,
        image_url: str,
        model: str = "gpt-5.4",
        max_tokens: int = 1024,
    ) -> str:
        """Analyze an image with a text prompt. Accepts URL or base64 data URI.

        Use for: screenshot analysis, chart reading, visual data extraction.
        """
        resp = await self._client.chat.completions.create(
            model=model,
            max_tokens=max_tokens,
            messages=[{
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {"type": "image_url", "image_url": {"url": image_url}},
                ],
            }],
        )
        return resp.choices[0].message.content or ""

    async def vision_multi(
        self,
        prompt: str,
        image_urls: list[str],
        model: str = "gpt-5.4",
        max_tokens: int = 2048,
    ) -> str:
        """Analyze multiple images with a single prompt."""
        content: list[dict] = [{"type": "text", "text": prompt}]
        for url in image_urls:
            content.append({"type": "image_url", "image_url": {"url": url}})
        resp = await self._client.chat.completions.create(
            model=model,
            max_tokens=max_tokens,
            messages=[{"role": "user", "content": content}],
        )
        return resp.choices[0].message.content or ""

    # ── Embeddings ───────────────────────────────────────────────
    # Spider: Scholar (semantic search), semantic cache system

    async def embed(
        self,
        text: str | list[str],
        model: str = "text-embedding-3-small",
        dimensions: int | None = None,
    ) -> list[list[float]]:
        """Generate vector embeddings for text(s).

        Returns list of float vectors. Use for:
        - Semantic similarity search
        - Semantic caching (compare query vectors)
        - Document clustering and retrieval
        """
        kwargs: dict = {"model": model, "input": text, "encoding_format": "float"}
        if dimensions:
            kwargs["dimensions"] = dimensions
        resp = await self._client.embeddings.create(**kwargs)
        return [item.embedding for item in resp.data]

    # ── Image Generation ─────────────────────────────────────────
    # Spider: Wolf (product images for revenue), Zero (experiments)

    async def generate_image(
        self,
        prompt: str,
        model: str = "gpt-image-1",
        size: str = "1024x1024",
        quality: str = "auto",
        n: int = 1,
        style: str = "vivid",
        response_format: str = "url",
    ) -> list[str]:
        """Generate images from a text prompt.

        Returns list of URLs or base64 strings.
        Models: gpt-image-1 (best), dall-e-3
        Sizes: 1024x1024, 1024x1536, 1536x1024, auto
        """
        resp = await self._client.images.generate(
            model=model,
            prompt=prompt,
            n=n,
            size=size,
            quality=quality,
            style=style,
            response_format=response_format,
        )
        if response_format == "url":
            return [img.url for img in resp.data if img.url]
        return [img.b64_json for img in resp.data if img.b64_json]

    async def edit_image(
        self,
        image_path: str,
        prompt: str,
        model: str = "gpt-image-1",
        size: str = "1024x1024",
        n: int = 1,
    ) -> list[str]:
        """Edit an existing image based on a text prompt."""
        with open(image_path, "rb") as f:
            resp = await self._client.images.edit(
                model=model,
                image=f,
                prompt=prompt,
                n=n,
                size=size,
            )
        return [img.url for img in resp.data if img.url]

    # ── Text-to-Speech ───────────────────────────────────────────
    # Spider: Root (voice output for commander briefings)

    async def tts(
        self,
        text: str,
        output_path: str,
        model: str = "gpt-4o-mini-tts",
        voice: str = "alloy",
    ) -> str:
        """Generate speech audio from text. Saves to output_path.

        Voices: alloy, ash, ballad, coral, echo, fable, nova, onyx, sage, shimmer
        Returns the output file path.
        """
        async with self._client.audio.speech.with_streaming_response.create(
            model=model,
            voice=voice,
            input=text,
        ) as response:
            with open(output_path, "wb") as f:
                async for chunk in response.iter_bytes():
                    f.write(chunk)
        return output_path

    # ── Speech-to-Text (Whisper) ─────────────────────────────────
    # Spider: Scholar (transcribe audio/video for research)

    async def transcribe(
        self,
        audio_path: str,
        model: str = "whisper-1",
        language: str | None = None,
        prompt: str | None = None,
    ) -> str:
        """Transcribe audio file to text using Whisper.

        Supports: mp3, mp4, mpeg, mpga, m4a, wav, webm
        """
        kwargs: dict = {"model": model}
        if language:
            kwargs["language"] = language
        if prompt:
            kwargs["prompt"] = prompt
        with open(audio_path, "rb") as f:
            kwargs["file"] = f
            resp = await self._client.audio.transcriptions.create(**kwargs)
        return resp.text

    async def translate(
        self,
        audio_path: str,
        model: str = "whisper-1",
    ) -> str:
        """Translate audio file to English text."""
        with open(audio_path, "rb") as f:
            resp = await self._client.audio.translations.create(
                model=model,
                file=f,
            )
        return resp.text

    # ── Moderation ───────────────────────────────────────────────
    # Spider: Root (safety filter on ALL agent outputs)

    async def moderate(
        self,
        text: str,
        model: str = "omni-moderation-latest",
    ) -> dict:
        """Check text for harmful content. Returns flagged categories.

        Use as a safety gate on agent outputs before showing to user.
        Returns: {flagged: bool, categories: {hate: bool, ...}, scores: {hate: float, ...}}
        """
        resp = await self._client.moderations.create(
            input=text,
            model=model,
        )
        result = resp.results[0]
        return {
            "flagged": result.flagged,
            "categories": {k: v for k, v in vars(result.categories).items() if not k.startswith("_")},
            "scores": {k: v for k, v in vars(result.category_scores).items() if not k.startswith("_")},
        }

    async def moderate_with_image(
        self,
        text: str,
        image_url: str,
        model: str = "omni-moderation-latest",
    ) -> dict:
        """Check text + image for harmful content."""
        resp = await self._client.moderations.create(
            input=[
                {"type": "text", "text": text},
                {"type": "image_url", "image_url": {"url": image_url}},
            ],
            model=model,
        )
        result = resp.results[0]
        return {
            "flagged": result.flagged,
            "categories": {k: v for k, v in vars(result.categories).items() if not k.startswith("_")},
            "scores": {k: v for k, v in vars(result.category_scores).items() if not k.startswith("_")},
        }

    # ── Models ───────────────────────────────────────────────────

    async def list_models(self) -> list[str]:
        """List all available OpenAI models."""
        resp = await self._client.models.list()
        return sorted([m.id for m in resp.data])

    # ── Responses API ────────────────────────────────────────────
    # The NEW primary interface for agent workflows. Built-in tools
    # (web search, code interpreter, file search) that OpenAI EXECUTES.
    # Spider: ALL spiders — this replaces chat_completion for agentic use.

    async def response(
        self,
        input: str,  # noqa: A002
        model: str = "gpt-5.4",
        instructions: str | None = None,
        tools: list[dict] | None = None,
        previous_response_id: str | None = None,
        store: bool = True,
        stream: bool = False,
        max_output_tokens: int | None = None,
        temperature: float | None = None,
    ) -> dict:
        """Create a response using the Responses API.

        Built-in tools (no execution loop needed):
          - {"type": "web_search_preview"} — real-time web search
          - {"type": "code_interpreter"} — sandboxed Python execution
          - {"type": "file_search", "vector_store_ids": ["vs_..."]} — RAG over docs

        Stateful conversations via previous_response_id — no message array management.
        """
        kwargs: dict = {"model": model, "input": input, "store": store}
        if instructions:
            kwargs["instructions"] = instructions
        if tools:
            kwargs["tools"] = tools
        if previous_response_id:
            kwargs["previous_response_id"] = previous_response_id
        if max_output_tokens:
            kwargs["max_output_tokens"] = max_output_tokens
        if temperature is not None:
            kwargs["temperature"] = temperature

        if not stream:
            resp = await self._client.responses.create(**kwargs)
            return {
                "id": resp.id,
                "output_text": resp.output_text,
                "output": [vars(o) if hasattr(o, '__dict__') else o for o in resp.output] if resp.output else [],
                "model": model,
                "provider": self._provider_name,
            }
        return await self._stream_response(kwargs)

    async def _stream_response(self, kwargs: dict) -> dict:
        """Stream a Responses API call, collecting output."""
        kwargs["stream"] = True
        collected_text = []
        response_id = ""
        stream = await self._client.responses.create(**kwargs)
        async for event in stream:
            if hasattr(event, 'type'):
                if event.type == 'response.output_text.delta' and hasattr(event, 'delta'):
                    collected_text.append(event.delta)
                elif event.type == 'response.completed' and hasattr(event, 'response'):
                    response_id = event.response.id if hasattr(event.response, 'id') else ""
        return {
            "id": response_id,
            "output_text": "".join(collected_text),
            "model": kwargs.get("model", ""),
            "provider": self._provider_name,
        }

    async def web_search(
        self,
        query: str,
        model: str = "gpt-5.4",
        instructions: str | None = None,
    ) -> str:
        """Search the web and return a synthesized answer.

        Spider: Scholar (real-time web research)
        Uses Responses API with built-in web_search_preview tool.
        """
        resp = await self.response(
            input=query,
            model=model,
            instructions=instructions or "Search the web and provide a comprehensive answer with sources.",
            tools=[{"type": "web_search_preview"}],
        )
        return resp.get("output_text", "")

    async def code_interpret(
        self,
        prompt: str,
        model: str = "gpt-5.4",
        file_ids: list[str] | None = None,
    ) -> dict:
        """Execute code in OpenAI's sandboxed Python environment.

        Spider: Payload (Compiler) — sandboxed code execution
        Returns both the text output and any generated files.
        """
        tools: list[dict] = [{"type": "code_interpreter"}]
        if file_ids:
            tools[0]["file_ids"] = file_ids
        resp = await self.response(
            input=prompt,
            model=model,
            instructions="Write and execute Python code to solve this task. Show your work.",
            tools=tools,
        )
        return resp

    # ── File Search + Vector Stores ──────────────────────────────
    # Spider: Scholar (RAG over documents), Proxy (deep reasoning over docs)

    async def create_vector_store(
        self,
        name: str,
        file_ids: list[str] | None = None,
        metadata: dict | None = None,
    ) -> dict:
        """Create a vector store for file search / RAG.

        Upload files first with upload_file(), then pass file_ids here.
        The vector store auto-chunks and embeds the files.
        """
        kwargs: dict = {"name": name}
        if file_ids:
            kwargs["file_ids"] = file_ids
        if metadata:
            kwargs["metadata"] = metadata
        resp = await self._client.vector_stores.create(**kwargs)
        return {"id": resp.id, "name": resp.name, "status": resp.status, "file_counts": vars(resp.file_counts) if hasattr(resp.file_counts, '__dict__') else {}}

    async def add_file_to_vector_store(
        self,
        vector_store_id: str,
        file_id: str,
    ) -> dict:
        """Add a file to an existing vector store."""
        resp = await self._client.vector_stores.files.create(
            vector_store_id=vector_store_id,
            file_id=file_id,
        )
        return {"id": resp.id, "status": resp.status}

    async def file_search(
        self,
        query: str,
        vector_store_ids: list[str],
        model: str = "gpt-5.4",
        instructions: str | None = None,
    ) -> str:
        """Search over documents in vector stores using Responses API.

        Spider: Scholar, Proxy — RAG pipeline for document-heavy tasks.
        """
        resp = await self.response(
            input=query,
            model=model,
            instructions=instructions or "Search the provided documents and answer based on their content.",
            tools=[{"type": "file_search", "vector_store_ids": vector_store_ids}],
        )
        return resp.get("output_text", "")

    # ── Files API ────────────────────────────────────────────────
    # Used by: Vector Stores, Batch, Fine-tuning, Code Interpreter

    async def upload_file(
        self,
        file_path: str,
        purpose: str = "assistants",
    ) -> str:
        """Upload a file to OpenAI. Returns file ID.

        Purposes: 'assistants' (vector stores/file search), 'batch', 'fine-tune'
        """
        with open(file_path, "rb") as f:
            resp = await self._client.files.create(file=f, purpose=purpose)
        return resp.id

    async def list_files(self) -> list[dict]:
        """List all uploaded files."""
        resp = await self._client.files.list()
        return [{"id": f.id, "filename": f.filename, "purpose": f.purpose, "bytes": f.bytes, "created_at": f.created_at} for f in resp.data]

    async def delete_file(self, file_id: str) -> bool:
        """Delete an uploaded file."""
        resp = await self._client.files.delete(file_id)
        return resp.deleted

    # ── Batch API ────────────────────────────────────────────────
    # Spider: Cron (Automator) — bulk processing at 50% cost
    # Queue thousands of requests, get results later.

    async def create_batch(
        self,
        input_file_id: str,
        endpoint: str = "/v1/chat/completions",
        completion_window: str = "24h",
        metadata: dict | None = None,
    ) -> dict:
        """Create a batch processing job.

        Spider: Cron — schedule bulk operations at 50% API cost.
        Upload a JSONL file with requests first via upload_file(purpose='batch').
        """
        kwargs: dict = {
            "input_file_id": input_file_id,
            "endpoint": endpoint,
            "completion_window": completion_window,
        }
        if metadata:
            kwargs["metadata"] = metadata
        resp = await self._client.batches.create(**kwargs)
        return {"id": resp.id, "status": resp.status, "endpoint": resp.endpoint, "created_at": resp.created_at}

    async def get_batch(self, batch_id: str) -> dict:
        """Check status of a batch job."""
        resp = await self._client.batches.retrieve(batch_id)
        return {
            "id": resp.id, "status": resp.status,
            "output_file_id": resp.output_file_id,
            "error_file_id": resp.error_file_id,
            "request_counts": vars(resp.request_counts) if hasattr(resp.request_counts, '__dict__') else {},
        }

    async def list_batches(self, limit: int = 20) -> list[dict]:
        """List recent batch jobs."""
        resp = await self._client.batches.list(limit=limit)
        return [{"id": b.id, "status": b.status, "endpoint": b.endpoint, "created_at": b.created_at} for b in resp.data]

    async def cancel_batch(self, batch_id: str) -> dict:
        """Cancel a batch job."""
        resp = await self._client.batches.cancel(batch_id)
        return {"id": resp.id, "status": resp.status}

    # ── Fine-tuning ──────────────────────────────────────────────
    # Spider: Zero (Lab) — train custom models on specific data

    async def create_fine_tune(
        self,
        training_file_id: str,
        model: str = "gpt-4o-mini-2024-07-18",
        suffix: str | None = None,
        n_epochs: int | str = "auto",
        hyperparameters: dict | None = None,
    ) -> dict:
        """Start a fine-tuning job.

        Spider: Zero (Lab) — experiments with custom model training.
        Upload training JSONL via upload_file(purpose='fine-tune') first.
        """
        kwargs: dict = {"training_file": training_file_id, "model": model}
        hp = hyperparameters or {}
        hp["n_epochs"] = n_epochs
        kwargs["hyperparameters"] = hp
        if suffix:
            kwargs["suffix"] = suffix
        resp = await self._client.fine_tuning.jobs.create(**kwargs)
        return {"id": resp.id, "model": resp.model, "status": resp.status, "created_at": resp.created_at}

    async def get_fine_tune(self, job_id: str) -> dict:
        """Check status of a fine-tuning job."""
        resp = await self._client.fine_tuning.jobs.retrieve(job_id)
        return {
            "id": resp.id, "model": resp.model, "status": resp.status,
            "fine_tuned_model": resp.fine_tuned_model,
            "trained_tokens": resp.trained_tokens,
        }

    async def list_fine_tunes(self, limit: int = 20) -> list[dict]:
        """List fine-tuning jobs."""
        resp = await self._client.fine_tuning.jobs.list(limit=limit)
        return [{"id": j.id, "model": j.model, "status": j.status, "fine_tuned_model": j.fine_tuned_model} for j in resp.data]

    async def cancel_fine_tune(self, job_id: str) -> dict:
        """Cancel a fine-tuning job."""
        resp = await self._client.fine_tuning.jobs.cancel(job_id)
        return {"id": resp.id, "status": resp.status}

    # ── Realtime API ─────────────────────────────────────────────
    # Connection setup for voice conversations. Full pipeline requires
    # WebSocket integration at the server level.

    def get_realtime_url(self, model: str = "gpt-4o-realtime-preview") -> str:
        """Get the WebSocket URL for the Realtime API.

        The caller must establish a WebSocket connection with:
          - Header: Authorization: Bearer {api_key}
          - Header: OpenAI-Beta: realtime=v1
        """
        return f"wss://api.openai.com/v1/realtime?model={model}"

    def get_realtime_headers(self) -> dict:
        """Get the required headers for Realtime API WebSocket connection."""
        settings = get_settings()
        return {
            "Authorization": f"Bearer {settings.openai_api_key}",
            "OpenAI-Beta": "realtime=v1",
        }

    # ── Video Generation ─────────────────────────────────────────
    # Spider: Wolf (marketing videos), Zero (experiments)

    async def generate_video(
        self,
        prompt: str,
        model: str = "sora",
        size: str = "1920x1080",
        duration: int = 5,
    ) -> dict:
        """Generate video from text prompt (when available).

        Note: Video generation API availability varies. This wraps the
        endpoint when it's accessible.
        """
        try:
            resp = await self._client.post(
                "/v1/videos/generations",
                body={"model": model, "prompt": prompt, "size": size, "duration": duration},
                cast_to=object,
            )
            return {"status": "submitted", "data": resp}
        except Exception as e:
            return {"status": "unavailable", "error": str(e)}


class DeepSeekClient(OpenAIClient):
    """Full DeepSeek API integration — OpenAI-compatible + unique features.

    Inherits from OpenAIClient: chat, chat_completion, streaming, tool calling,
    structured_output, list_models.

    DeepSeek-unique features (NOT in OpenAI):
    - Thinking Mode (R1 reasoning) — chain-of-thought with reasoning_content
    - FIM Completion — Fill-in-the-Middle for code (prompt + suffix)
    - Chat Prefix Completion — force model to continue from a prefix
    - Balance Query — check account credits
    - Auto Prefix Caching — automatic, no API call needed (reduced cost on cache hits)

    Spider allocation:
    - thinking → Proxy (Oracle) — deep reasoning
    - fim/prefix_completion → Payload (Compiler) — code infill
    - balance → System/Root — cost monitoring
    """

    _provider_name = "deepseek"

    def __init__(self):
        settings = get_settings()
        self._api_key = getattr(settings, 'deepseek_api_key', '') or ''
        self._client = openai.AsyncOpenAI(
            api_key=self._api_key,
            base_url="https://api.deepseek.com",
        )
        # Beta client for FIM and prefix completion endpoints
        self._beta_client = openai.AsyncOpenAI(
            api_key=self._api_key,
            base_url="https://api.deepseek.com/beta",
        )

    # ── Thinking Mode (R1 Reasoning) ─────────────────────────────
    # Spider: Proxy (Oracle) — deep chain-of-thought reasoning

    async def think(
        self,
        messages: list[dict],
        model: str = "deepseek-reasoner",
        tools: list[dict] | None = None,
        max_tokens: int = 8192,
        temperature: float = 0.7,
    ) -> dict:
        """Enable thinking mode — model outputs reasoning chain before answer.

        Returns both reasoning_content (thought process) and content (final answer).
        Can use model='deepseek-reasoner' OR pass thinking param with any model.
        """
        kwargs: dict = {
            "model": model,
            "messages": messages,
            "max_tokens": max_tokens,
            "temperature": temperature,
        }
        if tools:
            kwargs["tools"] = tools
        # Enable thinking via extra_body if not using deepseek-reasoner model
        if model != "deepseek-reasoner":
            kwargs["extra_body"] = {"thinking": {"type": "enabled"}}

        resp = await self._client.chat.completions.create(**kwargs)
        msg = resp.choices[0].message
        return {
            "reasoning": getattr(msg, 'reasoning_content', '') or '',
            "content": msg.content or '',
            "tool_calls": [
                {"name": tc.function.name, "arguments": _json.loads(tc.function.arguments) if isinstance(tc.function.arguments, str) else tc.function.arguments}
                for tc in (msg.tool_calls or [])
            ],
            "tokens_in": resp.usage.prompt_tokens if resp.usage else 0,
            "tokens_out": resp.usage.completion_tokens if resp.usage else 0,
            "model": model,
            "provider": self._provider_name,
        }

    # ── FIM Completion ───────────────────────────────────────────
    # Spider: Payload (Compiler) — code Fill-in-the-Middle

    async def fim(
        self,
        prompt: str,
        suffix: str,
        model: str = "deepseek-chat",
        max_tokens: int = 128,
        temperature: float = 0.0,
    ) -> str:
        """Fill-in-the-Middle completion — given code before and after, fill the gap.

        Example: prompt='def fib(a):' suffix='    return fib(a-1) + fib(a-2)'
        The model fills in the middle (function body).
        Uses the /beta endpoint.
        """
        resp = await self._beta_client.completions.create(
            model=model,
            prompt=prompt,
            suffix=suffix,
            max_tokens=max_tokens,
            temperature=temperature,
        )
        return resp.choices[0].text or ''

    # ── Chat Prefix Completion ───────────────────────────────────
    # Spider: Payload (Compiler) — force output format

    async def prefix_completion(
        self,
        messages: list[dict],
        assistant_prefix: str,
        model: str = "deepseek-chat",
        max_tokens: int = 4096,
        stop: list[str] | None = None,
    ) -> str:
        """Continue generation from a forced prefix.

        The assistant_prefix is prepended to the model's output — it MUST
        continue from that exact string. Useful for forcing code blocks,
        JSON structure, or specific format.
        Uses the /beta endpoint.
        """
        msgs = list(messages)
        msgs.append({"role": "assistant", "content": assistant_prefix, "prefix": True})
        kwargs: dict = {"model": model, "messages": msgs, "max_tokens": max_tokens}
        if stop:
            kwargs["stop"] = stop
        resp = await self._beta_client.chat.completions.create(**kwargs)
        return resp.choices[0].message.content or ''

    # ── Balance Query ────────────────────────────────────────────
    # Spider: System/Root — cost monitoring

    async def get_balance(self) -> dict:
        """Check DeepSeek account balance/credits.

        Returns available balance and usage information.
        """
        import httpx
        async with httpx.AsyncClient(timeout=10) as client:
            resp = await client.get(
                "https://api.deepseek.com/user/balance",
                headers={"Authorization": f"Bearer {self._api_key}", "Accept": "application/json"},
            )
            resp.raise_for_status()
            return resp.json()


class XAIClient(OpenAIClient):
    """Full xAI Grok API — OpenAI compat + native xai_sdk features.

    Inherits from OpenAIClient: chat, streaming, tools, structured_output, image gen.

    xAI-unique (via xai_sdk): x_search, web_search, sandboxed code,
    collections/RAG, files, voice/realtime, reasoning, citations.

    Spiders: Scholar gets x_search+web, Payload gets code, Proxy gets reasoning,
    Wolf gets x_search for sentiment, Root gets voice.
    """

    _provider_name = "xai"

    def __init__(self):
        settings = get_settings()
        self._api_key = getattr(settings, 'xai_api_key', '') or ''
        self._client = openai.AsyncOpenAI(api_key=self._api_key, base_url="https://api.x.ai/v1")
        from xai_sdk import Client as _XC
        self._xai = _XC(api_key=self._api_key)

    # ── X/Twitter Search — real-time post search with citations
    def x_search(self, query: str, model: str = "grok-4.20-beta-latest-non-reasoning") -> dict:
        """Search X/Twitter posts. Returns content + citations."""
        from xai_sdk.chat import user as _u
        from xai_sdk.tools import x_search as _xs
        chat = self._xai.chat.create(model=model, tools=[_xs()])
        chat.append(_u(query))
        r = chat.sample()
        return {"content": r.content, "citations": str(r.citations) if r.citations else "", "provider": self._provider_name}

    # ── Web Search — server-side web search
    def xai_web_search(self, query: str, model: str = "grok-4.20-beta-latest-non-reasoning") -> dict:
        """Web search via xAI's built-in tool."""
        from xai_sdk.chat import user as _u
        from xai_sdk.tools import web_search as _ws
        chat = self._xai.chat.create(model=model, tools=[_ws()])
        chat.append(_u(query))
        r = chat.sample()
        return {"content": r.content, "citations": str(r.citations) if r.citations else "", "provider": self._provider_name}

    # ── Sandboxed Code Runner
    def xai_run_code(self, prompt: str, model: str = "grok-4.20-beta-latest-non-reasoning") -> dict:
        """Run code in xAI's sandboxed environment."""
        from xai_sdk.chat import user as _u
        from xai_sdk.tools import code_execution as _ce
        chat = self._xai.chat.create(model=model, tools=[_ce()])
        chat.append(_u(prompt))
        r = chat.sample()
        return {"content": r.content, "reasoning_tokens": r.usage.reasoning_tokens if r.usage else 0, "provider": self._provider_name}

    # ── Combined Search + Code — full research pipeline in one call
    def search_and_analyze(self, query: str, model: str = "grok-4.20-beta-latest-non-reasoning") -> dict:
        """Search X + web + run code in one call."""
        from xai_sdk.chat import user as _u
        from xai_sdk.tools import web_search as _ws, x_search as _xs, code_execution as _ce
        chat = self._xai.chat.create(model=model, tools=[_ws(), _xs(), _ce()])
        chat.append(_u(query))
        r = chat.sample()
        return {"content": r.content, "citations": str(r.citations) if r.citations else "", "provider": self._provider_name}

    # ── Collections (Document RAG)
    async def create_collection(self, name: str) -> str:
        """Create a document collection. Returns collection_id."""
        r = self._xai.collections.create(name)
        return r.collection_id

    async def upload_to_collection(self, collection_id: str, data: bytes, filename: str) -> dict:
        """Upload a document to a collection."""
        r = self._xai.collections.upload_document(collection_id=collection_id, name=filename, data=data)
        return {"file_id": r.file_metadata.file_id if r.file_metadata else "", "status": "uploaded"}

    def collection_search(self, query: str, collection_ids: list[str], model: str = "grok-4.20-beta-latest-non-reasoning") -> dict:
        """Search across document collections."""
        from xai_sdk.chat import user as _u
        from xai_sdk.tools import collections_search as _cs
        chat = self._xai.chat.create(model=model, tools=[_cs(collection_ids=collection_ids)])
        chat.append(_u(query))
        r = chat.sample()
        return {"content": r.content, "citations": str(r.citations) if r.citations else "", "provider": self._provider_name}

    # ── Files
    def xai_upload_file(self, data: bytes, filename: str) -> str:
        """Upload a file. Returns file ID."""
        r = self._xai.files.upload(data, filename=filename)
        return r.id

    def xai_delete_file(self, file_id: str) -> bool:
        """Delete a file."""
        self._xai.files.delete(file_id)
        return True

    # ── Voice / Realtime
    def get_realtime_url(self) -> str:
        """WebSocket URL for real-time voice."""
        return "wss://api.x.ai/v1/realtime"

    def get_realtime_headers(self) -> dict:
        """Headers for voice WebSocket."""
        return {"Authorization": f"Bearer {self._api_key}"}

    # ── Native Image Generation
    def xai_generate_image(self, prompt: str, model: str = "grok-imagine-image", fmt: str = "base64") -> bytes:
        """Generate image via xAI native API."""
        r = self._xai.image.sample(prompt=prompt, model=model, image_format=fmt)
        return r.image


class GoogleClient:
    """Full Google Gemini API integration — all capabilities via google-genai SDK.

    Features:
    - Text Generation (generateContent) — streaming + non-streaming
    - Function Calling (tool declarations)
    - Structured Output (response_schema / response_mime_type)
    - Code Execution (sandboxed Python)
    - Google Search Grounding
    - Vision (image + video understanding)
    - Audio Understanding
    - Image Generation (Imagen)
    - Video Generation (Veo)
    - Speech Generation (TTS)
    - Embeddings (gemini-embedding-001)
    - Context Caching (reduced cost for repeated large contexts)
    - File Upload (Files API)
    - Tuning (fine-tuning)
    - Batch Prediction
    - Token Counting
    - Thinking Mode (extended reasoning with budget)
    - Live API (real-time streaming)

    Spider allocation:
    - chat/structured_output → ALL spiders (Router uses gemini-flash for classification)
    - google_search → Scholar (real-time web research)
    - code_execute → Payload (Compiler)
    - vision/audio → Scholar, Zero
    - image_gen → Wolf, Zero
    - video_gen → Wolf, Zero
    - tts → Root
    - embeddings → Scholar, semantic cache
    - caching → ALL (cost optimization for large context tasks)
    - tuning → Zero (Lab)
    - batch → Cron (Automator)
    """

    def __init__(self):
        from google import genai as _genai
        from google.genai import types as _types
        settings = get_settings()
        self._api_key = getattr(settings, 'google_api_key', '') or ''
        self._client = _genai.Client(api_key=self._api_key)
        self._types = _types
        self._genai = _genai

    def _to_contents(self, messages: list[dict]) -> tuple[list, str]:
        """Convert OpenAI-format messages to Gemini contents + system instruction."""
        contents = []
        system_text = ""
        for m in messages:
            if m["role"] == "system":
                system_text += m["content"] + "\n"
            else:
                role = "user" if m["role"] == "user" else "model"
                contents.append({"role": role, "parts": [{"text": m["content"]}]})
        return contents, system_text.strip()

    # ── Text Generation ──────────────────────────────────────────

    async def chat(self, messages: list[dict], model: str = "gemini-3.1-pro",
                   max_tokens: int = 4096, temperature: float = 0.7, stream: bool = False) -> str:
        """Generate text from a conversation. Returns str."""
        contents, system_text = self._to_contents(messages)
        config = self._types.GenerateContentConfig(
            temperature=temperature, max_output_tokens=max_tokens,
        )
        if system_text:
            config.system_instruction = system_text
        resp = self._client.models.generate_content(
            model=model, contents=contents, config=config,
        )
        return resp.text or ""

    async def chat_completion(
        self, messages: list[dict], model: str = "gemini-3.1-pro",
        tools: list[dict] | None = None, max_tokens: int = 4096, temperature: float = 0.7,
    ) -> LLMResponse:
        """Chat with structured response — supports function calling."""
        contents, system_text = self._to_contents(messages)
        config = self._types.GenerateContentConfig(
            temperature=temperature, max_output_tokens=max_tokens,
        )
        if system_text:
            config.system_instruction = system_text
        if tools:
            gemini_tools = []
            for t in tools:
                fn = t.get("function", t)
                gemini_tools.append(self._types.FunctionDeclaration(
                    name=fn["name"], description=fn.get("description", ""),
                    parameters=fn.get("parameters", {}),
                ))
            config.tools = [self._types.Tool(function_declarations=gemini_tools)]

        resp = self._client.models.generate_content(
            model=model, contents=contents, config=config,
        )
        text_parts = []
        tool_calls_out = []
        for part in resp.candidates[0].content.parts:
            if part.text:
                text_parts.append(part.text)
            if part.function_call:
                tool_calls_out.append(ToolCall(
                    name=part.function_call.name,
                    arguments=dict(part.function_call.args) if part.function_call.args else {},
                ))
        usage = resp.usage_metadata or {}
        return LLMResponse(
            text="\n".join(text_parts), tool_calls=tool_calls_out,
            tokens_in=getattr(usage, 'prompt_token_count', 0),
            tokens_out=getattr(usage, 'candidates_token_count', 0),
            model=model, provider="google",
        )

    # ── Structured Output ────────────────────────────────────────
    # Spider: Router (JSON classification), ALL spiders

    async def structured_output(
        self, prompt: str, schema: dict, model: str = "gemini-3.1-pro",
        temperature: float = 0.3,
    ) -> dict:
        """Generate guaranteed JSON output matching a schema."""
        resp = self._client.models.generate_content(
            model=model, contents=prompt,
            config=self._types.GenerateContentConfig(
                temperature=temperature,
                response_mime_type="application/json",
                response_schema=schema,
            ),
        )
        return _json.loads(resp.text or "{}")

    # ── Code Execution ───────────────────────────────────────────
    # Spider: Payload (Compiler) — sandboxed Python execution

    async def code_execute(
        self, prompt: str, model: str = "gemini-3.1-pro",
    ) -> dict:
        """Execute code in Gemini's sandboxed Python environment."""
        resp = self._client.models.generate_content(
            model=model, contents=prompt,
            config=self._types.GenerateContentConfig(
                tools=[self._types.Tool(code_execution=self._types.ToolCodeExecution)],
            ),
        )
        results = {"text": "", "code": "", "output": ""}
        for part in resp.candidates[0].content.parts:
            if part.text:
                results["text"] += part.text
            if part.executable_code:
                results["code"] += part.executable_code.code
            if part.code_execution_result:
                results["output"] += part.code_execution_result.output
        return results

    # ── Google Search Grounding ──────────────────────────────────
    # Spider: Scholar (real-time web research)

    async def google_search(
        self, query: str, model: str = "gemini-3.1-pro",
    ) -> str:
        """Search the web via Google Search grounding."""
        resp = self._client.models.generate_content(
            model=model, contents=query,
            config=self._types.GenerateContentConfig(
                tools=[self._types.Tool(google_search=self._types.GoogleSearch())],
            ),
        )
        return resp.text or ""

    # ── Vision ───────────────────────────────────────────────────
    # Spider: Scholar (screenshots/charts), Zero (experiments)

    async def vision(
        self, prompt: str, image_path: str, model: str = "gemini-3.1-pro",
    ) -> str:
        """Analyze an image with a text prompt."""
        uploaded = self._client.files.upload(file=image_path)
        resp = self._client.models.generate_content(
            model=model, contents=[uploaded, prompt],
        )
        return resp.text or ""

    async def vision_url(
        self, prompt: str, image_url: str, model: str = "gemini-3.1-pro",
    ) -> str:
        """Analyze an image from URL."""
        import httpx
        img_data = httpx.get(image_url).content
        import tempfile, os
        with tempfile.NamedTemporaryFile(suffix=".jpg", delete=False) as f:
            f.write(img_data)
            tmp = f.name
        try:
            return await self.vision(prompt, tmp, model)
        finally:
            os.unlink(tmp)

    # ── Audio Understanding ──────────────────────────────────────
    # Spider: Scholar (process audio/video content)

    async def understand_audio(
        self, prompt: str, audio_path: str, model: str = "gemini-3.1-pro",
    ) -> str:
        """Analyze an audio file with a text prompt."""
        uploaded = self._client.files.upload(file=audio_path)
        # Wait for processing
        import time
        while uploaded.state.name == 'PROCESSING':
            time.sleep(1)
            uploaded = self._client.files.get(name=uploaded.name)
        resp = self._client.models.generate_content(
            model=model, contents=[uploaded, prompt],
        )
        return resp.text or ""

    # ── Image Generation (Imagen) ────────────────────────────────
    # Spider: Wolf (product images), Zero (experiments)

    async def generate_image(
        self, prompt: str, model: str = "imagen-3.0-generate-002",
        n: int = 1,
    ) -> list[bytes]:
        """Generate images from text using Imagen. Returns list of image bytes."""
        resp = self._client.models.generate_images(
            model=model, prompt=prompt,
            config=self._types.GenerateImagesConfig(number_of_images=n),
        )
        return [img.image.image_bytes for img in resp.generated_images]

    # ── Video Generation (Veo) ───────────────────────────────────
    # Spider: Wolf (marketing), Zero (experiments)

    async def generate_video(
        self, prompt: str, model: str = "veo-3.1-generate-preview",
    ) -> dict:
        """Generate video from text using Veo. Returns operation to poll."""
        import time
        operation = self._client.models.generate_videos(
            model=model, prompt=prompt,
        )
        while not operation.done:
            time.sleep(5)
            operation = self._client.operations.get(operation)
        return {"done": True, "result": str(operation.result) if operation.result else "completed"}

    # ── Speech Generation (TTS) ──────────────────────────────────
    # Spider: Root (voice output)

    async def tts(
        self, text: str, output_path: str,
        model: str = "gemini-2.5-flash-preview-tts", voice: str = "Kore",
    ) -> str:
        """Generate speech audio from text. Saves WAV to output_path."""
        import wave
        resp = self._client.models.generate_content(
            model=model, contents=text,
            config=self._types.GenerateContentConfig(
                response_modalities=["AUDIO"],
                speech_config=self._types.SpeechConfig(
                    voice_config=self._types.VoiceConfig(
                        prebuilt_voice_config=self._types.PrebuiltVoiceConfig(voice_name=voice),
                    ),
                ),
            ),
        )
        data = resp.candidates[0].content.parts[0].inline_data.data
        with wave.open(output_path, "wb") as wf:
            wf.setnchannels(1)
            wf.setsampwidth(2)
            wf.setframerate(24000)
            wf.writeframes(data)
        return output_path

    # ── Embeddings ───────────────────────────────────────────────
    # Spider: Scholar (semantic search), semantic cache

    async def embed(
        self, text: str | list[str], model: str = "gemini-embedding-001",
        dimensions: int | None = None,
    ) -> list[list[float]]:
        """Generate vector embeddings."""
        config = {}
        if dimensions:
            config["output_dimensionality"] = dimensions
        resp = self._client.models.embed_content(
            model=model, contents=text, config=config if config else None,
        )
        if hasattr(resp, 'embeddings'):
            return [e.values for e in resp.embeddings]
        return [resp.embedding.values] if hasattr(resp, 'embedding') else []

    # ── Context Caching ──────────────────────────────────────────
    # Spider: ALL — reduces cost for repeated large-context tasks

    async def create_cache(
        self, contents: list, model: str = "gemini-3.1-pro",
        system_instruction: str | None = None, ttl_seconds: int = 3600,
    ) -> str:
        """Create a context cache for large documents. Returns cache name."""
        config = self._types.CreateCachedContentConfig(contents=contents)
        if system_instruction:
            config.system_instruction = system_instruction
        cache = self._client.caches.create(model=model, config=config)
        return cache.name

    async def chat_with_cache(
        self, prompt: str, cache_name: str, model: str = "gemini-3.1-pro",
    ) -> str:
        """Generate content using a cached context."""
        resp = self._client.models.generate_content(
            model=model, contents=prompt,
            config=self._types.GenerateContentConfig(cached_content=cache_name),
        )
        return resp.text or ""

    # ── File Upload ──────────────────────────────────────────────

    async def upload_file(self, file_path: str, mime_type: str | None = None) -> dict:
        """Upload a file to Gemini Files API."""
        kwargs = {"file": file_path}
        if mime_type:
            kwargs["config"] = {"mime_type": mime_type}
        resp = self._client.files.upload(**kwargs)
        return {"name": resp.name, "uri": resp.uri, "state": resp.state.name, "mime_type": resp.mime_type}

    async def list_files(self) -> list[dict]:
        """List uploaded files."""
        resp = self._client.files.list()
        return [{"name": f.name, "uri": f.uri, "state": f.state.name} for f in resp]

    async def delete_file(self, name: str) -> bool:
        """Delete an uploaded file."""
        self._client.files.delete(name=name)
        return True

    # ── Tuning (Fine-tuning) ─────────────────────────────────────
    # Spider: Zero (Lab) — train custom models

    async def create_tuning_job(
        self, training_data: list[dict], model: str = "gemini-3.1-flash-preview",
        epochs: int = 5, display_name: str | None = None,
    ) -> dict:
        """Create a tuning job. training_data: list of {text_input, output} dicts."""
        config = {"epoch_count": epochs, "tuned_model_display_name": display_name or "spider-tuned"}
        resp = self._client.tunings.create(
            base_model=model, training_dataset=training_data, config=config,
        )
        return {"name": resp.name, "state": str(resp.state) if hasattr(resp, 'state') else "submitted"}

    async def list_tuning_jobs(self) -> list[dict]:
        """List tuning jobs."""
        resp = self._client.tunings.list()
        return [{"name": t.name, "state": str(t.state)} for t in resp]

    # ── Batch Prediction ─────────────────────────────────────────
    # Spider: Cron (Automator) — bulk processing

    async def create_batch(
        self, requests_file: str, model: str = "gemini-3.1-pro",
        display_name: str | None = None,
    ) -> dict:
        """Create a batch prediction job from a JSONL file."""
        uploaded = self._client.files.upload(
            file=requests_file, config={"mime_type": "jsonl"},
        )
        resp = self._client.batches.create(
            model=model, src=uploaded.name,
            config={"display_name": display_name or "spider-batch"},
        )
        return {"name": resp.name, "state": resp.state.name if hasattr(resp.state, 'name') else str(resp.state)}

    async def get_batch(self, name: str) -> dict:
        """Check batch job status."""
        resp = self._client.batches.get(name=name)
        return {"name": resp.name, "state": resp.state.name if hasattr(resp.state, 'name') else str(resp.state)}

    # ── Token Counting ───────────────────────────────────────────

    async def count_tokens(
        self, contents: str | list, model: str = "gemini-3.1-pro",
    ) -> int:
        """Count tokens for content before sending. Helps budget management."""
        resp = self._client.models.count_tokens(model=model, contents=contents)
        return resp.total_tokens

    # ── Thinking Mode ────────────────────────────────────────────
    # Spider: Proxy (deep reasoning), Exploit (strategy)

    async def think(
        self, prompt: str, model: str = "gemini-3.1-pro",
        include_thoughts: bool = True, thinking_budget: int | None = None,
    ) -> dict:
        """Generate content with extended thinking/reasoning."""
        config = self._types.GenerateContentConfig(
            thinking_config=self._types.ThinkingConfig(
                include_thoughts=include_thoughts,
            ),
        )
        if thinking_budget:
            config.thinking_config.thinking_budget = thinking_budget
        resp = self._client.models.generate_content(
            model=model, contents=prompt, config=config,
        )
        result = {"text": "", "thoughts": ""}
        for part in resp.candidates[0].content.parts:
            if hasattr(part, 'thought') and part.thought:
                result["thoughts"] += (part.text or "")
            elif part.text:
                result["text"] += part.text
        return result

    # ── Live API ─────────────────────────────────────────────────
    # Real-time bidirectional streaming. Requires async WebSocket.

    def get_live_config(
        self, model: str = "gemini-3.1-flash-live-preview",
        tools: list[dict] | None = None,
        response_modalities: list[str] | None = None,
    ) -> dict:
        """Get configuration for a Live API session.

        The caller uses: async with client.aio.live.connect(model, config) as session
        """
        config: dict = {}
        if response_modalities:
            config["response_modalities"] = response_modalities
        if tools:
            config["tools"] = tools
        return {"model": model, "config": config, "client": self._client}

    # ── Models ───────────────────────────────────────────────────

    async def list_models(self) -> list[str]:
        """List available Gemini models."""
        resp = self._client.models.list()
        return [m.name for m in resp]


# Singletons
_anthropic: AnthropicClient | None = None
_openai: OpenAIClient | None = None
_deepseek: DeepSeekClient | None = None
_xai: XAIClient | None = None
_google: GoogleClient | None = None


def get_anthropic() -> AnthropicClient:
    global _anthropic
    if _anthropic is None: _anthropic = AnthropicClient()
    return _anthropic

def get_openai() -> OpenAIClient:
    global _openai
    if _openai is None: _openai = OpenAIClient()
    return _openai

def get_deepseek() -> DeepSeekClient:
    global _deepseek
    if _deepseek is None: _deepseek = DeepSeekClient()
    return _deepseek

def get_xai() -> XAIClient:
    global _xai
    if _xai is None: _xai = XAIClient()
    return _xai

def get_google() -> GoogleClient:
    global _google
    if _google is None: _google = GoogleClient()
    return _google


def get_cloud_client(provider: str):
    """Get the right client for a provider."""
    if provider == "anthropic": return get_anthropic()
    if provider == "openai": return get_openai()
    if provider == "deepseek": return get_deepseek()
    if provider == "xai": return get_xai()
    if provider == "google": return get_google()
    if provider == "oracle":
        from agentic_hub.core.oracle_client import get_oracle
        return get_oracle()
    return None
