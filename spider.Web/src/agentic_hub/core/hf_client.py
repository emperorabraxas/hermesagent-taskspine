"""Hugging Face Hub integration — 900K+ models via Inference API + Hub management.

Uses AsyncInferenceClient for serverless inference (chat, vision, TTS, ASR, translation,
summarization, embeddings, classification, image gen, object detection, QA, NER) and
HfApi for model/dataset management (search, info, download).

Spider allocation:
  - chat/text_generation → ALL (fallback provider for any spider)
  - text_to_image → Wolf (product images), Scholar (research)
  - transcribe/translate → Scholar (research)
  - summarize → Scholar, Oracle (compress information)
  - embed → Scholar, Code Team (semantic search)
  - classify/classify_image → Scholar (analysis)
  - detect_objects → Scholar, Zero (experiments)
  - visual_qa/image_to_text → Scholar
  - ner → Scholar (entity extraction)
  - list_models/model_info → ALL (model discovery)
"""
from __future__ import annotations

import logging
from pathlib import Path
from typing import Any, AsyncIterator

from agentic_hub.config import get_settings

logger = logging.getLogger(__name__)


class HuggingFaceClient:
    """Full Hugging Face Hub integration — inference + model management (20 methods)."""

    def __init__(self):
        settings = get_settings()
        self._token = settings.hf_token or None
        from huggingface_hub import AsyncInferenceClient, HfApi
        self._client = AsyncInferenceClient(token=self._token)
        self._api = HfApi(token=self._token)

    # ── Chat / Text Generation ────────────────────────────────────

    async def chat_completion(
        self,
        messages: list[dict],
        model: str = "meta-llama/Meta-Llama-3-8B-Instruct",
        max_tokens: int = 2048,
        temperature: float = 0.7,
        stream: bool = False,
    ) -> str | AsyncIterator[str]:
        """Chat completion using any HF model. OpenAI-compatible format."""
        output = await self._client.chat_completion(
            messages=messages,
            model=model,
            max_tokens=max_tokens,
            temperature=temperature,
            stream=stream,
        )
        if stream:
            return self._stream_chat(output)
        return output.choices[0].message.content or ""

    async def _stream_chat(self, stream) -> AsyncIterator[str]:
        async for chunk in stream:
            if chunk.choices and chunk.choices[0].delta.content:
                yield chunk.choices[0].delta.content

    async def text_generation(
        self,
        prompt: str,
        model: str = "meta-llama/Meta-Llama-3-8B-Instruct",
        max_new_tokens: int = 512,
        temperature: float = 0.7,
    ) -> str:
        """Generate text from a prompt."""
        result = await self._client.text_generation(
            prompt, model=model,
            max_new_tokens=max_new_tokens, temperature=temperature,
        )
        return result

    # ── Image Generation ──────────────────────────────────────────

    async def text_to_image(
        self,
        prompt: str,
        model: str = "black-forest-labs/FLUX.1-schnell",
        width: int = 1024,
        height: int = 1024,
    ) -> Any:
        """Generate an image from text. Returns PIL.Image object."""
        image = await self._client.text_to_image(
            prompt, model=model, width=width, height=height,
        )
        return image

    # ── Text-to-Speech ────────────────────────────────────────────

    async def text_to_speech(
        self,
        text: str,
        model: str = "facebook/mms-tts-eng",
        output_path: str | None = None,
    ) -> bytes | str:
        """Generate speech audio from text. Returns audio bytes or saves to path."""
        audio_bytes = await self._client.text_to_speech(text, model=model)
        if output_path:
            Path(output_path).write_bytes(audio_bytes)
            return output_path
        return audio_bytes

    # ── Speech-to-Text (ASR) ──────────────────────────────────────

    async def transcribe(
        self,
        audio_path: str,
        model: str = "openai/whisper-large-v3",
    ) -> str:
        """Transcribe audio to text."""
        with open(audio_path, "rb") as f:
            result = await self._client.automatic_speech_recognition(f.read(), model=model)
        return result.text if hasattr(result, "text") else str(result)

    # ── Translation ───────────────────────────────────────────────

    async def translate(
        self,
        text: str,
        model: str = "Helsinki-NLP/opus-mt-en-fr",
        src_lang: str | None = None,
        tgt_lang: str | None = None,
    ) -> str:
        """Translate text between languages."""
        result = await self._client.translation(text, model=model)
        if isinstance(result, list) and result:
            return result[0].get("translation_text", str(result[0]))
        return result.translation_text if hasattr(result, "translation_text") else str(result)

    # ── Summarization ─────────────────────────────────────────────

    async def summarize(
        self,
        text: str,
        model: str = "facebook/bart-large-cnn",
        max_length: int = 150,
        min_length: int = 30,
    ) -> str:
        """Summarize text."""
        result = await self._client.summarization(
            text, model=model,
            parameters={"max_length": max_length, "min_length": min_length},
        )
        return result.summary_text if hasattr(result, "summary_text") else str(result)

    # ── Embeddings / Feature Extraction ───────────────────────────

    async def embed(
        self,
        text: str,
        model: str = "sentence-transformers/all-MiniLM-L6-v2",
    ) -> list[float]:
        """Generate embeddings for text."""
        result = await self._client.feature_extraction(text, model=model)
        # Result shape varies: could be [embedding] or [[embedding]]
        if isinstance(result, list):
            if result and isinstance(result[0], list):
                return result[0]
            return result
        return list(result)

    async def sentence_similarity(
        self,
        source: str,
        sentences: list[str],
        model: str = "sentence-transformers/all-MiniLM-L6-v2",
    ) -> list[float]:
        """Compute similarity between a source sentence and candidates."""
        result = await self._client.sentence_similarity(
            source, other=sentences, model=model,
        )
        return result if isinstance(result, list) else [result]

    # ── Classification ────────────────────────────────────────────

    async def classify(
        self,
        text: str,
        labels: list[str],
        model: str = "facebook/bart-large-mnli",
    ) -> dict:
        """Zero-shot text classification."""
        result = await self._client.zero_shot_classification(
            text, labels, model=model,
        )
        if isinstance(result, list) and result:
            return {"labels": [r.get("label", "") for r in result],
                    "scores": [r.get("score", 0) for r in result]}
        return {"labels": result.labels if hasattr(result, "labels") else [],
                "scores": result.scores if hasattr(result, "scores") else []}

    async def classify_image(
        self,
        image_path: str,
        model: str = "google/vit-base-patch16-224",
    ) -> list[dict]:
        """Classify an image into categories."""
        with open(image_path, "rb") as f:
            result = await self._client.image_classification(f.read(), model=model)
        return [{"label": r.label, "score": r.score} for r in result] if hasattr(result[0], "label") else result

    # ── Object Detection ──────────────────────────────────────────

    async def detect_objects(
        self,
        image_path: str,
        model: str = "facebook/detr-resnet-50",
    ) -> list[dict]:
        """Detect objects in an image."""
        with open(image_path, "rb") as f:
            result = await self._client.object_detection(f.read(), model=model)
        return [{"label": r.label, "score": round(r.score, 3), "box": vars(r.box) if hasattr(r, "box") else {}}
                for r in result] if result else []

    # ── Question Answering ────────────────────────────────────────

    async def answer_question(
        self,
        question: str,
        context: str,
        model: str = "deepset/roberta-base-squad2",
    ) -> dict:
        """Extractive question answering — find the answer span in context."""
        result = await self._client.question_answering(
            question=question, context=context, model=model,
        )
        return {"answer": result.answer if hasattr(result, "answer") else str(result),
                "score": result.score if hasattr(result, "score") else 0,
                "start": result.start if hasattr(result, "start") else 0,
                "end": result.end if hasattr(result, "end") else 0}

    async def visual_qa(
        self,
        image_path: str,
        question: str,
        model: str = "dandelin/vilt-b32-finetuned-vqa",
    ) -> list[dict]:
        """Visual question answering — answer questions about an image."""
        with open(image_path, "rb") as f:
            result = await self._client.visual_question_answering(
                image=f.read(), question=question, model=model,
            )
        return [{"answer": r.answer, "score": round(r.score, 3)} for r in result] if result else []

    # ── NLP Tasks ─────────────────────────────────────────────────

    async def ner(
        self,
        text: str,
        model: str = "dslim/bert-base-NER",
    ) -> list[dict]:
        """Named Entity Recognition — extract entities from text."""
        result = await self._client.token_classification(text, model=model)
        return [{"entity": r.entity_group if hasattr(r, "entity_group") else r.get("entity_group", ""),
                 "word": r.word if hasattr(r, "word") else r.get("word", ""),
                 "score": round(r.score if hasattr(r, "score") else r.get("score", 0), 3)}
                for r in result] if result else []

    async def fill_mask(
        self,
        text: str,
        model: str = "bert-base-uncased",
    ) -> list[dict]:
        """Fill in a [MASK] token in text."""
        result = await self._client.fill_mask(text, model=model)
        return [{"token": r.token_str if hasattr(r, "token_str") else r.get("token_str", ""),
                 "score": round(r.score if hasattr(r, "score") else r.get("score", 0), 3)}
                for r in result] if result else []

    async def image_to_text(
        self,
        image_path: str,
        model: str = "Salesforce/blip-image-captioning-large",
    ) -> str:
        """Generate a caption for an image."""
        with open(image_path, "rb") as f:
            result = await self._client.image_to_text(f.read(), model=model)
        return result.generated_text if hasattr(result, "generated_text") else str(result)

    # ── Model / Dataset Management (HfApi) ────────────────────────

    def list_models(
        self,
        query: str = "",
        task: str | None = None,
        sort: str = "downloads",
        limit: int = 20,
    ) -> list[dict]:
        """Search models on the Hub."""
        kwargs: dict[str, Any] = {"sort": sort, "limit": limit}
        if query:
            kwargs["search"] = query
        if task:
            kwargs["pipeline_tag"] = task
        models = self._api.list_models(**kwargs)
        return [
            {"id": m.id, "downloads": m.downloads, "likes": m.likes,
             "task": m.pipeline_tag or "", "updated": str(m.last_modified or "")}
            for m in models
        ]

    def model_info(self, model_id: str) -> dict:
        """Get detailed info about a model."""
        info = self._api.model_info(model_id)
        return {
            "id": info.id, "author": info.author or "",
            "task": info.pipeline_tag or "", "tags": info.tags or [],
            "downloads": info.downloads, "likes": info.likes,
            "library": info.library_name or "",
            "created": str(info.created_at or ""),
            "files": len(info.siblings or []),
        }

    def list_datasets(
        self,
        query: str = "",
        sort: str = "downloads",
        limit: int = 20,
    ) -> list[dict]:
        """Search datasets on the Hub."""
        kwargs: dict[str, Any] = {"sort": sort, "limit": limit}
        if query:
            kwargs["search"] = query
        datasets = self._api.list_datasets(**kwargs)
        return [
            {"id": d.id, "downloads": d.downloads, "likes": d.likes,
             "updated": str(d.last_modified or "")}
            for d in datasets
        ]


# ── Singleton ─────────────────────────────────────────────────────

_instance: HuggingFaceClient | None = None


def get_huggingface() -> HuggingFaceClient:
    """Get the singleton HuggingFaceClient."""
    global _instance
    if _instance is None:
        _instance = HuggingFaceClient()
    return _instance
