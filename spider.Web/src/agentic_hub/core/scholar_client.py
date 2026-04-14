"""Semantic Scholar API client — 200M+ academic papers via free HTTP API.

No SDK needed — pure httpx against the Graph API (paper/author search, details,
recommendations). Optional API key raises rate limit from 1 req/s to 100 req/s.

Spider allocation:
  - search_papers/match_paper/get_paper → Scholar (primary), Oracle (academic queries)
  - search_authors/get_author → Scholar
  - recommend_papers → Scholar
"""
from __future__ import annotations

import logging
import time
from typing import Any

import httpx

from agentic_hub.config import get_settings

logger = logging.getLogger(__name__)

# Fields requested per paper — balances detail vs. response size
_PAPER_FIELDS = "title,abstract,year,citationCount,authors,openAccessPdf,externalIds"
_AUTHOR_FIELDS = "name,affiliations,paperCount,citationCount,hIndex"

_CACHE_TTL = 600  # 10 minutes


class ScholarClient:
    """Async Semantic Scholar API client with TTL cache and prompt budget controls."""

    GRAPH_BASE = "https://api.semanticscholar.org/graph/v1"
    RECS_BASE = "https://api.semanticscholar.org/recommendations/v1"

    def __init__(self, api_key: str = ""):
        headers = {"User-Agent": "SpiderWeb/ScholarClient"}
        if api_key:
            headers["x-api-key"] = api_key
        self._client = httpx.AsyncClient(
            headers=headers,
            timeout=httpx.Timeout(10.0, connect=5.0),
        )
        self._cache: dict[str, tuple[float, Any]] = {}

    def _cache_key(self, *parts: str) -> str:
        return "|".join(str(p).lower().strip() for p in parts)

    def _cache_get(self, key: str) -> Any | None:
        if key in self._cache:
            ts, val = self._cache[key]
            if time.time() - ts < _CACHE_TTL:
                return val
            del self._cache[key]
        return None

    def _cache_set(self, key: str, val: Any) -> None:
        self._cache[key] = (time.time(), val)
        # Evict oldest if cache grows too large
        if len(self._cache) > 200:
            oldest = min(self._cache, key=lambda k: self._cache[k][0])
            del self._cache[oldest]

    async def _get(self, url: str, params: dict | None = None) -> dict | list | None:
        """GET with single retry on 429/5xx."""
        for attempt in range(2):
            try:
                resp = await self._client.get(url, params=params)
                if resp.status_code == 200:
                    return resp.json()
                if resp.status_code in (429, 500, 502, 503) and attempt == 0:
                    import asyncio
                    await asyncio.sleep(2)
                    continue
                logger.warning(f"Scholar API {resp.status_code}: {url}")
                return None
            except httpx.TimeoutException:
                if attempt == 0:
                    continue
                logger.warning(f"Scholar API timeout: {url}")
                return None
            except Exception as e:
                logger.warning(f"Scholar API error: {e}")
                return None
        return None

    async def _post(self, url: str, json_body: dict) -> dict | list | None:
        """POST with single retry on 429/5xx."""
        for attempt in range(2):
            try:
                resp = await self._client.post(url, json=json_body)
                if resp.status_code == 200:
                    return resp.json()
                if resp.status_code in (429, 500, 502, 503) and attempt == 0:
                    import asyncio
                    await asyncio.sleep(2)
                    continue
                logger.warning(f"Scholar API POST {resp.status_code}: {url}")
                return None
            except httpx.TimeoutException:
                if attempt == 0:
                    continue
                return None
            except Exception as e:
                logger.warning(f"Scholar API POST error: {e}")
                return None
        return None

    # ── Paper Search ──────────────────────────────────────────────

    async def search_papers(
        self,
        query: str,
        year: str = "",
        min_citations: int = 0,
        limit: int = 5,
    ) -> list[dict]:
        """Keyword search for papers. Returns up to `limit` results."""
        ck = self._cache_key("search", query, year, str(min_citations), str(limit))
        cached = self._cache_get(ck)
        if cached is not None:
            return cached

        params: dict[str, Any] = {
            "query": query,
            "limit": min(limit, 10),
            "fields": _PAPER_FIELDS,
        }
        if year:
            params["year"] = year
        if min_citations > 0:
            params["minCitationCount"] = min_citations

        data = await self._get(f"{self.GRAPH_BASE}/paper/search", params)
        if not data or "data" not in data:
            return []

        results = data["data"]
        self._cache_set(ck, results)
        return results

    async def match_paper(self, title: str) -> dict | None:
        """Exact title match — returns the single best matching paper."""
        ck = self._cache_key("match", title)
        cached = self._cache_get(ck)
        if cached is not None:
            return cached

        data = await self._get(
            f"{self.GRAPH_BASE}/paper/search/match",
            {"query": title, "fields": _PAPER_FIELDS},
        )
        if not data or "data" not in data:
            return None

        result = data["data"][0] if isinstance(data["data"], list) else data.get("data")
        if result:
            self._cache_set(ck, result)
        return result

    async def get_paper(self, paper_id: str) -> dict | None:
        """Get full paper details by Semantic Scholar ID, DOI, ArXiv ID, etc."""
        ck = self._cache_key("paper", paper_id)
        cached = self._cache_get(ck)
        if cached is not None:
            return cached

        data = await self._get(
            f"{self.GRAPH_BASE}/paper/{paper_id}",
            {"fields": _PAPER_FIELDS},
        )
        if data:
            self._cache_set(ck, data)
        return data

    # ── Author Search ─────────────────────────────────────────────

    async def search_authors(self, query: str, limit: int = 5) -> list[dict]:
        """Search for authors by name."""
        ck = self._cache_key("authors", query, str(limit))
        cached = self._cache_get(ck)
        if cached is not None:
            return cached

        data = await self._get(
            f"{self.GRAPH_BASE}/author/search",
            {"query": query, "limit": min(limit, 10), "fields": _AUTHOR_FIELDS},
        )
        if not data or "data" not in data:
            return []

        results = data["data"]
        self._cache_set(ck, results)
        return results

    async def get_author(self, author_id: str) -> dict | None:
        """Get author details by Semantic Scholar author ID."""
        ck = self._cache_key("author", author_id)
        cached = self._cache_get(ck)
        if cached is not None:
            return cached

        data = await self._get(
            f"{self.GRAPH_BASE}/author/{author_id}",
            {"fields": _AUTHOR_FIELDS},
        )
        if data:
            self._cache_set(ck, data)
        return data

    # ── Recommendations ───────────────────────────────────────────

    async def recommend_papers(
        self,
        positive_ids: list[str],
        negative_ids: list[str] | None = None,
        limit: int = 5,
    ) -> list[dict]:
        """Get paper recommendations from seed papers."""
        body: dict[str, Any] = {"positivePaperIds": positive_ids}
        if negative_ids:
            body["negativePaperIds"] = negative_ids

        data = await self._post(
            f"{self.RECS_BASE}/papers",
            body,
        )
        if not data or "recommendedPapers" not in data:
            return []

        return data["recommendedPapers"][:limit]

    # ── Context Formatting ────────────────────────────────────────

    @staticmethod
    def _format_authors(authors: list[dict], max_authors: int = 3) -> str:
        names = [a.get("name", "Unknown") for a in authors[:max_authors]]
        if len(authors) > max_authors:
            names.append("et al.")
        return ", ".join(names)

    @staticmethod
    def _format_ids(paper: dict) -> str:
        """Format DOI/ArXiv/PDF links when present."""
        parts = []
        ext = paper.get("externalIds") or {}
        if ext.get("ArXiv"):
            parts.append(f"ArXiv: {ext['ArXiv']}")
        if ext.get("DOI"):
            parts.append(f"DOI: {ext['DOI']}")
        pdf = paper.get("openAccessPdf") or {}
        if pdf.get("url"):
            parts.append(f"PDF: {pdf['url']}")
        return " | ".join(parts)

    def build_context(self, papers: list[dict], max_papers: int = 3) -> str:
        """Format papers as injected system context (tight budget).

        Hard limits: 3 papers, 600-char abstracts, 3 authors.
        This goes into the system prompt alongside RAG chunks.
        """
        if not papers:
            return ""

        lines = ["Academic papers relevant to this query:\n"]
        for i, p in enumerate(papers[:max_papers], 1):
            title = p.get("title", "Untitled")
            year = p.get("year", "")
            cites = p.get("citationCount", 0)
            authors = self._format_authors(p.get("authors") or [])
            abstract = (p.get("abstract") or "")[:600]
            ids = self._format_ids(p)

            lines.append(f"{i}. {title}" + (f" ({year})" if year else ""))
            if cites:
                lines.append(f"   Citations: {cites:,}")
            if authors:
                lines.append(f"   Authors: {authors}")
            if abstract:
                lines.append(f"   Abstract: {abstract}")
            if ids:
                lines.append(f"   {ids}")
            lines.append("")

        return "\n".join(lines)

    def format_search_results(self, papers: list[dict], max_papers: int = 5) -> str:
        """Format papers for /scholar command output (richer than context injection)."""
        if not papers:
            return "No papers found.\n"

        lines = [f"**Found {len(papers)} paper(s):**\n"]
        for i, p in enumerate(papers[:max_papers], 1):
            title = p.get("title", "Untitled")
            year = p.get("year", "")
            cites = p.get("citationCount", 0)
            authors = self._format_authors(p.get("authors") or [], max_authors=5)
            abstract = p.get("abstract") or ""
            ids = self._format_ids(p)

            lines.append(f"### {i}. {title}" + (f" ({year})" if year else ""))
            if cites:
                lines.append(f"📊 **{cites:,} citations**")
            if authors:
                lines.append(f"👤 {authors}")
            if abstract:
                lines.append(f"\n> {abstract}\n")
            if ids:
                lines.append(f"🔗 {ids}")
            lines.append("---")

        return "\n".join(lines)

    async def close(self):
        await self._client.aclose()


# ── Singleton ─────────────────────────────────────────────────────

_instance: ScholarClient | None = None


def get_scholar() -> ScholarClient:
    global _instance
    if _instance is None:
        settings = get_settings()
        _instance = ScholarClient(api_key=settings.semantic_scholar_api_key)
    return _instance
