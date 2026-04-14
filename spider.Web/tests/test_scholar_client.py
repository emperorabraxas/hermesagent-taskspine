"""Tests for Semantic Scholar API client.

Covers: formatting budget, missing fields, routing logic,
failure resilience, /scholar fallback, and cache TTL.
"""
from __future__ import annotations

import asyncio
import time

import httpx
import pytest
import respx

from agentic_hub.core.scholar_client import ScholarClient
from agentic_hub.core.orchestrator import ACADEMIC_PATTERNS

# ── Fixtures ──────────────────────────────────────────────────────

SAMPLE_PAPER = {
    "paperId": "abc123",
    "title": "Attention Is All You Need",
    "year": 2017,
    "citationCount": 100000,
    "authors": [
        {"name": "Ashish Vaswani"},
        {"name": "Noam Shazeer"},
        {"name": "Niki Parmar"},
        {"name": "Jakob Uszkoreit"},
        {"name": "Llion Jones"},
    ],
    "abstract": "The dominant sequence transduction models are based on complex recurrent or convolutional neural networks. " * 10,  # Long abstract
    "openAccessPdf": {"url": "https://arxiv.org/pdf/1706.03762"},
    "externalIds": {"ArXiv": "1706.03762", "DOI": "10.5555/3295222.3295349"},
}

SAMPLE_PAPER_MINIMAL = {
    "paperId": "def456",
    "title": "Some Paper Without Details",
    "year": None,
    "citationCount": 0,
    "authors": [],
    "abstract": None,
    "openAccessPdf": None,
    "externalIds": None,
}

SAMPLE_AUTHOR = {
    "authorId": "123",
    "name": "Ashish Vaswani",
    "affiliations": ["Google Brain"],
    "paperCount": 50,
    "citationCount": 150000,
    "hIndex": 30,
}


@pytest.fixture
def client():
    return ScholarClient(api_key="")


@pytest.fixture
def client_with_key():
    return ScholarClient(api_key="test-key-123")


# ── build_context() budget tests ─────────────────────────────────

class TestBuildContext:
    def test_max_three_papers(self, client):
        papers = [SAMPLE_PAPER] * 5
        ctx = client.build_context(papers)
        # Should only have entries 1, 2, 3
        assert "1." in ctx
        assert "2." in ctx
        assert "3." in ctx
        assert "4." not in ctx

    def test_abstract_truncated_at_600(self, client):
        ctx = client.build_context([SAMPLE_PAPER])
        # The abstract in SAMPLE_PAPER is repeated text > 600 chars
        # Find the abstract line and check its length
        for line in ctx.split("\n"):
            if line.strip().startswith("Abstract:"):
                abstract_text = line.split("Abstract:")[1].strip()
                assert len(abstract_text) <= 600

    def test_authors_capped_at_three(self, client):
        ctx = client.build_context([SAMPLE_PAPER])
        assert "et al." in ctx
        # Should have exactly 3 named authors + et al.
        assert "Ashish Vaswani" in ctx
        assert "Noam Shazeer" in ctx
        assert "Niki Parmar" in ctx
        assert "Jakob Uszkoreit" not in ctx

    def test_ids_included(self, client):
        ctx = client.build_context([SAMPLE_PAPER])
        assert "ArXiv: 1706.03762" in ctx
        assert "DOI: 10.5555/3295222.3295349" in ctx
        assert "PDF: https://arxiv.org/pdf/1706.03762" in ctx

    def test_empty_papers_returns_empty(self, client):
        assert client.build_context([]) == ""


class TestBuildContextMissingFields:
    def test_no_abstract(self, client):
        ctx = client.build_context([SAMPLE_PAPER_MINIMAL])
        assert "Abstract:" not in ctx
        assert "Some Paper Without Details" in ctx

    def test_no_pdf_no_ids(self, client):
        ctx = client.build_context([SAMPLE_PAPER_MINIMAL])
        assert "ArXiv" not in ctx
        assert "DOI" not in ctx
        assert "PDF" not in ctx

    def test_no_authors(self, client):
        ctx = client.build_context([SAMPLE_PAPER_MINIMAL])
        assert "Authors:" not in ctx

    def test_no_year(self, client):
        ctx = client.build_context([SAMPLE_PAPER_MINIMAL])
        # Title should not have "()" or "(None)"
        assert "(None)" not in ctx


