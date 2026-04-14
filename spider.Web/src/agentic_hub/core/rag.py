"""RAG pipeline — index local files, embed chunks, retrieve context for Scholar.

Uses Ollama's /api/embed endpoint with mxbai-embed-large for embeddings.
Stores vectors in SQLite with cosine similarity search (no extra deps).
"""
from __future__ import annotations

import hashlib
import json
import logging
import math
import sqlite3
from pathlib import Path
from typing import AsyncIterator

import httpx

from agentic_hub.config import get_settings

logger = logging.getLogger(__name__)

RAG_DB = Path(__file__).parent.parent.parent.parent / "data" / "rag.db"
EMBED_MODEL = "mxbai-embed-large"
CHUNK_SIZE = 200  # tokens — mxbai-embed-large has 512 token context
CHUNK_OVERLAP = 30
TOP_K = 5

# File types we index
INDEXABLE = {
    ".py", ".js", ".ts", ".tsx", ".jsx", ".md", ".txt", ".yaml", ".yml",
    ".json", ".toml", ".cfg", ".ini", ".sh", ".bash", ".css", ".html",
    ".sql", ".rs", ".go", ".java", ".c", ".h", ".cpp", ".hpp",
    ".gdscript", ".gd", ".cls", ".trigger", ".apex",
}

SKIP_DIRS = {
    ".git", "node_modules", ".venv", "venv", "__pycache__", ".cache",
    ".ollama", ".local", "dist", "build", ".next", ".mypy_cache",
}


def _init_db():
    """Create the RAG database and tables."""
    RAG_DB.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(RAG_DB))
    conn.execute("""CREATE TABLE IF NOT EXISTS chunks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        file_path TEXT NOT NULL,
        file_hash TEXT NOT NULL,
        chunk_index INTEGER NOT NULL,
        content TEXT NOT NULL,
        embedding TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        UNIQUE(file_path, chunk_index)
    )""")
    conn.execute("""CREATE INDEX IF NOT EXISTS idx_chunks_path ON chunks(file_path)""")
    conn.execute("""CREATE INDEX IF NOT EXISTS idx_chunks_hash ON chunks(file_hash)""")
    conn.commit()
    return conn


def _chunk_text(text: str, chunk_size: int = CHUNK_SIZE, overlap: int = CHUNK_OVERLAP) -> list[str]:
    """Split text into overlapping chunks by approximate token count."""
    # Rough approximation: 1 token ≈ 4 chars
    char_size = chunk_size * 4
    char_overlap = overlap * 4
    chunks = []
    start = 0
    while start < len(text):
        end = start + char_size
        chunk = text[start:end]
        if chunk.strip():
            chunks.append(chunk.strip())
        start = end - char_overlap
    return chunks


def _file_hash(path: Path) -> str:
    """Quick hash of file contents for change detection."""
    return hashlib.md5(path.read_bytes()).hexdigest()[:12]


async def _embed(texts: list[str], base_url: str | None = None) -> list[list[float]]:
    """Get embeddings from Ollama, one at a time for reliability."""
    url = (base_url or get_settings().ollama_base_url) + "/api/embed"
    all_embeddings = []
    async with httpx.AsyncClient(timeout=120) as client:
        for text in texts:
            resp = await client.post(url, json={
                "model": EMBED_MODEL,
                "input": text,
                "keep_alive": "30s",  # Short TTL — embed model must vacate VRAM for chat models
            })
            resp.raise_for_status()
            data = resp.json()
            embs = data.get("embeddings", [])
            if embs:
                all_embeddings.append(embs[0])
            else:
                # Fallback: zero vector
                all_embeddings.append([0.0] * 1024)
    return all_embeddings


def _cosine_sim(a: list[float], b: list[float]) -> float:
    """Cosine similarity between two vectors."""
    dot = sum(x * y for x, y in zip(a, b))
    norm_a = math.sqrt(sum(x * x for x in a))
    norm_b = math.sqrt(sum(x * x for x in b))
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return dot / (norm_a * norm_b)


