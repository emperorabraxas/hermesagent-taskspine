"""Oracle Cloud Generative AI integration — 30+ models via OpenAI-compatible API.

Hosts Cohere, Llama 4, Gemini 2.5, Grok 4.20, and OpenAI models on OCI infrastructure.
Unique features: Cohere Embed v4 (multimodal), Rerank 3.5, NL2SQL, Guardrails (content
moderation + prompt injection + PII detection).

Spider allocation:
  - chat/structured_output → ALL (fallback cloud provider)
  - embed → Fangveil (research), Cachephantom (code)
  - rerank → Fangveil (document relevance for RAG)
  - guardrails → Cryptweaver (safety gate), Windowkernel (reasoning validation)
  - nl2sql → Fangveil (data queries), Cachephantom (database operations)
  - list_models → ALL (model discovery)
"""
from __future__ import annotations

import logging
from typing import Any, AsyncIterator

from agentic_hub.config import get_settings

logger = logging.getLogger(__name__)


class OracleClient:
    """Full Oracle Cloud Generative AI integration (7 methods).

    Uses oci-openai for OpenAI-compatible chat/completions.
    Uses native OCI SDK for embeddings, rerank, guardrails, NL2SQL.
    """

    def __init__(self):
        settings = get_settings()
        self._compartment_id = settings.oci_compartment_id
        self._profile = settings.oci_config_profile or "DEFAULT"
        self._client = None
        self._oci_client = None

    def _ensure_client(self):
        """Lazy-init the AsyncOciOpenAI client."""
        if self._client is None:
            from oci_openai import AsyncOciOpenAI, OciUserPrincipalAuth
            self._client = AsyncOciOpenAI(
                base_url="https://inference.generativeai.us-chicago-1.oci.oraclecloud.com/20231130/actions/v1",
                auth=OciUserPrincipalAuth(profile_name=self._profile),
                compartment_id=self._compartment_id,
            )

    def _ensure_oci_client(self):
        """Lazy-init the native OCI GenerativeAiInference client."""
        if self._oci_client is None:
            import oci
            config = oci.config.from_file(profile_name=self._profile)
            from oci.generative_ai_inference import GenerativeAiInferenceClient
            self._oci_client = GenerativeAiInferenceClient(config)

    @property
    def is_configured(self) -> bool:
        return bool(self._compartment_id)

    # ── Chat (OpenAI-compatible) ──────────────────────────────────

    async def chat(
        self,
        messages: list[dict],
        model: str = "cohere.command-a-03-2025",
        max_tokens: int = 4096,
        temperature: float = 0.7,
        stream: bool = False,
    ) -> str | AsyncIterator[str]:
        """Chat completion via OCI-hosted models."""
        self._ensure_client()
        resp = await self._client.chat.completions.create(
            model=model, messages=messages,
            max_tokens=max_tokens, temperature=temperature,
            stream=stream,
        )
        if stream:
            return self._stream_chat(resp)
        return resp.choices[0].message.content or ""

    async def _stream_chat(self, stream) -> AsyncIterator[str]:
        async for chunk in stream:
            if chunk.choices and chunk.choices[0].delta.content:
                yield chunk.choices[0].delta.content

    async def chat_completion(
        self,
        messages: list[dict],
        model: str = "cohere.command-a-03-2025",
        tools: list[dict] | None = None,
        max_tokens: int = 4096,
        temperature: float = 0.7,
    ) -> Any:
        """Chat with structured response + tool calling."""
        self._ensure_client()
        kwargs: dict = {
            "model": model, "messages": messages,
            "max_tokens": max_tokens, "temperature": temperature,
        }
        if tools:
            kwargs["tools"] = tools
        resp = await self._client.chat.completions.create(**kwargs)
        # Return in LLMResponse-compatible format
        from agentic_hub.core.tools.llm_response import LLMResponse, ToolCall
        text = resp.choices[0].message.content or ""
        tool_calls = []
        if resp.choices[0].message.tool_calls:
            for tc in resp.choices[0].message.tool_calls:
                import json as _json
                args = tc.function.arguments
                if isinstance(args, str):
                    try:
                        args = _json.loads(args)
                    except Exception:
                        args = {}
                tool_calls.append(ToolCall(name=tc.function.name, arguments=args, call_id=tc.id))
        return LLMResponse(
            text=text, tool_calls=tool_calls,
            tokens_in=resp.usage.prompt_tokens if resp.usage else 0,
            tokens_out=resp.usage.completion_tokens if resp.usage else 0,
            model=model, provider="oracle",
        )

    # ── Embeddings (Cohere Embed v4 — multimodal) ─────────────────

    async def embed(
        self,
        texts: list[str],
        model: str = "cohere.embed-english-v3.0",
        input_type: str = "search_document",
    ) -> list[list[float]]:
        """Generate embeddings using Cohere Embed models on OCI.

        input_type: 'search_document', 'search_query', 'classification', 'clustering'
        """
        import asyncio
        self._ensure_oci_client()

        def _embed():
            from oci.generative_ai_inference.models import (
                EmbedTextDetails, OnDemandServingMode,
            )
            details = EmbedTextDetails(
                serving_mode=OnDemandServingMode(model_id=model),
                compartment_id=self._compartment_id,
                inputs=texts,
                input_type=input_type,
            )
            resp = self._oci_client.embed_text(details)
            return resp.data.embeddings

        return await asyncio.to_thread(_embed)

    # ── Rerank (Cohere Rerank 3.5) ────────────────────────────────

    async def rerank(
        self,
        query: str,
        documents: list[str],
        model: str = "cohere.rerank.v3-5",
        top_n: int = 5,
    ) -> list[dict]:
        """Rerank documents by relevance to a query.

        Returns: [{"index": 0, "relevance_score": 0.95, "document": "..."}]
        """
        import asyncio
        self._ensure_oci_client()

        def _rerank():
            from oci.generative_ai_inference.models import (
                RerankTextDetails, OnDemandServingMode,
                RerankTextDocument,
            )
            docs = [RerankTextDocument(text=d) for d in documents]
            details = RerankTextDetails(
                serving_mode=OnDemandServingMode(model_id=model),
                compartment_id=self._compartment_id,
                query=query,
                documents=docs,
                top_n=top_n,
            )
            resp = self._oci_client.rerank_text(details)
            return [
                {"index": r.index, "relevance_score": r.relevance_score,
                 "document": documents[r.index] if r.index < len(documents) else ""}
                for r in resp.data.results
            ]

        return await asyncio.to_thread(_rerank)

    # ── Guardrails (Content Mod + Prompt Injection + PII) ─────────

    async def guardrails(
        self,
        text: str,
    ) -> dict:
        """Run guardrails check — content moderation, prompt injection, PII detection.

        Returns: {
            "content_moderation": {"overall": 0.0, "blocklist": 0.0},
            "prompt_injection": 0.0,
            "pii": [{"text": "...", "label": "EMAIL", "score": 0.95}]
        }
        """
        import asyncio
        self._ensure_oci_client()

        def _check():
            from oci.generative_ai_inference.models import (
                ApplyGuardrailsDetails,
            )
            details = ApplyGuardrailsDetails(
                compartment_id=self._compartment_id,
                text=text,
            )
            resp = self._oci_client.apply_guardrails(details)
            result = {"content_moderation": {}, "prompt_injection": 0.0, "pii": []}
            if hasattr(resp.data, 'results') and resp.data.results:
                r = resp.data.results
                if hasattr(r, 'content_moderation') and r.content_moderation:
                    cm = r.content_moderation
                    result["content_moderation"] = {
                        c.name.lower(): c.score for c in (cm.categories or [])
                    }
                if hasattr(r, 'prompt_injection') and r.prompt_injection:
                    result["prompt_injection"] = r.prompt_injection.score
                if hasattr(r, 'personally_identifiable_information'):
                    pii = r.personally_identifiable_information or []
                    result["pii"] = [
                        {"text": p.text, "label": p.label, "score": p.score,
                         "offset": p.offset, "length": p.length}
                        for p in pii
                    ]
            return result

        return await asyncio.to_thread(_check)

    # ── NL2SQL (Natural Language to SQL) ──────────────────────────

    async def nl2sql(
        self,
        query: str,
        vector_store_id: str,
    ) -> str:
        """Convert natural language to SQL query.

        Requires a vector store with ingested database schema.
        Returns the generated SQL string.
        """
        import asyncio
        self._ensure_oci_client()

        def _generate():
            from oci.generative_ai_inference.models import (
                GenerateSqlFromNlDetails,
            )
            details = GenerateSqlFromNlDetails(
                compartment_id=self._compartment_id,
                query=query,
                vector_store_id=vector_store_id,
            )
            resp = self._oci_client.generate_sql_from_nl(details)
            return resp.data.sql if hasattr(resp.data, 'sql') else str(resp.data)

        return await asyncio.to_thread(_generate)

    # ── List Models ───────────────────────────────────────────────

    async def list_models(self) -> list[dict]:
        """List available models on OCI Generative AI."""
        # Return known models since OCI doesn't have a simple list endpoint
        return [
            {"id": "cohere.command-a-reasoning", "type": "chat", "provider": "cohere"},
            {"id": "cohere.command-a-vision", "type": "chat+vision", "provider": "cohere"},
            {"id": "cohere.command-a-03-2025", "type": "chat", "provider": "cohere"},
            {"id": "cohere.command-r-plus-08-2024", "type": "chat", "provider": "cohere"},
            {"id": "meta.llama-4-maverick-17b-128e-instruct-fp8", "type": "chat", "provider": "meta"},
            {"id": "meta.llama-4-scout-17b-16e-instruct", "type": "chat", "provider": "meta"},
            {"id": "meta.llama-3.3-70b-instruct", "type": "chat", "provider": "meta"},
            {"id": "meta.llama-3.2-90b-vision-instruct", "type": "chat+vision", "provider": "meta"},
            {"id": "google.gemini-2.5-pro", "type": "chat", "provider": "google"},
            {"id": "google.gemini-2.5-flash", "type": "chat", "provider": "google"},
            {"id": "xai.grok-4.20-multi-agent", "type": "chat+agents", "provider": "xai"},
            {"id": "xai.grok-4.20", "type": "chat+reasoning", "provider": "xai"},
            {"id": "xai.grok-code-fast-1", "type": "code", "provider": "xai"},
            {"id": "cohere.embed-v4.0", "type": "embed+vision", "provider": "cohere"},
            {"id": "cohere.embed-english-v3.0", "type": "embed", "provider": "cohere"},
            {"id": "cohere.embed-multilingual-v3.0", "type": "embed", "provider": "cohere"},
            {"id": "cohere.rerank.v3-5", "type": "rerank", "provider": "cohere"},
        ]


# ── Singleton ─────────────────────────────────────────────────────

_instance: OracleClient | None = None


def get_oracle() -> OracleClient:
    global _instance
    if _instance is None:
        _instance = OracleClient()
    return _instance