# ── format_search_results() ──────────────────────────────────────

class TestFormatSearchResults:
    def test_no_results(self, client):
        output = client.format_search_results([])
        assert "No papers found" in output

    def test_richer_output(self, client):
        output = client.format_search_results([SAMPLE_PAPER])
        assert "###" in output  # Markdown headers
        assert "100,000 citations" in output
        assert "Ashish Vaswani" in output

    def test_max_five_papers(self, client):
        papers = [SAMPLE_PAPER] * 8
        output = client.format_search_results(papers)
        assert "### 5." in output
        assert "### 6." not in output


# ── Routing logic (ACADEMIC_PATTERNS) ────────────────────────────

class TestAcademicPatterns:
    @pytest.mark.parametrize("query", [
        "find papers on transformer architecture",
        "what does the arxiv paper say about attention",
        "cite this DOI 10.5555/3295222",
        "vaswani et al 2017",
        "IEEE conference on neural networks",
        "literature review on LLMs",
        "h-index of this author",
        "peer review process",
        "search for preprint on diffusion models",
    ])
    def test_academic_queries_match(self, query):
        assert ACADEMIC_PATTERNS.search(query) is not None

    @pytest.mark.parametrize("query", [
        "what's the weather today",
        "write me a python function",
        "deploy to production",
        "how do I use docker",
        "buy bitcoin",
    ])
    def test_non_academic_queries_dont_match(self, query):
        assert ACADEMIC_PATTERNS.search(query) is None


# ── API calls with respx ─────────────────────────────────────────

@pytest.mark.asyncio
class TestSearchPapers:
    @respx.mock
    async def test_search_returns_results(self, client):
        respx.get("https://api.semanticscholar.org/graph/v1/paper/search").mock(
            return_value=httpx.Response(200, json={"data": [SAMPLE_PAPER]})
        )
        results = await client.search_papers("transformer attention")
        assert len(results) == 1
        assert results[0]["title"] == "Attention Is All You Need"

    @respx.mock
    async def test_search_empty_results(self, client):
        respx.get("https://api.semanticscholar.org/graph/v1/paper/search").mock(
            return_value=httpx.Response(200, json={"data": []})
        )
        results = await client.search_papers("nonexistent paper xyz")
        assert results == []

    @respx.mock
    async def test_search_timeout_returns_empty(self, client):
        respx.get("https://api.semanticscholar.org/graph/v1/paper/search").mock(
            side_effect=httpx.TimeoutException("timed out")
        )
        results = await client.search_papers("anything")
        assert results == []

    @respx.mock
    async def test_search_429_retries_once(self, client):
        route = respx.get("https://api.semanticscholar.org/graph/v1/paper/search")
        route.side_effect = [
            httpx.Response(429),
            httpx.Response(200, json={"data": [SAMPLE_PAPER]}),
        ]
        results = await client.search_papers("retry test")
        assert len(results) == 1
        assert route.call_count == 2

    @respx.mock
    async def test_search_500_retries_and_fails(self, client):
        respx.get("https://api.semanticscholar.org/graph/v1/paper/search").mock(
            return_value=httpx.Response(500)
        )
        results = await client.search_papers("server error")
        assert results == []


@pytest.mark.asyncio
class TestMatchPaper:
    @respx.mock
    async def test_match_found(self, client):
        respx.get("https://api.semanticscholar.org/graph/v1/paper/search/match").mock(
            return_value=httpx.Response(200, json={"data": [SAMPLE_PAPER]})
        )
        result = await client.match_paper("Attention Is All You Need")
        assert result is not None
        assert result["title"] == "Attention Is All You Need"

    @respx.mock
    async def test_match_not_found(self, client):
        respx.get("https://api.semanticscholar.org/graph/v1/paper/search/match").mock(
            return_value=httpx.Response(404)
        )
        result = await client.match_paper("Nonexistent Paper Title")
        assert result is None