class RAGPipeline:
    """Index files and retrieve relevant context for queries."""

    def __init__(self):
        self._conn = _init_db()

    async def index_directory(self, directory: str | Path, force: bool = False) -> dict:
        """Index all indexable files in a directory. Returns stats."""
        directory = Path(directory)
        if not directory.exists():
            return {"error": f"Directory not found: {directory}"}

        files_found = 0
        files_indexed = 0
        chunks_created = 0
        files_skipped = 0

        for path in directory.rglob("*"):
            # Skip non-files and non-indexable
            if not path.is_file():
                continue
            if path.suffix.lower() not in INDEXABLE:
                continue
            # Skip excluded dirs
            if any(part in SKIP_DIRS for part in path.parts):
                continue
            # Skip large files (>100KB)
            if path.stat().st_size > 100_000:
                continue

            files_found += 1
            fhash = _file_hash(path)

            # Check if already indexed with same hash
            if not force:
                existing = self._conn.execute(
                    "SELECT 1 FROM chunks WHERE file_path=? AND file_hash=? LIMIT 1",
                    (str(path), fhash)
                ).fetchone()
                if existing:
                    files_skipped += 1
                    continue

            # Remove old chunks for this file
            self._conn.execute("DELETE FROM chunks WHERE file_path=?", (str(path),))

            # Read and chunk
            try:
                text = path.read_text(errors="ignore")
            except Exception:
                continue

            chunks = _chunk_text(text)
            if not chunks:
                continue

            # Embed all chunks
            try:
                embeddings = await _embed(chunks)
            except Exception as e:
                logger.warning(f"Embedding failed for {path}: {e}")
                continue

            # Store
            for i, (chunk, emb) in enumerate(zip(chunks, embeddings)):
                self._conn.execute(
                    "INSERT OR REPLACE INTO chunks (file_path, file_hash, chunk_index, content, embedding) VALUES (?,?,?,?,?)",
                    (str(path), fhash, i, chunk, json.dumps(emb))
                )

            files_indexed += 1
            chunks_created += len(chunks)

        self._conn.commit()
        return {
            "directory": str(directory),
            "files_found": files_found,
            "files_indexed": files_indexed,
            "files_skipped": files_skipped,
            "chunks_created": chunks_created,
        }

    async def query(self, question: str, top_k: int = TOP_K) -> list[dict]:
        """Find the most relevant chunks for a question."""
        # Embed the question
        try:
            q_embeddings = await _embed([question])
        except Exception as e:
            logger.error(f"Query embedding failed: {e}")
            return []

        if not q_embeddings:
            return []

        q_vec = q_embeddings[0]

        # Load all chunks and score (brute force — fine for <100k chunks)
        rows = self._conn.execute(
            "SELECT file_path, chunk_index, content, embedding FROM chunks"
        ).fetchall()

        scored = []
        for file_path, chunk_idx, content, emb_json in rows:
            emb = json.loads(emb_json)
            score = _cosine_sim(q_vec, emb)
            scored.append({
                "file": file_path,
                "chunk": chunk_idx,
                "content": content,
                "score": round(score, 4),
            })

        scored.sort(key=lambda x: x["score"], reverse=True)
        return scored[:top_k]

    def get_stats(self) -> dict:
        """Get index statistics."""
        total_chunks = self._conn.execute("SELECT COUNT(*) FROM chunks").fetchone()[0]
        total_files = self._conn.execute("SELECT COUNT(DISTINCT file_path) FROM chunks").fetchone()[0]
        return {"total_chunks": total_chunks, "total_files": total_files}

    def build_context(self, results: list[dict], max_chars: int = 4000) -> str:
        """Build a context string from RAG results for injection into prompts."""
        if not results:
            return ""
        parts = ["## Relevant context from local files:\n"]
        chars = 0
        for r in results:
            entry = f"\n### {r['file']} (chunk {r['chunk']}, relevance: {r['score']})\n```\n{r['content']}\n```\n"
            if chars + len(entry) > max_chars:
                break
            parts.append(entry)
            chars += len(entry)
        return "".join(parts)