@pytest.mark.asyncio
class TestGetPaper:
    @respx.mock
    async def test_get_by_id(self, client):
        respx.get("https://api.semanticscholar.org/graph/v1/paper/abc123").mock(
            return_value=httpx.Response(200, json=SAMPLE_PAPER)
        )
        result = await client.get_paper("abc123")
        assert result["title"] == "Attention Is All You Need"


@pytest.mark.asyncio
class TestSearchAuthors:
    @respx.mock
    async def test_search_authors(self, client):
        respx.get("https://api.semanticscholar.org/graph/v1/author/search").mock(
            return_value=httpx.Response(200, json={"data": [SAMPLE_AUTHOR]})
        )
        results = await client.search_authors("Vaswani")
        assert len(results) == 1
        assert results[0]["name"] == "Ashish Vaswani"


@pytest.mark.asyncio
class TestRecommendPapers:
    @respx.mock
    async def test_recommend(self, client):
        respx.post("https://api.semanticscholar.org/recommendations/v1/papers").mock(
            return_value=httpx.Response(200, json={"recommendedPapers": [SAMPLE_PAPER, SAMPLE_PAPER_MINIMAL]})
        )
        results = await client.recommend_papers(["abc123"])
        assert len(results) == 2


# ── Cache behavior ────────────────────────────────────────────────

class TestCache:
    def test_cache_expires(self, client):
        key = "test_key"
        client._cache_set(key, "value")
        assert client._cache_get(key) == "value"

        # Manually expire the entry
        client._cache[key] = (time.time() - 700, "value")  # 700s > 600s TTL
        assert client._cache_get(key) is None

    def test_cache_eviction(self, client):
        # Fill cache past limit
        for i in range(210):
            client._cache_set(f"key_{i}", f"val_{i}")
        assert len(client._cache) <= 200


@pytest.mark.asyncio
class TestCacheNetwork:
    @respx.mock
    async def test_cache_hit_skips_network(self, client):
        route = respx.get("https://api.semanticscholar.org/graph/v1/paper/search")
        route.mock(return_value=httpx.Response(200, json={"data": [SAMPLE_PAPER]}))

        # First call hits network
        r1 = await client.search_papers("cache test")
        assert len(r1) == 1
        assert route.call_count == 1

        # Second call should use cache
        r2 = await client.search_papers("cache test")
        assert len(r2) == 1
        assert route.call_count == 1  # No additional network call


# ── API key header ────────────────────────────────────────────────

class TestApiKey:
    def test_no_key_no_header(self, client):
        assert "x-api-key" not in client._client.headers

    def test_key_sets_header(self, client_with_key):
        assert client_with_key._client.headers["x-api-key"] == "test-key-123"


# ── Scholar command fallback logic ────────────────────────────────

@pytest.mark.asyncio
class TestScholarCommandFallback:
    @respx.mock
    async def test_match_hit_returns_single(self, client):
        """When exact match succeeds, returns that paper (no search needed)."""
        respx.get("https://api.semanticscholar.org/graph/v1/paper/search/match").mock(
            return_value=httpx.Response(200, json={"data": [SAMPLE_PAPER]})
        )
        paper = await client.match_paper("Attention Is All You Need")
        assert paper is not None
        output = client.format_search_results([paper])
        assert "Attention Is All You Need" in output

    @respx.mock
    async def test_match_miss_falls_back_to_search(self, client):
        """When match fails, search_papers provides results."""
        respx.get("https://api.semanticscholar.org/graph/v1/paper/search/match").mock(
            return_value=httpx.Response(404)
        )
        respx.get("https://api.semanticscholar.org/graph/v1/paper/search").mock(
            return_value=httpx.Response(200, json={"data": [SAMPLE_PAPER]})
        )
        paper = await client.match_paper("vague query")
        assert paper is None  # match failed

        results = await client.search_papers("vague query", limit=5)
        assert len(results) == 1
        output = client.format_search_results(results)
        assert "Attention Is All You Need" in output
