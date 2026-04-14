"""Built-in tools — wrap existing spider.Web capabilities as schema-defined tools."""
from __future__ import annotations

import asyncio
import logging
import time
from pathlib import Path
from typing import Any

from agentic_hub.core.tools.base import BaseTool, ToolParameter, ToolResult

logger = logging.getLogger(__name__)


async def _try_providers(providers: list[tuple[str, Any]], **kwargs) -> tuple[str, Any]:
    """Try cloud providers in order until one succeeds.

    providers: [(name, async_callable), ...] — each callable(**kwargs) returns result.
    Returns (provider_name, result) or raises RuntimeError if all fail.
    """
    errors = []
    for name, fn in providers:
        try:
            result = await fn(**kwargs)
            return name, result
        except Exception as e:
            errors.append(f"{name}: {e}")
    raise RuntimeError(f"All providers failed: {'; '.join(errors)}")


class ShellTool(BaseTool):
    """Execute shell commands in the persistent sandbox."""

    @property
    def name(self) -> str:
        return "shell"

    @property
    def description(self) -> str:
        return (
            "Execute a shell command on the user's machine. Commands run in a persistent "
            "bash session (cd and env vars persist between calls). Dangerous commands are "
            "blocked. Privileged commands (sudo, systemctl) require user approval."
        )

    @property
    def parameters(self) -> list[ToolParameter]:
        return [
            ToolParameter("command", "string", "The shell command to execute"),
            ToolParameter("cwd", "string", "Working directory (optional, persists)", required=False),
        ]

    async def execute(self, **kwargs: Any) -> ToolResult:
        from agentic_hub.core.sandbox import execute
        import re
        command = kwargs.get("command", "")
        cwd = kwargs.get("cwd")
        if not command.strip():
            return ToolResult(output="", success=False, error="Empty command")
        start = time.monotonic()
        result = await execute(command, cwd=cwd)
        elapsed_ms = int((time.monotonic() - start) * 1000)

        # Some common "control flow" commands intentionally use non-zero exit codes
        # (e.g., `killall foo` => rc=1 when no process exists). Treat those benign
        # cases as success so spiders don't derail.
        cmd = command.strip()
        stderr_lc = (result.stderr or "").lower()
        stdout_lc = (result.stdout or "").lower()
        benign_nonzero = False
        if result.returncode == 1:
            if re.match(r"^(killall|pkill)\b", cmd) and ("no process found" in stderr_lc or "no process found" in stdout_lc):
                benign_nonzero = True
            elif re.match(r"^pgrep\b", cmd) and not (result.stdout or "").strip():
                benign_nonzero = True

        output_parts = []
        if result.stdout:
            output_parts.append(result.stdout)
        if result.stderr and result.returncode != 0 and not benign_nonzero:
            output_parts.append(f"STDERR: {result.stderr[:500]}")
        if result.timed_out:
            output_parts.append("TIMED OUT")
        output = "\n".join(output_parts) or "(no output)"
        return ToolResult(
            output=output,
            success=(result.returncode == 0) or benign_nonzero,
            error=None if ((result.returncode == 0) or benign_nonzero) else (result.stderr[:200] if result.returncode != 0 else None),
            metadata={"returncode": result.returncode, "latency_ms": elapsed_ms},
        )


class ReadFileTool(BaseTool):
    """Read file contents from the filesystem."""

    @property
    def name(self) -> str:
        return "read_file"

    @property
    def description(self) -> str:
        return (
            "Read the contents of a file. Path-restricted to project directories. "
            "Returns up to 50KB of content. Use for reading source code, configs, "
            "logs, and data files."
        )

    @property
    def parameters(self) -> list[ToolParameter]:
        return [
            ToolParameter("path", "string", "Absolute or relative path to the file"),
        ]

    async def execute(self, **kwargs: Any) -> ToolResult:
        from agentic_hub.core.sandbox import read_file
        path = kwargs.get("path", "")
        if not path:
            return ToolResult(output="", success=False, error="No path specified")
        content = await read_file(path)
        is_error = content.startswith("Access denied") or content.startswith("Error reading")
        return ToolResult(
            output=content,
            success=not is_error,
            error=content if is_error else None,
            metadata={"path": path, "bytes": len(content)},
        )


class WriteFileTool(BaseTool):
    """Write content to a file."""

    @property
    def name(self) -> str:
        return "write_file"

    @property
    def description(self) -> str:
        return (
            "Write content to a file. Path-restricted to project directories. "
            "Creates the file if it doesn't exist, overwrites if it does. "
            "Use for creating or modifying source code, configs, and data files."
        )

    @property
    def parameters(self) -> list[ToolParameter]:
        return [
            ToolParameter("path", "string", "Absolute or relative path to write"),
            ToolParameter("content", "string", "The content to write to the file"),
        ]

    async def execute(self, **kwargs: Any) -> ToolResult:
        from agentic_hub.core.sandbox import write_file
        path = kwargs.get("path", "")
        content = kwargs.get("content", "")
        if not path:
            return ToolResult(output="", success=False, error="No path specified")
        result = await write_file(path, content)
        is_error = result.startswith("Access denied") or result.startswith("Error writing")
        return ToolResult(
            output=result,
            success=not is_error,
            error=result if is_error else None,
            metadata={"path": path, "bytes_written": len(content)},
        )


class ListDirectoryTool(BaseTool):
    """List contents of a directory."""

    @property
    def name(self) -> str:
        return "list_dir"

    @property
    def description(self) -> str:
        return (
            "List files and directories at a given path. Returns file names, sizes, "
            "and permissions. Use to explore directory structure before reading files."
        )

    @property
    def parameters(self) -> list[ToolParameter]:
        return [
            ToolParameter("path", "string", "Directory path to list (default: current dir)", required=False, default="."),
        ]

    async def execute(self, **kwargs: Any) -> ToolResult:
        from agentic_hub.core.sandbox import list_dir
        path = kwargs.get("path", ".")
        content = await list_dir(path)
        is_error = "No such file or directory" in content or "Permission denied" in content
        return ToolResult(
            output=content,
            success=not is_error,
            error=content if is_error else None,
            metadata={"path": path},
        )


class WebFetchTool(BaseTool):
    """Fetch content from a URL."""

    @property
    def name(self) -> str:
        return "web_fetch"

    @property
    def description(self) -> str:
        return (
            "Fetch the content of a web URL via HTTP GET. Returns the response body "
            "(text or JSON). Use for retrieving documentation, API data, or web pages. "
            "Timeout: 30 seconds. Max response: 50KB."
        )

    @property
    def parameters(self) -> list[ToolParameter]:
        return [
            ToolParameter("url", "string", "The URL to fetch"),
        ]

    async def execute(self, **kwargs: Any) -> ToolResult:
        import httpx
        url = kwargs.get("url", "")
        if not url:
            return ToolResult(output="", success=False, error="No URL specified")
        if not url.startswith(("http://", "https://")):
            return ToolResult(output="", success=False, error="URL must start with http:// or https://")
        start = time.monotonic()
        try:
            async with httpx.AsyncClient(timeout=30, follow_redirects=True) as client:
                resp = await client.get(url, headers={"User-Agent": "SpiderWeb/1.0"})
                elapsed_ms = int((time.monotonic() - start) * 1000)
                body = resp.text[:50000]
                return ToolResult(
                    output=body,
                    success=resp.status_code < 400,
                    error=f"HTTP {resp.status_code}" if resp.status_code >= 400 else None,
                    metadata={"status": resp.status_code, "latency_ms": elapsed_ms, "bytes": len(body)},
                )
        except httpx.TimeoutException:
            return ToolResult(output="", success=False, error="Request timed out (30s)")
        except Exception as e:
            return ToolResult(output="", success=False, error=str(e)[:200])


class RAGSearchTool(BaseTool):
    """Search the local knowledge base using RAG."""

    @property
    def name(self) -> str:
        return "rag_search"

    @property
    def description(self) -> str:
        return (
            "Search the local RAG knowledge base for relevant code, documentation, or "
            "data. Uses vector similarity to find the most relevant chunks from indexed "
            "files. Returns matched content with source file paths."
        )

    @property
    def parameters(self) -> list[ToolParameter]:
        return [
            ToolParameter("query", "string", "Natural language search query"),
            ToolParameter("top_k", "integer", "Number of results to return (default: 5)", required=False, default=5),
        ]

    async def execute(self, **kwargs: Any) -> ToolResult:
        query = kwargs.get("query", "")
        top_k = kwargs.get("top_k", 5)
        if not query:
            return ToolResult(output="", success=False, error="No query specified")
        try:
            from agentic_hub.core.rag import RAGPipeline
            rag = RAGPipeline()
            results = await rag.query(query, top_k=top_k)
            if not results:
                return ToolResult(output="No relevant results found.", success=True, metadata={"chunks": 0})
            context = rag.build_context(results)
            return ToolResult(
                output=context,
                success=True,
                metadata={"chunks": len(results)},
            )
        except Exception as e:
            return ToolResult(output="", success=False, error=f"RAG query failed: {e}")


class PythonEvalTool(BaseTool):
    """Evaluate a Python expression safely."""

    @property
    def name(self) -> str:
        return "python_eval"

    @property
    def description(self) -> str:
        return (
            "Evaluate a Python expression and return the result. Useful for calculations, "
            "data transformations, and string operations. Restricted to safe operations — "
            "no file I/O, no imports, no exec/eval nesting."
        )

    @property
    def parameters(self) -> list[ToolParameter]:
        return [
            ToolParameter("expression", "string", "Python expression to evaluate"),
        ]

    async def execute(self, **kwargs: Any) -> ToolResult:
        expression = kwargs.get("expression", "")
        if not expression:
            return ToolResult(output="", success=False, error="No expression specified")

        # Block dangerous builtins
        BLOCKED = {"exec", "eval", "compile", "__import__", "open", "input",
                    "breakpoint", "exit", "quit", "globals", "locals", "vars",
                    "setattr", "delattr", "getattr"}
        for blocked in BLOCKED:
            if blocked in expression:
                return ToolResult(output="", success=False, error=f"Blocked: {blocked} not allowed")

        safe_globals = {"__builtins__": {
            "len": len, "range": range, "int": int, "float": float, "str": str,
            "bool": bool, "list": list, "dict": dict, "set": set, "tuple": tuple,
            "min": min, "max": max, "sum": sum, "abs": abs, "round": round,
            "sorted": sorted, "reversed": reversed, "enumerate": enumerate,
            "zip": zip, "map": map, "filter": filter, "any": any, "all": all,
            "isinstance": isinstance, "type": type, "repr": repr,
            "True": True, "False": False, "None": None,
        }}

        try:
            result = eval(expression, safe_globals, {})
            return ToolResult(output=str(result), success=True)
        except Exception as e:
            return ToolResult(output="", success=False, error=f"Eval error: {e}")


class EntitySearchTool(BaseTool):
    """Search the entity knowledge graph for cross-session knowledge."""

    @property
    def name(self) -> str:
        return "entity_search"

    @property
    def description(self) -> str:
        return (
            "Search the entity knowledge graph for information about people, projects, "
            "stocks, tools, or concepts remembered from previous conversations. "
            "Returns entity details, relationships, and recent mentions."
        )

    @property
    def parameters(self) -> list[ToolParameter]:
        return [
            ToolParameter("query", "string", "Entity name or keyword to search for"),
        ]

    async def execute(self, **kwargs: Any) -> ToolResult:
        query = kwargs.get("query", "")
        if not query:
            return ToolResult(output="", success=False, error="No query specified")

        try:
            from agentic_hub.core.entity_memory import get_entity_memory
            em = get_entity_memory()

            # Direct lookup
            entity = await em.query_entity(query)
            if entity:
                lines = [f"**{entity['name']}** ({entity['type']})"]
                if entity.get("description"):
                    lines.append(f"Description: {entity['description']}")
                lines.append(f"Mentions: {entity['mention_count']}")
                if entity.get("relations"):
                    lines.append("Relations:")
                    for rel in entity["relations"][:10]:
                        if "target" in rel:
                            lines.append(f"  → {rel['type']} → {rel['target']}")
                        elif "source" in rel:
                            lines.append(f"  ← {rel['source']} → {rel['type']}")
                return ToolResult(output="\n".join(lines), success=True)

            # No exact match — try related entities
            related = await em.get_related_entities(query, depth=1)
            if related:
                lines = [f"No exact match for '{query}', but found related:"]
                for r in related[:5]:
                    lines.append(f"- **{r['name']}** ({r['type']}): {r.get('description', '')}")
                return ToolResult(output="\n".join(lines), success=True)

            return ToolResult(output=f"No entities found matching '{query}'", success=True)

        except Exception as e:
            return ToolResult(output="", success=False, error=f"Entity search error: {e}")


class EditFileTool(BaseTool):
    """Surgical file editing — replace specific text without rewriting the whole file."""

    @property
    def name(self) -> str:
        return "edit_file"

    @property
    def description(self) -> str:
        return (
            "Edit a file by replacing specific text. Provide the exact text to find "
            "and the replacement text. Fails if the text is not found or is ambiguous. "
            "Use replace_all=true to replace all occurrences."
        )

    @property
    def parameters(self) -> list[ToolParameter]:
        return [
            ToolParameter("path", "string", "Path to the file to edit", required=True),
            ToolParameter("old_text", "string", "Exact text to find and replace", required=True),
            ToolParameter("new_text", "string", "Replacement text", required=True),
            ToolParameter("replace_all", "boolean", "Replace all occurrences (default: false)"),
        ]

    async def execute(self, **kwargs: Any) -> ToolResult:
        from agentic_hub.core.sandbox import edit_file
        path = kwargs.get("path", "")
        old_text = kwargs.get("old_text", "")
        new_text = kwargs.get("new_text", "")
        replace_all = kwargs.get("replace_all", False)
        if not path or not old_text:
            return ToolResult(output="", success=False, error="path and old_text required")
        result = await edit_file(path, old_text, new_text, replace_all)
        is_error = result.startswith("Error")
        return ToolResult(output=result, success=not is_error, error=result if is_error else None)


class GlobTool(BaseTool):
    """Find files by glob pattern across the codebase."""

    @property
    def name(self) -> str:
        return "glob"

    @property
    def description(self) -> str:
        return (
            "Find files matching a glob pattern. Supports ** for recursive matching. "
            "Examples: '**/*.py' finds all Python files, 'src/**/*.ts' finds TypeScript in src/."
        )

    @property
    def parameters(self) -> list[ToolParameter]:
        return [
            ToolParameter("pattern", "string", "Glob pattern (e.g. **/*.py, src/**/*.ts)", required=True),
            ToolParameter("path", "string", "Base directory to search in (default: current project)"),
        ]

    async def execute(self, **kwargs: Any) -> ToolResult:
        from agentic_hub.core.sandbox import glob_files
        pattern = kwargs.get("pattern", "")
        path = kwargs.get("path", ".")
        if not pattern:
            return ToolResult(output="", success=False, error="pattern required")
        result = await glob_files(pattern, path)
        is_error = result.startswith("Glob error") or result.startswith("Access denied")
        return ToolResult(output=result, success=not is_error, error=result if is_error else None)


class GrepTool(BaseTool):
    """Search file contents with regex."""

    @property
    def name(self) -> str:
        return "grep"

    @property
    def description(self) -> str:
        return (
            "Search file contents using regex patterns. Returns matching lines with "
            "file path, line number, and content. Supports case-insensitive search "
            "and file type filtering."
        )

    @property
    def parameters(self) -> list[ToolParameter]:
        return [
            ToolParameter("pattern", "string", "Regex pattern to search for", required=True),
            ToolParameter("path", "string", "Directory or file to search in (default: current project)"),
            ToolParameter("case_sensitive", "boolean", "Case-sensitive search (default: true)"),
            ToolParameter("file_glob", "string", "Filter files by glob (e.g. *.py, *.ts)"),
        ]

    async def execute(self, **kwargs: Any) -> ToolResult:
        from agentic_hub.core.sandbox import grep_search
        pattern = kwargs.get("pattern", "")
        path = kwargs.get("path", ".")
        case = kwargs.get("case_sensitive", True)
        file_glob = kwargs.get("file_glob", "")
        if not pattern:
            return ToolResult(output="", success=False, error="pattern required")
        result = await grep_search(pattern, path, case, file_glob)
        is_error = result.startswith("Search error") or result.startswith("Access denied")
        return ToolResult(output=result, success=not is_error, error=result if is_error else None)


class GitTool(BaseTool):
    """Git version control operations."""

    @property
    def name(self) -> str:
        return "git"

    @property
    def description(self) -> str:
        return (
            "Run git commands: status, diff, add, commit, push, pull, log, branch, "
            "checkout, stash, show, remote, fetch, tag. Destructive operations "
            "(force-push, reset --hard, clean -f) are blocked."
        )

    @property
    def parameters(self) -> list[ToolParameter]:
        return [
            ToolParameter("command", "string", "Git subcommand: status, diff, add, commit, push, log, branch, etc.", required=True),
            ToolParameter("args", "string", "Additional arguments (e.g. '-m \"commit message\"', '--oneline -10', 'src/file.py')"),
            ToolParameter("cwd", "string", "Working directory (default: spider.Web project root)"),
        ]

    async def execute(self, **kwargs: Any) -> ToolResult:
        from agentic_hub.core.sandbox import git_cmd
        command = kwargs.get("command", "")
        args = kwargs.get("args", "")
        cwd = kwargs.get("cwd", "")
        if not command:
            return ToolResult(output="", success=False, error="command required")
        result = await git_cmd(command, args, cwd)
        is_error = result.startswith("Blocked") or result.startswith("Git error") or "not allowed" in result
        return ToolResult(output=result, success=not is_error, error=result if is_error else None)


class WebSearchTool(BaseTool):
    """Search the web using Claude's built-in web search."""

    @property
    def name(self) -> str:
        return "web_search"

    @property
    def description(self) -> str:
        return (
            "Search the web for current information using Claude's built-in web search. "
            "Returns cited results. Use for real-time data, news, prices, documentation."
        )

    @property
    def parameters(self) -> list[ToolParameter]:
        return [
            ToolParameter("query", "string", "Search query", required=True),
        ]

    async def execute(self, **kwargs: Any) -> ToolResult:
        query = kwargs.get("query", "")
        if not query:
            return ToolResult(output="", success=False, error="query required")
        try:
            from agentic_hub.core.cloud_client import get_cloud_client
            client = get_cloud_client("anthropic")
            if not client:
                return ToolResult(output="", success=False, error="Anthropic not configured")
            result = await client.web_search(query)
            return ToolResult(output=result, success=True)
        except Exception as e:
            return ToolResult(output="", success=False, error=f"Web search error: {e}")


class CodeExecTool(BaseTool):
    """Execute Python code in Anthropic's sandboxed environment."""

    @property
    def name(self) -> str:
        return "cloud_python"

    @property
    def description(self) -> str:
        return (
            "Execute Python code in Claude's sandboxed cloud environment. "
            "Has numpy, pandas, matplotlib. Use for data analysis, calculations, "
            "and generating charts. Results returned as text or images."
        )

    @property
    def parameters(self) -> list[ToolParameter]:
        return [
            ToolParameter("code", "string", "Python code to execute", required=True),
        ]

    async def execute(self, **kwargs: Any) -> ToolResult:
        code = kwargs.get("code", "")
        if not code:
            return ToolResult(output="", success=False, error="code required")
        try:
            from agentic_hub.core.cloud_client import get_cloud_client
            client = get_cloud_client("anthropic")
            if not client:
                return ToolResult(output="", success=False, error="Anthropic not configured")
            # Use code execution tool via messages API
            resp = await client._client.messages.create(
                model="claude-sonnet-4-6-20250514",
                max_tokens=4096,
                tools=[{"type": "code_execution_20250522"}],
                messages=[{"role": "user", "content": f"Run this Python code and return the output:\n```python\n{code}\n```"}],
            )
            parts = []
            for block in resp.content:
                if block.type == "text":
                    parts.append(block.text)
                elif hasattr(block, "output"):
                    parts.append(str(block.output))
            return ToolResult(output="\n".join(parts) or "Code executed", success=True)
        except Exception as e:
            return ToolResult(output="", success=False, error=f"Code exec error: {e}")


# ── Cloud-Powered Tools ──────────────────────────────────────────────
# These wrap the cloud client methods built across 9 integrations.
# Multi-provider tools try local first, then cheapest cloud, then best.


def _get_settings():
    from agentic_hub.config import get_settings
    return get_settings()


class VisionTool(BaseTool):
    """Analyze images using vision-capable models (multi-provider)."""

    @property
    def name(self) -> str:
        return "vision"

    @property
    def description(self) -> str:
        return (
            "Analyze an image with a text prompt. Describe what you see, extract text, "
            "read charts, identify objects. Accepts base64 image data or a URL."
        )

    @property
    def parameters(self) -> list[ToolParameter]:
        return [
            ToolParameter("prompt", "string", "What to analyze in the image", required=True),
            ToolParameter("image", "string", "Base64-encoded image data or URL", required=True),
            ToolParameter("source_type", "string", "Image source type",
                          required=False, enum=["base64", "url"], default="base64"),
        ]

    async def execute(self, **kwargs: Any) -> ToolResult:
        prompt = kwargs.get("prompt", "")
        image = kwargs.get("image", "")
        source_type = kwargs.get("source_type", "base64")
        if not prompt or not image:
            return ToolResult(output="", success=False, error="prompt and image required")

        settings = _get_settings()
        providers: list[tuple[str, Any]] = []

        # Ollama local vision (free)
        try:
            from agentic_hub.core.ollama_client import get_ollama
            ollama = get_ollama()

            async def _ollama_vision(**kw):
                return await ollama.analyze_image(
                    prompt=kw["prompt"], image_data=kw["image"], model="gemma3"
                )
            providers.append(("ollama", _ollama_vision))
        except Exception:
            pass

        # Anthropic vision
        if settings.anthropic_api_key:
            async def _anthropic_vision(**kw):
                from agentic_hub.core.cloud_client import get_anthropic
                return await get_anthropic().vision(
                    prompt=kw["prompt"], image_data=kw["image"],
                    source_type=kw.get("source_type", "base64"),
                )
            providers.append(("anthropic", _anthropic_vision))

        # OpenAI vision
        if settings.openai_api_key:
            async def _openai_vision(**kw):
                from agentic_hub.core.cloud_client import get_openai
                return await get_openai().vision(
                    prompt=kw["prompt"], image_url=kw["image"],
                )
            providers.append(("openai", _openai_vision))

        # Google vision
        if getattr(settings, "google_api_key", ""):
            async def _google_vision(**kw):
                from agentic_hub.core.cloud_client import get_google
                if kw.get("source_type") == "url":
                    return await get_google().vision_url(prompt=kw["prompt"], url=kw["image"])
                return await get_google().vision(prompt=kw["prompt"], image_data=kw["image"])
            providers.append(("google", _google_vision))

        # HuggingFace image captioning (free)
        async def _hf_vision(**kw):
            from agentic_hub.core.hf_client import get_huggingface
            hf = get_huggingface()
            # HF image_to_text needs a file path; if base64, skip
            if kw.get("source_type") == "url":
                return f"[HF vision requires local image. Query: {kw['prompt']}]"
            return f"[HF vision: use classify_image or image_to_text for local files]"
        # Only add as last resort — HF vision is limited compared to cloud
        providers.append(("huggingface", _hf_vision))

        if not providers:
            return ToolResult(output="", success=False, error="No vision provider available")

        try:
            provider, result = await _try_providers(
                providers, prompt=prompt, image=image, source_type=source_type,
            )
            output = result if isinstance(result, str) else str(result)
            return ToolResult(output=output, success=True, metadata={"provider": provider})
        except RuntimeError as e:
            return ToolResult(output="", success=False, error=str(e))


class PDFTool(BaseTool):
    """Analyze PDF documents with citations (Anthropic)."""

    @property
    def name(self) -> str:
        return "analyze_pdf"

    @property
    def description(self) -> str:
        return (
            "Analyze a PDF document — extract text, read tables, understand charts, "
            "answer questions about the content. Returns cited results."
        )

    @property
    def parameters(self) -> list[ToolParameter]:
        return [
            ToolParameter("prompt", "string", "Question about the PDF", required=True),
            ToolParameter("pdf_data", "string", "Base64-encoded PDF or URL", required=True),
            ToolParameter("source_type", "string", "PDF source type",
                          required=False, enum=["base64", "url"], default="base64"),
        ]

    async def execute(self, **kwargs: Any) -> ToolResult:
        prompt = kwargs.get("prompt", "")
        pdf_data = kwargs.get("pdf_data", "")
        source_type = kwargs.get("source_type", "base64")
        if not prompt or not pdf_data:
            return ToolResult(output="", success=False, error="prompt and pdf_data required")
        try:
            from agentic_hub.core.cloud_client import get_anthropic
            settings = _get_settings()
            if not settings.anthropic_api_key:
                return ToolResult(output="", success=False, error="Anthropic API key required for PDF analysis")
            result = await get_anthropic().analyze_pdf(
                prompt=prompt, pdf_data=pdf_data, source_type=source_type, citations=True,
            )
            text = result.get("text", "")
            citations = result.get("citations", [])
            output = text
            if citations:
                output += f"\n\n[{len(citations)} citation(s) found]"
            return ToolResult(output=output, success=True, metadata={"citations": len(citations)})
        except Exception as e:
            return ToolResult(output="", success=False, error=f"PDF analysis error: {e}")


class ThinkDeepTool(BaseTool):
    """Extended reasoning — model thinks step-by-step before answering (multi-provider)."""

    @property
    def name(self) -> str:
        return "think_deep"

    @property
    def description(self) -> str:
        return (
            "Extended reasoning for complex problems — math, strategy, analysis, debugging. "
            "The model reasons step-by-step internally, then provides a final answer. "
            "Use for hard problems that need careful thought."
        )

    @property
    def parameters(self) -> list[ToolParameter]:
        return [
            ToolParameter("prompt", "string", "The problem to think through", required=True),
            ToolParameter("system", "string", "Optional system context", required=False),
        ]

    async def execute(self, **kwargs: Any) -> ToolResult:
        prompt = kwargs.get("prompt", "")
        system = kwargs.get("system", "")
        if not prompt:
            return ToolResult(output="", success=False, error="prompt required")

        settings = _get_settings()
        providers: list[tuple[str, Any]] = []

        # DeepSeek R1 (cheapest reasoning)
        if getattr(settings, "deepseek_api_key", ""):
            async def _deepseek_think(**kw):
                from agentic_hub.core.cloud_client import get_deepseek
                return await get_deepseek().think(
                    messages=[{"role": "user", "content": kw["prompt"]}],
                )
            providers.append(("deepseek", _deepseek_think))

        # Anthropic extended thinking
        if settings.anthropic_api_key:
            async def _anthropic_think(**kw):
                from agentic_hub.core.cloud_client import get_anthropic
                result = await get_anthropic().think_and_respond(
                    messages=[{"role": "user", "content": kw["prompt"]}],
                    system=kw.get("system", ""),
                )
                return f"**Thinking:**\n{result['thinking']}\n\n**Answer:**\n{result['response']}"
            providers.append(("anthropic", _anthropic_think))

        # Google Gemini thinking
        if getattr(settings, "google_api_key", ""):
            async def _google_think(**kw):
                from agentic_hub.core.cloud_client import get_google
                return await get_google().think(
                    messages=[{"role": "user", "content": kw["prompt"]}],
                )
            providers.append(("google", _google_think))

        # Ollama local thinking (deepseek-r1 if available)
        try:
            from agentic_hub.core.ollama_client import get_ollama
            ollama = get_ollama()

            async def _ollama_think(**kw):
                return await ollama.think(
                    model="deepseek-r1:7b",
                    messages=[{"role": "user", "content": kw["prompt"]}],
                )
            providers.append(("ollama", _ollama_think))
        except Exception:
            pass

        if not providers:
            return ToolResult(output="", success=False, error="No thinking provider available")

        try:
            provider, result = await _try_providers(providers, prompt=prompt, system=system)
            output = result if isinstance(result, str) else str(result)
            return ToolResult(output=output, success=True, metadata={"provider": provider})
        except RuntimeError as e:
            return ToolResult(output="", success=False, error=str(e))


class StructuredOutputTool(BaseTool):
    """Get guaranteed JSON output matching a schema (multi-provider)."""

    @property
    def name(self) -> str:
        return "structured_output"

    @property
    def description(self) -> str:
        return (
            "Extract structured data from text as guaranteed JSON matching a schema. "
            "Provide a JSON schema and the model returns data conforming to it. "
            "Use for data extraction, classification, entity recognition."
        )

    @property
    def parameters(self) -> list[ToolParameter]:
        return [
            ToolParameter("prompt", "string", "Text to extract structured data from", required=True),
            ToolParameter("schema", "string", "JSON schema as a string (must be valid JSON)", required=True),
        ]

    async def execute(self, **kwargs: Any) -> ToolResult:
        prompt = kwargs.get("prompt", "")
        schema_str = kwargs.get("schema", "")
        if not prompt or not schema_str:
            return ToolResult(output="", success=False, error="prompt and schema required")
        try:
            import json as _json
            schema = _json.loads(schema_str)
        except Exception:
            return ToolResult(output="", success=False, error="schema must be valid JSON")

        settings = _get_settings()

        # Try Anthropic (most reliable structured output via forced tool use)
        if settings.anthropic_api_key:
            try:
                from agentic_hub.core.cloud_client import get_anthropic
                result = await get_anthropic().structured_output(
                    messages=[{"role": "user", "content": prompt}], schema=schema,
                )
                return ToolResult(
                    output=_json.dumps(result, indent=2), success=True,
                    metadata={"provider": "anthropic"},
                )
            except Exception as e:
                logger.debug(f"Anthropic structured_output failed: {e}")

        # Try OpenAI
        if settings.openai_api_key:
            try:
                from agentic_hub.core.cloud_client import get_openai
                result = await get_openai().structured_output(
                    messages=[{"role": "user", "content": prompt}], schema=schema,
                )
                return ToolResult(
                    output=_json.dumps(result, indent=2), success=True,
                    metadata={"provider": "openai"},
                )
            except Exception as e:
                logger.debug(f"OpenAI structured_output failed: {e}")

        # Try Ollama
        try:
            from agentic_hub.core.ollama_client import get_ollama
            result = await get_ollama().structured_output(
                messages=[{"role": "user", "content": prompt}], schema=schema,
            )
            return ToolResult(
                output=_json.dumps(result, indent=2) if isinstance(result, dict) else str(result),
                success=True, metadata={"provider": "ollama"},
            )
        except Exception as e:
            logger.debug(f"Ollama structured_output failed: {e}")

        return ToolResult(output="", success=False, error="No structured output provider available")


class ImageGenTool(BaseTool):
    """Generate images from text prompts (multi-provider)."""

    @property
    def name(self) -> str:
        return "generate_image"

    @property
    def description(self) -> str:
        return (
            "Generate an image from a text description. Returns a URL to the generated image. "
            "Supports photorealistic, artistic, and abstract styles."
        )

    @property
    def parameters(self) -> list[ToolParameter]:
        return [
            ToolParameter("prompt", "string", "Description of the image to generate", required=True),
            ToolParameter("size", "string", "Image size",
                          required=False, enum=["1024x1024", "1792x1024", "1024x1792"], default="1024x1024"),
        ]

    async def execute(self, **kwargs: Any) -> ToolResult:
        prompt = kwargs.get("prompt", "")
        size = kwargs.get("size", "1024x1024")
        if not prompt:
            return ToolResult(output="", success=False, error="prompt required")

        settings = _get_settings()

        # OpenAI (best quality — gpt-image-1)
        if settings.openai_api_key:
            try:
                from agentic_hub.core.cloud_client import get_openai
                urls = await get_openai().generate_image(prompt=prompt, size=size)
                if urls:
                    return ToolResult(
                        output=f"Image generated: {urls[0]}", success=True,
                        metadata={"provider": "openai", "url": urls[0]},
                    )
            except Exception as e:
                logger.debug(f"OpenAI image gen failed: {e}")

        # Google Imagen
        if getattr(settings, "google_api_key", ""):
            try:
                from agentic_hub.core.cloud_client import get_google
                result = await get_google().generate_image(prompt=prompt)
                return ToolResult(
                    output=f"Image generated via Imagen: {result}", success=True,
                    metadata={"provider": "google"},
                )
            except Exception as e:
                logger.debug(f"Google image gen failed: {e}")

        # xAI Aurora
        if getattr(settings, "xai_api_key", ""):
            try:
                from agentic_hub.core.cloud_client import get_xai
                result = await asyncio.to_thread(get_xai().xai_generate_image, prompt)
                return ToolResult(
                    output=f"Image generated via Aurora: {result}", success=True,
                    metadata={"provider": "xai"},
                )
            except Exception as e:
                logger.debug(f"xAI image gen failed: {e}")

        # HuggingFace FLUX (free tier)
        try:
            from agentic_hub.core.hf_client import get_huggingface
            hf = get_huggingface()
            image = await hf.text_to_image(prompt=prompt)
            if image:
                data_dir = Path(__file__).parent.parent.parent.parent / "data" / "images"
                data_dir.mkdir(parents=True, exist_ok=True)
                fname = f"hf_{int(time.time())}.png"
                path = data_dir / fname
                image.save(str(path))
                return ToolResult(
                    output=f"Image generated via FLUX: /api/images/{fname}", success=True,
                    metadata={"provider": "huggingface", "path": str(path)},
                )
        except Exception as e:
            logger.debug(f"HF image gen failed: {e}")

        return ToolResult(output="", success=False, error="No image generation provider available")


class TTSTool(BaseTool):
    """Convert text to speech audio (multi-provider)."""

    @property
    def name(self) -> str:
        return "text_to_speech"

    @property
    def description(self) -> str:
        return (
            "Convert text to spoken audio. Generates an MP3 file. "
            "Use for reading documents aloud, creating audio content, or accessibility."
        )

    @property
    def parameters(self) -> list[ToolParameter]:
        return [
            ToolParameter("text", "string", "Text to convert to speech", required=True),
            ToolParameter("voice", "string", "Voice to use",
                          required=False, enum=["alloy", "coral", "nova", "onyx", "shimmer", "fable", "echo"],
                          default="alloy"),
        ]

    async def execute(self, **kwargs: Any) -> ToolResult:
        text = kwargs.get("text", "")
        voice = kwargs.get("voice", "alloy")
        if not text:
            return ToolResult(output="", success=False, error="text required")

        settings = _get_settings()
        data_dir = Path(__file__).parent.parent.parent.parent / "data" / "audio"
        data_dir.mkdir(parents=True, exist_ok=True)
        filename = f"tts_{int(time.time())}.mp3"
        output_path = str(data_dir / filename)

        # OpenAI TTS (gpt-4o-mini-tts)
        if settings.openai_api_key:
            try:
                from agentic_hub.core.cloud_client import get_openai
                path = await get_openai().tts(text=text, output_path=output_path, voice=voice)
                return ToolResult(
                    output=f"Audio generated: {path}", success=True,
                    metadata={"provider": "openai", "path": path, "voice": voice},
                )
            except Exception as e:
                logger.debug(f"OpenAI TTS failed: {e}")

        # Google TTS
        if getattr(settings, "google_api_key", ""):
            try:
                from agentic_hub.core.cloud_client import get_google
                result = await get_google().tts(text=text, output_path=output_path)
                return ToolResult(
                    output=f"Audio generated: {result}", success=True,
                    metadata={"provider": "google", "path": output_path},
                )
            except Exception as e:
                logger.debug(f"Google TTS failed: {e}")

        return ToolResult(output="", success=False, error="No TTS provider available")


class TranscribeTool(BaseTool):
    """Transcribe audio to text using Whisper (OpenAI)."""

    @property
    def name(self) -> str:
        return "transcribe"

    @property
    def description(self) -> str:
        return (
            "Transcribe an audio file to text. Supports MP3, MP4, WAV, WEBM, M4A. "
            "Returns the transcribed text content."
        )

    @property
    def parameters(self) -> list[ToolParameter]:
        return [
            ToolParameter("audio_path", "string", "Path to the audio file", required=True),
            ToolParameter("language", "string", "Language code (ISO-639-1, e.g. 'en')", required=False),
        ]

    async def execute(self, **kwargs: Any) -> ToolResult:
        audio_path = kwargs.get("audio_path", "")
        language = kwargs.get("language")
        if not audio_path:
            return ToolResult(output="", success=False, error="audio_path required")
        if not Path(audio_path).exists():
            return ToolResult(output="", success=False, error=f"File not found: {audio_path}")
        try:
            settings = _get_settings()
            if not settings.openai_api_key:
                return ToolResult(output="", success=False, error="OpenAI API key required for transcription")
            from agentic_hub.core.cloud_client import get_openai
            text = await get_openai().transcribe(audio_path=audio_path, language=language)
            return ToolResult(output=text, success=True, metadata={"provider": "openai"})
        except Exception as e:
            return ToolResult(output="", success=False, error=f"Transcription error: {e}")


class ModerateTool(BaseTool):
    """Check text for harmful content (OpenAI Moderation)."""

    @property
    def name(self) -> str:
        return "moderate"

    @property
    def description(self) -> str:
        return (
            "Check text for harmful content — hate speech, harassment, self-harm, sexual content, "
            "violence. Returns flagged categories and confidence scores. "
            "Use as a safety gate on untrusted content."
        )

    @property
    def parameters(self) -> list[ToolParameter]:
        return [
            ToolParameter("text", "string", "Text to check for harmful content", required=True),
        ]

    async def execute(self, **kwargs: Any) -> ToolResult:
        text = kwargs.get("text", "")
        if not text:
            return ToolResult(output="", success=False, error="text required")
        try:
            settings = _get_settings()
            if not settings.openai_api_key:
                return ToolResult(output="", success=False, error="OpenAI API key required for moderation")
            from agentic_hub.core.cloud_client import get_openai
            import json as _json
            result = await get_openai().moderate(text=text)
            flagged = result.get("flagged", False)
            output = f"Flagged: {flagged}\n"
            if flagged:
                cats = {k: v for k, v in result.get("categories", {}).items() if v}
                output += f"Categories: {', '.join(cats.keys())}\n"
            scores = result.get("scores", {})
            top_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)[:5]
            output += "Top scores: " + ", ".join(f"{k}: {v:.3f}" for k, v in top_scores)
            return ToolResult(output=output, success=True, metadata={"flagged": flagged})
        except Exception as e:
            return ToolResult(output="", success=False, error=f"Moderation error: {e}")


class EmbedTool(BaseTool):
    """Generate vector embeddings for text (multi-provider)."""

    @property
    def name(self) -> str:
        return "embed"

    @property
    def description(self) -> str:
        return (
            "Generate vector embeddings for text. Use for semantic similarity, "
            "clustering, or feeding into vector databases. Returns embedding dimension count."
        )

    @property
    def parameters(self) -> list[ToolParameter]:
        return [
            ToolParameter("text", "string", "Text to embed", required=True),
        ]

    async def execute(self, **kwargs: Any) -> ToolResult:
        text = kwargs.get("text", "")
        if not text:
            return ToolResult(output="", success=False, error="text required")

        settings = _get_settings()

        # Ollama local embeddings (free)
        try:
            from agentic_hub.core.ollama_client import get_ollama
            embedding = await get_ollama().embed(text)
            if embedding:
                dims = len(embedding) if isinstance(embedding, list) else 0
                return ToolResult(
                    output=f"Embedding generated ({dims} dimensions)", success=True,
                    metadata={"provider": "ollama", "dimensions": dims},
                )
        except Exception:
            pass

        # OpenAI embeddings
        if settings.openai_api_key:
            try:
                from agentic_hub.core.cloud_client import get_openai
                result = await get_openai().embed(text)
                dims = len(result[0]) if result else 0
                return ToolResult(
                    output=f"Embedding generated ({dims} dimensions)", success=True,
                    metadata={"provider": "openai", "dimensions": dims},
                )
            except Exception as e:
                logger.debug(f"OpenAI embed failed: {e}")

        # Google embeddings
        if getattr(settings, "google_api_key", ""):
            try:
                from agentic_hub.core.cloud_client import get_google
                result = await get_google().embed(text)
                dims = len(result) if isinstance(result, list) else 0
                return ToolResult(
                    output=f"Embedding generated ({dims} dimensions)", success=True,
                    metadata={"provider": "google", "dimensions": dims},
                )
            except Exception as e:
                logger.debug(f"Google embed failed: {e}")

        # HuggingFace embeddings (free, sentence-transformers)
        try:
            from agentic_hub.core.hf_client import get_huggingface
            result = await get_huggingface().embed(text)
            dims = len(result) if isinstance(result, list) else 0
            return ToolResult(
                output=f"Embedding generated ({dims} dimensions)", success=True,
                metadata={"provider": "huggingface", "dimensions": dims},
            )
        except Exception as e:
            logger.debug(f"HF embed failed: {e}")

        return ToolResult(output="", success=False, error="No embedding provider available")


class XSearchTool(BaseTool):
    """Search X/Twitter for real-time social intelligence (xAI)."""

    @property
    def name(self) -> str:
        return "x_search"

    @property
    def description(self) -> str:
        return (
            "Search X/Twitter for real-time posts, sentiment, breaking news, and social media intelligence. "
            "Returns cited results from X. Use for market sentiment, trending topics, real-time events."
        )

    @property
    def parameters(self) -> list[ToolParameter]:
        return [
            ToolParameter("query", "string", "Search query for X/Twitter", required=True),
        ]

    async def execute(self, **kwargs: Any) -> ToolResult:
        query = kwargs.get("query", "")
        if not query:
            return ToolResult(output="", success=False, error="query required")
        try:
            settings = _get_settings()
            if not getattr(settings, "xai_api_key", ""):
                return ToolResult(output="", success=False, error="xAI API key required for X search")
            from agentic_hub.core.cloud_client import get_xai
            xai = get_xai()
            result = await asyncio.to_thread(xai.x_search, query)
            content = result.get("content", "")
            citations = result.get("citations", "")
            output = content
            if citations:
                output += f"\n\nCitations: {citations}"
            return ToolResult(output=output, success=True, metadata={"provider": "xai"})
        except Exception as e:
            return ToolResult(output="", success=False, error=f"X search error: {e}")


class CodeFillTool(BaseTool):
    """Fill-in-the-middle code completion (DeepSeek FIM)."""

    @property
    def name(self) -> str:
        return "code_fill"

    @property
    def description(self) -> str:
        return (
            "Fill in missing code between a prefix and suffix. Given code before and after a gap, "
            "generate the code that belongs in between. Use for auto-completion, code repair."
        )

    @property
    def parameters(self) -> list[ToolParameter]:
        return [
            ToolParameter("prefix", "string", "Code before the gap", required=True),
            ToolParameter("suffix", "string", "Code after the gap", required=True),
        ]

    async def execute(self, **kwargs: Any) -> ToolResult:
        prefix = kwargs.get("prefix", "")
        suffix = kwargs.get("suffix", "")
        if not prefix:
            return ToolResult(output="", success=False, error="prefix required")
        try:
            settings = _get_settings()
            if not getattr(settings, "deepseek_api_key", ""):
                return ToolResult(output="", success=False, error="DeepSeek API key required for FIM")
            from agentic_hub.core.cloud_client import get_deepseek
            result = await get_deepseek().fim(prompt=prefix, suffix=suffix)
            return ToolResult(output=result, success=True, metadata={"provider": "deepseek"})
        except Exception as e:
            return ToolResult(output="", success=False, error=f"Code fill error: {e}")


class DBSearchTool(BaseTool):
    """Full-text search across conversation history and entities (PostgreSQL)."""

    @property
    def name(self) -> str:
        return "db_search"

    @property
    def description(self) -> str:
        return (
            "Search conversation history and entities using full-text search. "
            "Finds messages, entities, and knowledge from past interactions. "
            "Use for recalling previous conversations, finding mentioned topics."
        )

    @property
    def parameters(self) -> list[ToolParameter]:
        return [
            ToolParameter("query", "string", "Search query", required=True),
            ToolParameter("search_type", "string", "What to search",
                          required=False, enum=["messages", "entities", "all"], default="all"),
            ToolParameter("limit", "integer", "Max results per type", required=False, default=10),
        ]

    async def execute(self, **kwargs: Any) -> ToolResult:
        query = kwargs.get("query", "")
        search_type = kwargs.get("search_type", "all")
        limit = kwargs.get("limit", 10)
        if not query:
            return ToolResult(output="", success=False, error="query required")
        try:
            from agentic_hub.core.pg_service import get_pg_service
            pg = await get_pg_service()
            if not pg.connected:
                return ToolResult(output="", success=False, error="PostgreSQL not connected")

            import json as _json
            results = {}
            if search_type in ("all", "messages"):
                results["messages"] = await pg.search_messages(query, limit=limit)
            if search_type in ("all", "entities"):
                results["entities"] = await pg.search_entities(query, limit=limit)

            total = sum(len(v) for v in results.values())
            output = f"Found {total} result(s):\n"
            for category, items in results.items():
                if items:
                    output += f"\n--- {category.upper()} ---\n"
                    for item in items[:5]:
                        output += f"  {_json.dumps(item, default=str)[:200]}\n"
            return ToolResult(output=output, success=True, metadata={"total": total})
        except Exception as e:
            return ToolResult(output="", success=False, error=f"DB search error: {e}")


class LeaderboardTool(BaseTool):
    """View spider XP leaderboards and rankings (Redis)."""

    @property
    def name(self) -> str:
        return "leaderboard"

    @property
    def description(self) -> str:
        return (
            "View spider rankings — XP earned, tasks completed, tokens used, or trade P&L. "
            "Returns the top performers with scores."
        )

    @property
    def parameters(self) -> list[ToolParameter]:
        return [
            ToolParameter("board", "string", "Which leaderboard to view",
                          required=False, enum=["xp", "tasks", "trades", "usage"], default="xp"),
            ToolParameter("top_n", "integer", "Number of top entries", required=False, default=10),
        ]

    async def execute(self, **kwargs: Any) -> ToolResult:
        board = kwargs.get("board", "xp")
        top_n = kwargs.get("top_n", 10)
        try:
            from agentic_hub.core.redis_service import get_redis_service
            redis = await get_redis_service()
            if not redis.connected:
                return ToolResult(output="", success=False, error="Redis not connected")
            entries = await redis.get_leaderboard(f"leaderboard:{board}", top_n=top_n)
            if not entries:
                return ToolResult(output=f"No {board} leaderboard data yet", success=True)
            output = f"🏆 {board.upper()} Leaderboard:\n"
            for i, entry in enumerate(entries, 1):
                member = entry.get("member", "?")
                score = entry.get("score", 0)
                output += f"  #{i} {member}: {score}\n"
            return ToolResult(output=output, success=True, metadata={"board": board, "entries": len(entries)})
        except Exception as e:
            return ToolResult(output="", success=False, error=f"Leaderboard error: {e}")


# ── Hugging Face Hub Tools ───────────────────────────────────────────


class HFSearchModelsTool(BaseTool):
    """Search 900K+ models on Hugging Face Hub."""

    @property
    def name(self) -> str:
        return "hf_search_models"

    @property
    def description(self) -> str:
        return (
            "Search Hugging Face Hub for ML models. Find models by name, task "
            "(text-generation, image-classification, translation, etc.), or keyword. "
            "Returns model IDs, download counts, and tasks."
        )

    @property
    def parameters(self) -> list[ToolParameter]:
        return [
            ToolParameter("query", "string", "Search query or model name", required=True),
            ToolParameter("task", "string", "Filter by task (text-generation, image-classification, etc.)",
                          required=False),
            ToolParameter("limit", "integer", "Max results", required=False, default=10),
        ]

    async def execute(self, **kwargs: Any) -> ToolResult:
        query = kwargs.get("query", "")
        task = kwargs.get("task")
        limit = kwargs.get("limit", 10)
        if not query:
            return ToolResult(output="", success=False, error="query required")
        try:
            from agentic_hub.core.hf_client import get_huggingface
            hf = get_huggingface()
            models = hf.list_models(query=query, task=task, limit=limit)
            if not models:
                return ToolResult(output=f"No models found for '{query}'", success=True)
            output = f"Found {len(models)} model(s):\n"
            for m in models:
                output += f"  {m['id']} — {m['task']} ({m['downloads']:,} downloads, {m['likes']} likes)\n"
            return ToolResult(output=output, success=True, metadata={"count": len(models)})
        except Exception as e:
            return ToolResult(output="", success=False, error=f"HF search error: {e}")


class HFSummarizeTool(BaseTool):
    """Summarize text using Hugging Face models."""

    @property
    def name(self) -> str:
        return "hf_summarize"

    @property
    def description(self) -> str:
        return (
            "Summarize long text into a concise version using ML models. "
            "Good for compressing articles, documents, or research into key points."
        )

    @property
    def parameters(self) -> list[ToolParameter]:
        return [
            ToolParameter("text", "string", "Text to summarize", required=True),
            ToolParameter("max_length", "integer", "Max summary length in tokens", required=False, default=150),
        ]

    async def execute(self, **kwargs: Any) -> ToolResult:
        text = kwargs.get("text", "")
        max_length = kwargs.get("max_length", 150)
        if not text:
            return ToolResult(output="", success=False, error="text required")
        try:
            from agentic_hub.core.hf_client import get_huggingface
            hf = get_huggingface()
            result = await hf.summarize(text=text, max_length=max_length)
            return ToolResult(output=result, success=True, metadata={"provider": "huggingface"})
        except Exception as e:
            return ToolResult(output="", success=False, error=f"Summarization error: {e}")


class HFTranslateTool(BaseTool):
    """Translate text between languages using Hugging Face models."""

    @property
    def name(self) -> str:
        return "hf_translate"

    @property
    def description(self) -> str:
        return (
            "Translate text from one language to another. "
            "Specify a model for the language pair (e.g. Helsinki-NLP/opus-mt-en-fr for English to French)."
        )

    @property
    def parameters(self) -> list[ToolParameter]:
        return [
            ToolParameter("text", "string", "Text to translate", required=True),
            ToolParameter("model", "string", "Translation model (e.g. Helsinki-NLP/opus-mt-en-fr)",
                          required=False, default="Helsinki-NLP/opus-mt-en-fr"),
        ]

    async def execute(self, **kwargs: Any) -> ToolResult:
        text = kwargs.get("text", "")
        model = kwargs.get("model", "Helsinki-NLP/opus-mt-en-fr")
        if not text:
            return ToolResult(output="", success=False, error="text required")
        try:
            from agentic_hub.core.hf_client import get_huggingface
            hf = get_huggingface()
            result = await hf.translate(text=text, model=model)
            return ToolResult(output=result, success=True, metadata={"provider": "huggingface", "model": model})
        except Exception as e:
            return ToolResult(output="", success=False, error=f"Translation error: {e}")


class HFClassifyTool(BaseTool):
    """Zero-shot text classification using Hugging Face models."""

    @property
    def name(self) -> str:
        return "hf_classify"

    @property
    def description(self) -> str:
        return (
            "Classify text into categories WITHOUT training data. Provide any labels you want. "
            "Uses zero-shot classification — works for sentiment, topic, intent, or any custom labels."
        )

    @property
    def parameters(self) -> list[ToolParameter]:
        return [
            ToolParameter("text", "string", "Text to classify", required=True),
            ToolParameter("labels", "string", "Comma-separated labels (e.g. 'positive,negative,neutral')", required=True),
        ]

    async def execute(self, **kwargs: Any) -> ToolResult:
        text = kwargs.get("text", "")
        labels_str = kwargs.get("labels", "")
        if not text or not labels_str:
            return ToolResult(output="", success=False, error="text and labels required")
        labels = [l.strip() for l in labels_str.split(",")]
        try:
            from agentic_hub.core.hf_client import get_huggingface
            hf = get_huggingface()
            result = await hf.classify(text=text, labels=labels)
            output = "Classification:\n"
            for label, score in zip(result.get("labels", []), result.get("scores", [])):
                output += f"  {label}: {score:.3f}\n"
            return ToolResult(output=output, success=True, metadata={"provider": "huggingface"})
        except Exception as e:
            return ToolResult(output="", success=False, error=f"Classification error: {e}")


class HFNERTool(BaseTool):
    """Extract named entities from text (people, organizations, locations)."""

    @property
    def name(self) -> str:
        return "hf_ner"

    @property
    def description(self) -> str:
        return (
            "Extract named entities from text — people, organizations, locations, dates. "
            "Uses NER (Named Entity Recognition) models."
        )

    @property
    def parameters(self) -> list[ToolParameter]:
        return [
            ToolParameter("text", "string", "Text to extract entities from", required=True),
        ]

    async def execute(self, **kwargs: Any) -> ToolResult:
        text = kwargs.get("text", "")
        if not text:
            return ToolResult(output="", success=False, error="text required")
        try:
            from agentic_hub.core.hf_client import get_huggingface
            hf = get_huggingface()
            entities = await hf.ner(text=text)
            if not entities:
                return ToolResult(output="No entities found", success=True)
            output = f"Found {len(entities)} entities:\n"
            for e in entities:
                output += f"  [{e['entity']}] {e['word']} (confidence: {e['score']})\n"
            return ToolResult(output=output, success=True, metadata={"count": len(entities)})
        except Exception as e:
            return ToolResult(output="", success=False, error=f"NER error: {e}")


class HFQATool(BaseTool):
    """Extractive question answering — find answers in text."""

    @property
    def name(self) -> str:
        return "hf_qa"

    @property
    def description(self) -> str:
        return (
            "Answer a question by finding the relevant span in a given context text. "
            "Provide both the question and the text that contains the answer."
        )

    @property
    def parameters(self) -> list[ToolParameter]:
        return [
            ToolParameter("question", "string", "The question to answer", required=True),
            ToolParameter("context", "string", "The text containing the answer", required=True),
        ]

    async def execute(self, **kwargs: Any) -> ToolResult:
        question = kwargs.get("question", "")
        context = kwargs.get("context", "")
        if not question or not context:
            return ToolResult(output="", success=False, error="question and context required")
        try:
            from agentic_hub.core.hf_client import get_huggingface
            hf = get_huggingface()
            result = await hf.answer_question(question=question, context=context)
            output = f"Answer: {result['answer']}\nConfidence: {result['score']:.3f}"
            return ToolResult(output=output, success=True, metadata={"provider": "huggingface"})
        except Exception as e:
            return ToolResult(output="", success=False, error=f"QA error: {e}")


# ── Admin / Management Tools ─────────────────────────────────────────
# Batch jobs, fine-tuning, file management, vector stores, model management


class BatchJobTool(BaseTool):
    """Create and check batch processing jobs (50% cost discount)."""

    @property
    def name(self) -> str:
        return "batch_job"

    @property
    def description(self) -> str:
        return (
            "Create or check a batch processing job for bulk requests at 50% cost. "
            "Provide 'create' action with requests, or 'check' action with a batch_id."
        )

    @property
    def parameters(self) -> list[ToolParameter]:
        return [
            ToolParameter("action", "string", "Action to perform", required=True,
                          enum=["create", "check"]),
            ToolParameter("batch_id", "string", "Batch ID to check (for 'check' action)", required=False),
            ToolParameter("requests_json", "string", "JSON array of requests (for 'create' action)", required=False),
        ]

    async def execute(self, **kwargs: Any) -> ToolResult:
        action = kwargs.get("action", "")
        settings = _get_settings()
        try:
            if action == "check":
                batch_id = kwargs.get("batch_id", "")
                if not batch_id:
                    return ToolResult(output="", success=False, error="batch_id required for check")
                if settings.anthropic_api_key:
                    from agentic_hub.core.cloud_client import get_anthropic
                    result = await get_anthropic().get_batch(batch_id)
                elif settings.openai_api_key:
                    from agentic_hub.core.cloud_client import get_openai
                    result = await get_openai().get_batch(batch_id)
                else:
                    return ToolResult(output="", success=False, error="No API key configured")
                import json as _json
                return ToolResult(output=_json.dumps(result, indent=2), success=True)
            elif action == "create":
                requests_json = kwargs.get("requests_json", "")
                if not requests_json:
                    return ToolResult(output="", success=False, error="requests_json required for create")
                import json as _json
                requests = _json.loads(requests_json)
                if settings.anthropic_api_key:
                    from agentic_hub.core.cloud_client import get_anthropic
                    result = await get_anthropic().create_batch(requests)
                elif settings.openai_api_key:
                    from agentic_hub.core.cloud_client import get_openai
                    result = await get_openai().create_batch(requests)
                else:
                    return ToolResult(output="", success=False, error="No API key configured")
                return ToolResult(output=_json.dumps(result, indent=2), success=True, metadata={"provider": "batch"})
            else:
                return ToolResult(output="", success=False, error="action must be 'create' or 'check'")
        except Exception as e:
            return ToolResult(output="", success=False, error=f"Batch error: {e}")


class FileManagerTool(BaseTool):
    """Upload, list, and delete files on cloud providers."""

    @property
    def name(self) -> str:
        return "file_manager"

    @property
    def description(self) -> str:
        return (
            "Manage files on cloud providers — upload for use in conversations, "
            "list uploaded files, or delete files. Files persist across requests."
        )

    @property
    def parameters(self) -> list[ToolParameter]:
        return [
            ToolParameter("action", "string", "Action to perform", required=True,
                          enum=["upload", "list", "delete"]),
            ToolParameter("file_path", "string", "Local path to upload (for 'upload')", required=False),
            ToolParameter("file_id", "string", "File ID to delete (for 'delete')", required=False),
        ]

    async def execute(self, **kwargs: Any) -> ToolResult:
        action = kwargs.get("action", "")
        settings = _get_settings()
        try:
            import json as _json
            if action == "upload":
                fp = kwargs.get("file_path", "")
                if not fp or not Path(fp).exists():
                    return ToolResult(output="", success=False, error="valid file_path required")
                if settings.anthropic_api_key:
                    from agentic_hub.core.cloud_client import get_anthropic
                    fid = await get_anthropic().upload_file(fp)
                    return ToolResult(output=f"Uploaded: {fid}", success=True, metadata={"file_id": fid, "provider": "anthropic"})
                elif settings.openai_api_key:
                    from agentic_hub.core.cloud_client import get_openai
                    result = await get_openai().upload_file(fp)
                    return ToolResult(output=f"Uploaded: {result}", success=True, metadata={"provider": "openai"})
                return ToolResult(output="", success=False, error="No API key configured")
            elif action == "list":
                files = []
                if settings.anthropic_api_key:
                    from agentic_hub.core.cloud_client import get_anthropic
                    files = await get_anthropic().list_files()
                elif settings.openai_api_key:
                    from agentic_hub.core.cloud_client import get_openai
                    files = await get_openai().list_files()
                return ToolResult(output=_json.dumps(files, indent=2, default=str), success=True)
            elif action == "delete":
                fid = kwargs.get("file_id", "")
                if not fid:
                    return ToolResult(output="", success=False, error="file_id required")
                if settings.anthropic_api_key:
                    from agentic_hub.core.cloud_client import get_anthropic
                    await get_anthropic().delete_file(fid)
                elif settings.openai_api_key:
                    from agentic_hub.core.cloud_client import get_openai
                    await get_openai().delete_file(fid)
                return ToolResult(output=f"Deleted: {fid}", success=True)
            return ToolResult(output="", success=False, error="action must be upload/list/delete")
        except Exception as e:
            return ToolResult(output="", success=False, error=f"File manager error: {e}")


class FineTuneTool(BaseTool):
    """Create and manage fine-tuning jobs (OpenAI, Google)."""

    @property
    def name(self) -> str:
        return "fine_tune"

    @property
    def description(self) -> str:
        return (
            "Create, check, or list fine-tuning jobs. Train custom models on your data. "
            "Requires a training file uploaded via file_manager first."
        )

    @property
    def parameters(self) -> list[ToolParameter]:
        return [
            ToolParameter("action", "string", "Action to perform", required=True,
                          enum=["create", "check", "list", "cancel"]),
            ToolParameter("training_file", "string", "Training file ID (for 'create')", required=False),
            ToolParameter("model", "string", "Base model to fine-tune (for 'create')", required=False, default="gpt-4o-mini-2024-07-18"),
            ToolParameter("job_id", "string", "Job ID (for 'check'/'cancel')", required=False),
        ]

    async def execute(self, **kwargs: Any) -> ToolResult:
        action = kwargs.get("action", "")
        settings = _get_settings()
        if not settings.openai_api_key:
            return ToolResult(output="", success=False, error="OpenAI API key required for fine-tuning")
        try:
            import json as _json
            from agentic_hub.core.cloud_client import get_openai
            oai = get_openai()
            if action == "create":
                tf = kwargs.get("training_file", "")
                model = kwargs.get("model", "gpt-4o-mini-2024-07-18")
                if not tf:
                    return ToolResult(output="", success=False, error="training_file required")
                result = await oai.create_fine_tune(training_file=tf, model=model)
                return ToolResult(output=_json.dumps(result, indent=2, default=str), success=True)
            elif action == "check":
                jid = kwargs.get("job_id", "")
                if not jid:
                    return ToolResult(output="", success=False, error="job_id required")
                result = await oai.get_fine_tune(jid)
                return ToolResult(output=_json.dumps(result, indent=2, default=str), success=True)
            elif action == "list":
                result = await oai.list_fine_tunes()
                return ToolResult(output=_json.dumps(result, indent=2, default=str), success=True)
            elif action == "cancel":
                jid = kwargs.get("job_id", "")
                if not jid:
                    return ToolResult(output="", success=False, error="job_id required")
                result = await oai.cancel_fine_tune(jid)
                return ToolResult(output=_json.dumps(result, indent=2, default=str), success=True)
            return ToolResult(output="", success=False, error="action must be create/check/list/cancel")
        except Exception as e:
            return ToolResult(output="", success=False, error=f"Fine-tune error: {e}")


class VectorStoreTool(BaseTool):
    """Create vector stores and search documents (OpenAI)."""

    @property
    def name(self) -> str:
        return "vector_store"

    @property
    def description(self) -> str:
        return (
            "Create vector stores, add files, and search across documents using embeddings. "
            "Powered by OpenAI's vector store API for RAG workflows."
        )

    @property
    def parameters(self) -> list[ToolParameter]:
        return [
            ToolParameter("action", "string", "Action to perform", required=True,
                          enum=["create", "add_file", "search"]),
            ToolParameter("name", "string", "Store name (for 'create')", required=False),
            ToolParameter("store_id", "string", "Vector store ID (for 'add_file'/'search')", required=False),
            ToolParameter("file_id", "string", "File ID to add (for 'add_file')", required=False),
            ToolParameter("query", "string", "Search query (for 'search')", required=False),
        ]

    async def execute(self, **kwargs: Any) -> ToolResult:
        action = kwargs.get("action", "")
        settings = _get_settings()
        if not settings.openai_api_key:
            return ToolResult(output="", success=False, error="OpenAI API key required")
        try:
            import json as _json
            from agentic_hub.core.cloud_client import get_openai
            oai = get_openai()
            if action == "create":
                name = kwargs.get("name", "spider-web-store")
                result = await oai.create_vector_store(name=name)
                return ToolResult(output=_json.dumps(result, indent=2, default=str), success=True)
            elif action == "add_file":
                sid = kwargs.get("store_id", "")
                fid = kwargs.get("file_id", "")
                if not sid or not fid:
                    return ToolResult(output="", success=False, error="store_id and file_id required")
                result = await oai.add_file_to_vector_store(store_id=sid, file_id=fid)
                return ToolResult(output=_json.dumps(result, indent=2, default=str), success=True)
            elif action == "search":
                sid = kwargs.get("store_id", "")
                q = kwargs.get("query", "")
                if not sid or not q:
                    return ToolResult(output="", success=False, error="store_id and query required")
                result = await oai.file_search(query=q, vector_store_ids=[sid])
                return ToolResult(output=str(result)[:3000], success=True)
            return ToolResult(output="", success=False, error="action must be create/add_file/search")
        except Exception as e:
            return ToolResult(output="", success=False, error=f"Vector store error: {e}")


class ModelManagerTool(BaseTool):
    """List, pull, and manage models (Ollama + HuggingFace + Cloud)."""

    @property
    def name(self) -> str:
        return "model_manager"

    @property
    def description(self) -> str:
        return (
            "Manage AI models — list available models, pull new ones from Ollama, "
            "search HuggingFace Hub, or list cloud provider models."
        )

    @property
    def parameters(self) -> list[ToolParameter]:
        return [
            ToolParameter("action", "string", "Action to perform", required=True,
                          enum=["list_local", "list_cloud", "pull", "delete", "info"]),
            ToolParameter("model", "string", "Model name (for pull/delete/info)", required=False),
        ]

    async def execute(self, **kwargs: Any) -> ToolResult:
        action = kwargs.get("action", "")
        model = kwargs.get("model", "")
        try:
            import json as _json
            if action == "list_local":
                from agentic_hub.core.ollama_client import get_ollama
                models = await get_ollama().list_models()
                output = f"Local models ({len(models)}):\n"
                for m in models:
                    name = m.get("name", m.get("model", "?"))
                    size = m.get("size", 0)
                    output += f"  {name} ({size/(1024**3):.1f}GB)\n"
                return ToolResult(output=output, success=True)
            elif action == "list_cloud":
                results = []
                settings = _get_settings()
                if settings.anthropic_api_key:
                    from agentic_hub.core.cloud_client import get_anthropic
                    models = await get_anthropic().list_models()
                    results.extend([f"  [anthropic] {m['id']}" for m in models[:5]])
                if settings.openai_api_key:
                    from agentic_hub.core.cloud_client import get_openai
                    models = await get_openai().list_models()
                    results.extend([f"  [openai] {m}" for m in models[:10]])
                return ToolResult(output=f"Cloud models:\n" + "\n".join(results), success=True)
            elif action == "pull":
                if not model:
                    return ToolResult(output="", success=False, error="model name required")
                from agentic_hub.core.ollama_client import get_ollama
                await get_ollama().pull_model(model)
                return ToolResult(output=f"Pulling {model}...", success=True)
            elif action == "delete":
                if not model:
                    return ToolResult(output="", success=False, error="model name required")
                from agentic_hub.core.ollama_client import get_ollama
                await get_ollama().delete_model(model)
                return ToolResult(output=f"Deleted {model}", success=True)
            elif action == "info":
                if not model:
                    return ToolResult(output="", success=False, error="model name required")
                try:
                    from agentic_hub.core.ollama_client import get_ollama
                    info = await get_ollama().show_model(model)
                    return ToolResult(output=str(info)[:2000], success=True, metadata={"provider": "ollama"})
                except Exception:
                    from agentic_hub.core.hf_client import get_huggingface
                    info = get_huggingface().model_info(model)
                    return ToolResult(output=_json.dumps(info, indent=2, default=str), success=True, metadata={"provider": "huggingface"})
            return ToolResult(output="", success=False, error="action must be list_local/list_cloud/pull/delete/info")
        except Exception as e:
            return ToolResult(output="", success=False, error=f"Model manager error: {e}")


class TokenCountTool(BaseTool):
    """Count tokens before sending a request (Anthropic, Google)."""

    @property
    def name(self) -> str:
        return "count_tokens"

    @property
    def description(self) -> str:
        return (
            "Count how many tokens a message would use before sending it. "
            "Useful for estimating costs and staying within context limits."
        )

    @property
    def parameters(self) -> list[ToolParameter]:
        return [
            ToolParameter("text", "string", "Text to count tokens for", required=True),
        ]

    async def execute(self, **kwargs: Any) -> ToolResult:
        text = kwargs.get("text", "")
        if not text:
            return ToolResult(output="", success=False, error="text required")
        settings = _get_settings()
        try:
            if settings.anthropic_api_key:
                from agentic_hub.core.cloud_client import get_anthropic
                count = await get_anthropic().count_tokens(messages=[{"role": "user", "content": text}])
                return ToolResult(output=f"{count} tokens (Anthropic)", success=True, metadata={"tokens": count})
            if getattr(settings, "google_api_key", ""):
                from agentic_hub.core.cloud_client import get_google
                count = await get_google().count_tokens(contents=text)
                return ToolResult(output=f"{count} tokens (Google)", success=True, metadata={"tokens": count})
            # Rough estimate fallback
            est = len(text.split()) * 1.3
            return ToolResult(output=f"~{int(est)} tokens (estimate)", success=True)
        except Exception as e:
            return ToolResult(output="", success=False, error=f"Token count error: {e}")


class ImageEditTool(BaseTool):
    """Edit an existing image with a text prompt (OpenAI)."""

    @property
    def name(self) -> str:
        return "edit_image"

    @property
    def description(self) -> str:
        return (
            "Edit an existing image based on a text prompt. Modify, extend, or transform "
            "images using AI. Provide the path to the image and describe what to change."
        )

    @property
    def parameters(self) -> list[ToolParameter]:
        return [
            ToolParameter("image_path", "string", "Path to the image to edit", required=True),
            ToolParameter("prompt", "string", "Description of the edit to make", required=True),
        ]

    async def execute(self, **kwargs: Any) -> ToolResult:
        image_path = kwargs.get("image_path", "")
        prompt = kwargs.get("prompt", "")
        if not image_path or not prompt:
            return ToolResult(output="", success=False, error="image_path and prompt required")
        if not Path(image_path).exists():
            return ToolResult(output="", success=False, error=f"File not found: {image_path}")
        settings = _get_settings()
        if not settings.openai_api_key:
            return ToolResult(output="", success=False, error="OpenAI API key required")
        try:
            from agentic_hub.core.cloud_client import get_openai
            urls = await get_openai().edit_image(image_path=image_path, prompt=prompt)
            if urls:
                return ToolResult(output=f"Edited image: {urls[0]}", success=True, metadata={"url": urls[0]})
            return ToolResult(output="", success=False, error="No result returned")
        except Exception as e:
            return ToolResult(output="", success=False, error=f"Image edit error: {e}")


class VideoGenTool(BaseTool):
    """Generate video from text (OpenAI Sora, Google Veo)."""

    @property
    def name(self) -> str:
        return "generate_video"

    @property
    def description(self) -> str:
        return (
            "Generate a video from a text description. Creates short video clips "
            "using AI video generation models."
        )

    @property
    def parameters(self) -> list[ToolParameter]:
        return [
            ToolParameter("prompt", "string", "Description of the video to generate", required=True),
        ]

    async def execute(self, **kwargs: Any) -> ToolResult:
        prompt = kwargs.get("prompt", "")
        if not prompt:
            return ToolResult(output="", success=False, error="prompt required")
        settings = _get_settings()
        try:
            if settings.openai_api_key:
                from agentic_hub.core.cloud_client import get_openai
                result = await get_openai().generate_video(prompt=prompt)
                return ToolResult(output=f"Video generated: {result}", success=True, metadata={"provider": "openai"})
            if getattr(settings, "google_api_key", ""):
                from agentic_hub.core.cloud_client import get_google
                result = await get_google().generate_video(prompt=prompt)
                return ToolResult(output=f"Video generated: {result}", success=True, metadata={"provider": "google"})
            return ToolResult(output="", success=False, error="No video generation provider available")
        except Exception as e:
            return ToolResult(output="", success=False, error=f"Video gen error: {e}")


class ComputerUseTool(BaseTool):
    """Autonomous computer control — mouse, keyboard, screen (Anthropic)."""

    @property
    def name(self) -> str:
        return "computer_use"

    @property
    def description(self) -> str:
        return (
            "Control a computer autonomously — click, type, screenshot, scroll. "
            "Claude can see the screen and interact with any application. "
            "Use for browser automation, GUI testing, desktop tasks."
        )

    @property
    def parameters(self) -> list[ToolParameter]:
        return [
            ToolParameter("prompt", "string", "What to do on the computer", required=True),
        ]

    async def execute(self, **kwargs: Any) -> ToolResult:
        prompt = kwargs.get("prompt", "")
        if not prompt:
            return ToolResult(output="", success=False, error="prompt required")
        settings = _get_settings()
        if not settings.anthropic_api_key:
            return ToolResult(output="", success=False, error="Anthropic API key required")
        try:
            from agentic_hub.core.cloud_client import get_anthropic
            result = await get_anthropic().computer_use(prompt=prompt)
            import json as _json
            return ToolResult(output=_json.dumps(result, indent=2, default=str)[:3000], success=True)
        except Exception as e:
            return ToolResult(output="", success=False, error=f"Computer use error: {e}")


class FuzzySearchTool(BaseTool):
    """Fuzzy entity name matching (PostgreSQL pg_trgm)."""

    @property
    def name(self) -> str:
        return "fuzzy_search"

    @property
    def description(self) -> str:
        return (
            "Find entities even with typos or partial names using fuzzy matching. "
            "Powered by PostgreSQL trigram similarity."
        )

    @property
    def parameters(self) -> list[ToolParameter]:
        return [
            ToolParameter("name", "string", "Entity name to search (can be misspelled)", required=True),
            ToolParameter("limit", "integer", "Max results", required=False, default=5),
        ]

    async def execute(self, **kwargs: Any) -> ToolResult:
        name = kwargs.get("name", "")
        limit = kwargs.get("limit", 5)
        if not name:
            return ToolResult(output="", success=False, error="name required")
        try:
            from agentic_hub.core.pg_service import get_pg_service
            pg = await get_pg_service()
            if not pg.connected:
                return ToolResult(output="", success=False, error="PostgreSQL not connected")
            results = await pg.fuzzy_match_entity(name, limit=limit)
            if not results:
                return ToolResult(output=f"No fuzzy matches for '{name}'", success=True)
            import json as _json
            output = f"Fuzzy matches for '{name}':\n"
            for r in results:
                output += f"  {_json.dumps(r, default=str)[:150]}\n"
            return ToolResult(output=output, success=True, metadata={"count": len(results)})
        except Exception as e:
            return ToolResult(output="", success=False, error=f"Fuzzy search error: {e}")


class CacheTool(BaseTool):
    """Redis caching — store and retrieve cached values."""

    @property
    def name(self) -> str:
        return "cache"

    @property
    def description(self) -> str:
        return (
            "Store or retrieve cached values in Redis. Use for caching API responses, "
            "computed results, or any data that should persist briefly."
        )

    @property
    def parameters(self) -> list[ToolParameter]:
        return [
            ToolParameter("action", "string", "Action to perform", required=True,
                          enum=["set", "get", "delete"]),
            ToolParameter("key", "string", "Cache key", required=True),
            ToolParameter("value", "string", "Value to store (for 'set')", required=False),
            ToolParameter("ttl", "integer", "Time-to-live in seconds (for 'set')", required=False, default=3600),
        ]

    async def execute(self, **kwargs: Any) -> ToolResult:
        action = kwargs.get("action", "")
        key = kwargs.get("key", "")
        if not key:
            return ToolResult(output="", success=False, error="key required")
        try:
            from agentic_hub.core.redis_service import get_redis_service
            redis = await get_redis_service()
            if not redis.connected:
                return ToolResult(output="", success=False, error="Redis not connected")
            if action == "set":
                value = kwargs.get("value", "")
                ttl = kwargs.get("ttl", 3600)
                await redis.cache_set(key, value, ttl=ttl)
                return ToolResult(output=f"Cached '{key}' (TTL: {ttl}s)", success=True)
            elif action == "get":
                value = await redis.cache_get(key)
                if value is None:
                    return ToolResult(output=f"Cache miss: '{key}'", success=True)
                return ToolResult(output=str(value), success=True)
            elif action == "delete":
                await redis.cache_delete(key)
                return ToolResult(output=f"Deleted cache key '{key}'", success=True)
            return ToolResult(output="", success=False, error="action must be set/get/delete")
        except Exception as e:
            return ToolResult(output="", success=False, error=f"Cache error: {e}")


class BalanceCheckTool(BaseTool):
    """Check API credit balances (DeepSeek)."""

    @property
    def name(self) -> str:
        return "check_balance"

    @property
    def description(self) -> str:
        return "Check remaining API credit balance for cloud providers."

    @property
    def parameters(self) -> list[ToolParameter]:
        return []

    async def execute(self, **kwargs: Any) -> ToolResult:
        settings = _get_settings()
        results = []
        if getattr(settings, "deepseek_api_key", ""):
            try:
                from agentic_hub.core.cloud_client import get_deepseek
                balance = await get_deepseek().get_balance()
                import json as _json
                results.append(f"DeepSeek: {_json.dumps(balance)}")
            except Exception as e:
                results.append(f"DeepSeek: error — {e}")
        if not results:
            return ToolResult(output="No balance-check providers configured", success=True)
        return ToolResult(output="\n".join(results), success=True)


# ── Oracle Cloud AI Tools ────────────────────────────────────────────


class PhoneNotifyTool(BaseTool):
    """Send a notification to the user's iPhone."""

    @property
    def name(self) -> str:
        return "phone_notify"

    @property
    def description(self) -> str:
        return (
            "Send a push notification to the user's iPhone. Use to alert about "
            "completed tasks, trade executions, price alerts, or anything urgent. "
            "The notification can trigger a Shortcut on the phone."
        )

    @property
    def parameters(self) -> list[ToolParameter]:
        return [
            ToolParameter("title", "string", "Notification title", required=True),
            ToolParameter("text", "string", "Notification body text", required=True),
        ]

    async def execute(self, **kwargs: Any) -> ToolResult:
        title = kwargs.get("title", "")
        text = kwargs.get("text", "")
        if not title or not text:
            return ToolResult(output="", success=False, error="title and text required")
        try:
            from agentic_hub.core.shortcuts_client import get_shortcuts_client
            client = get_shortcuts_client()
            if not client.is_configured:
                return ToolResult(output="", success=False,
                                  error="Phone notifications not configured (set PUSHCUT_API_KEY or IFTTT_WEBHOOK_KEY)")
            result = await client.notify(title, text)
            provider = result.get("provider", "unknown")
            return ToolResult(output=f"Notification sent via {provider}: {title}", success=result.get("ok", False),
                              metadata={"provider": provider})
        except Exception as e:
            return ToolResult(output="", success=False, error=f"Phone notify error: {e}")


class OracleGuardrailsTool(BaseTool):
    """Content moderation + prompt injection + PII detection (Oracle Cloud)."""

    @property
    def name(self) -> str:
        return "guardrails"

    @property
    def description(self) -> str:
        return (
            "Scan text for harmful content, prompt injection attacks, and personally "
            "identifiable information (PII). Returns safety scores and detected PII entities. "
            "Use as a safety gate on untrusted input or before exposing outputs externally."
        )

    @property
    def parameters(self) -> list[ToolParameter]:
        return [
            ToolParameter("text", "string", "Text to scan for safety", required=True),
        ]

    async def execute(self, **kwargs: Any) -> ToolResult:
        text = kwargs.get("text", "")
        if not text:
            return ToolResult(output="", success=False, error="text required")
        settings = _get_settings()
        if not settings.oci_compartment_id:
            return ToolResult(output="", success=False, error="Oracle Cloud not configured (OCI_COMPARTMENT_ID required)")
        try:
            from agentic_hub.core.oracle_client import get_oracle
            result = await get_oracle().guardrails(text)
            import json as _json
            cm = result.get("content_moderation", {})
            pi = result.get("prompt_injection", 0)
            pii = result.get("pii", [])
            output = f"Content Moderation: {_json.dumps(cm)}\n"
            output += f"Prompt Injection: {'DETECTED' if pi >= 0.5 else 'clean'} (score: {pi})\n"
            if pii:
                output += f"PII Detected ({len(pii)}):\n"
                for p in pii:
                    output += f"  [{p['label']}] \"{p['text']}\" (confidence: {p['score']:.2f})\n"
            else:
                output += "PII: none detected\n"
            flagged = cm.get("overall", 0) >= 0.5 or pi >= 0.5 or len(pii) > 0
            return ToolResult(output=output, success=True, metadata={"flagged": flagged, "pii_count": len(pii)})
        except Exception as e:
            return ToolResult(output="", success=False, error=f"Guardrails error: {e}")


class RerankTool(BaseTool):
    """Rerank documents by relevance to a query (Oracle Cohere Rerank)."""

    @property
    def name(self) -> str:
        return "rerank"

    @property
    def description(self) -> str:
        return (
            "Reorder a list of documents by relevance to a search query. "
            "Use after RAG retrieval to improve result quality — put the most relevant "
            "documents first. Powered by Cohere Rerank 3.5."
        )

    @property
    def parameters(self) -> list[ToolParameter]:
        return [
            ToolParameter("query", "string", "The search query", required=True),
            ToolParameter("documents", "string", "JSON array of document strings to rerank", required=True),
            ToolParameter("top_n", "integer", "Number of top results to return", required=False, default=5),
        ]

    async def execute(self, **kwargs: Any) -> ToolResult:
        query = kwargs.get("query", "")
        docs_str = kwargs.get("documents", "")
        top_n = kwargs.get("top_n", 5)
        if not query or not docs_str:
            return ToolResult(output="", success=False, error="query and documents required")
        settings = _get_settings()
        if not settings.oci_compartment_id:
            return ToolResult(output="", success=False, error="Oracle Cloud not configured")
        try:
            import json as _json
            documents = _json.loads(docs_str)
            from agentic_hub.core.oracle_client import get_oracle
            results = await get_oracle().rerank(query=query, documents=documents, top_n=top_n)
            output = f"Reranked {len(results)} documents:\n"
            for r in results:
                output += f"  #{r['index']+1} (score: {r['relevance_score']:.3f}) {r['document'][:100]}\n"
            return ToolResult(output=output, success=True, metadata={"count": len(results)})
        except Exception as e:
            return ToolResult(output="", success=False, error=f"Rerank error: {e}")


# ---------------------------------------------------------------------------
# Salesforce Tools — sf CLI, domain knowledge, browser validation
# ---------------------------------------------------------------------------

class SalesforceTool(BaseTool):
    """Execute Salesforce CLI operations — deploy, retrieve, test, query."""

    @property
    def name(self) -> str:
        return "salesforce"

    @property
    def description(self) -> str:
        return (
            "Execute Salesforce CLI (sf) operations: deploy metadata, retrieve source, "
            "run Apex tests, query data with SOQL, check org info, and preview deployments. "
            "Commands target the default org unless target_org is specified. "
            "The sf CLI handles auth token refresh automatically. "
            "IMPORTANT: Before deploying, always run sf_knowledge tool to check for gotchas. "
            "After deploying LWC changes, use sf_validate to screenshot the result."
        )

    @property
    def parameters(self) -> list[ToolParameter]:
        return [
            ToolParameter("action", "string",
                "The Salesforce operation to perform",
                enum=["deploy", "retrieve", "test", "query", "org_info",
                      "deploy_preview", "deploy_report", "list_orgs"]),
            ToolParameter("target_org", "string",
                "Org alias or username (default: joedev)", required=False, default="joedev"),
            ToolParameter("source_dir", "string",
                "Source directory for deploy/retrieve (default: force-app)", required=False),
            ToolParameter("metadata", "string",
                "Metadata types/components for retrieve (-m flag), e.g. "
                "'ApexClass:MyClass,LightningComponentBundle:myLwc'", required=False),
            ToolParameter("test_names", "string",
                "Comma-separated test class names for 'test' action", required=False),
            ToolParameter("test_level", "string",
                "Test level for deploy",
                required=False,
                enum=["NoTestRun", "RunSpecifiedTests", "RunLocalTests", "RunAllTestsInOrg"]),
            ToolParameter("soql", "string",
                "SOQL query for 'query' action", required=False),
            ToolParameter("wait_minutes", "integer",
                "Minutes to wait for async deploy (default: 10)", required=False, default=10),
        ]

    async def execute(self, **kwargs: Any) -> ToolResult:
        from agentic_hub.core.sandbox import execute
        import json as _json

        action = kwargs.get("action", "")
        target = kwargs.get("target_org", "joedev")
        source_dir = kwargs.get("source_dir", "force-app")
        metadata = kwargs.get("metadata", "")
        test_names = kwargs.get("test_names", "")
        test_level = kwargs.get("test_level", "")
        soql = kwargs.get("soql", "")
        wait = kwargs.get("wait_minutes", 10)

        project_dir = str(Path.home() / "salesforce-backup")

        if action == "deploy":
            cmd = (f"sf project deploy start --source-dir {source_dir} "
                   f"-o {target} --wait {wait} --json")
            if test_level:
                cmd += f" --test-level {test_level}"
            if test_level == "RunSpecifiedTests" and test_names:
                for tn in test_names.split(","):
                    cmd += f" --tests {tn.strip()}"
        elif action == "retrieve":
            cmd = f"sf project retrieve start -o {target} --json"
            if metadata:
                cmd += f" -m {metadata}"
            else:
                cmd += f" --source-dir {source_dir}"
        elif action == "test":
            if test_names:
                names = " ".join(f"--tests {n.strip()}" for n in test_names.split(","))
                cmd = (f"sf apex run test -o {target} {names} "
                       f"--result-format human --wait 5 --json")
            else:
                cmd = (f"sf apex run test -o {target} --test-level RunLocalTests "
                       f"--result-format human --wait 5 --json")
        elif action == "query":
            if not soql:
                return ToolResult(output="", success=False,
                                  error="'soql' parameter required for query action")
            cmd = f'sf data query -o {target} --query "{soql}" --json'
        elif action == "org_info":
            cmd = f"sf org display -o {target} --json"
        elif action == "deploy_preview":
            cmd = (f"sf project deploy preview --source-dir {source_dir} "
                   f"-o {target} --json")
        elif action == "deploy_report":
            cmd = f"sf project deploy report -o {target} --json"
        elif action == "list_orgs":
            cmd = "sf org list --json"
        else:
            return ToolResult(output="", success=False,
                              error=f"Unknown action: {action}")

        start = time.monotonic()
        result = await execute(cmd, cwd=project_dir, timeout=300)
        elapsed_ms = int((time.monotonic() - start) * 1000)

        output_parts = []
        if result.stdout:
            try:
                data = _json.loads(result.stdout)
                if action == "deploy" and "result" in data:
                    r = data["result"]
                    status = r.get("status", "Unknown")
                    output_parts.append(f"Deploy Status: {status}")
                    if r.get("numberComponentsDeployed"):
                        output_parts.append(f"Components deployed: {r['numberComponentsDeployed']}")
                    if r.get("numberComponentErrors"):
                        output_parts.append(f"Component errors: {r['numberComponentErrors']}")
                    if r.get("numberTestsCompleted"):
                        output_parts.append(
                            f"Tests: {r['numberTestsCompleted']} completed, "
                            f"{r.get('numberTestErrors', 0)} failed")
                    for err in r.get("details", {}).get("componentFailures", []):
                        output_parts.append(
                            f"  ❌ {err.get('componentType','')}/{err.get('fullName','')}: "
                            f"{err.get('problem','')}")
                    for err in (r.get("details", {}).get("runTestResult", {})
                                .get("failures", [])):
                        output_parts.append(
                            f"  ❌ {err.get('name','')}.{err.get('methodName','')}: "
                            f"{err.get('message','')[:200]}")
                elif action == "test" and "result" in data:
                    r = data["result"]
                    summary = r.get("summary", {})
                    output_parts.append(
                        f"Tests: {summary.get('testsRan', 0)} ran, "
                        f"{summary.get('passing', 0)} passed, "
                        f"{summary.get('failing', 0)} failed")
                    output_parts.append(f"Coverage: {summary.get('orgWideCoverage', 'N/A')}")
                    for t in r.get("tests", []):
                        icon = "✅" if t.get("Outcome") == "Pass" else "❌"
                        cls = t.get("ApexClass", {}).get("Name", "")
                        output_parts.append(f"  {icon} {cls}.{t.get('MethodName', '')}")
                        if t.get("Message"):
                            output_parts.append(f"      {t['Message'][:200]}")
                else:
                    output_parts.append(_json.dumps(data, indent=2)[:10000])
            except (_json.JSONDecodeError, ValueError):
                output_parts.append(result.stdout[:10000])

        if result.stderr and result.returncode != 0:
            output_parts.append(f"STDERR: {result.stderr[:1000]}")

        output = "\n".join(output_parts) or "(no output)"
        return ToolResult(
            output=output,
            success=result.returncode == 0,
            error=result.stderr[:200] if result.returncode != 0 else None,
            metadata={"action": action, "target_org": target, "latency_ms": elapsed_ms},
        )


class SalesforceKnowledgeTool(BaseTool):
    """Query Salesforce domain knowledge — gotchas, patterns, and hard-learned lessons."""

    @property
    def name(self) -> str:
        return "sf_knowledge"

    @property
    def description(self) -> str:
        return (
            "Query the Salesforce domain knowledge base for gotchas, patterns, and lessons "
            "learned from the Nexa Mortgage / UWM integration project. Use BEFORE making "
            "any Salesforce changes to avoid known pitfalls. Topics: CMDT XML namespaces, "
            "deploy traps, LWC wire/modal quirks, Apex sharing/integration patterns, "
            "test coverage vs LO walkthrough, org config, UWM API specifics, known bugs."
        )

    @property
    def parameters(self) -> list[ToolParameter]:
        return [
            ToolParameter("topic", "string",
                "Knowledge topic to retrieve",
                enum=["cmdt", "deploy", "lwc", "apex", "testing",
                      "uwm_api", "org_config", "known_bugs", "all"]),
        ]

    async def execute(self, **kwargs: Any) -> ToolResult:
        import yaml
        topic = kwargs.get("topic", "all")
        knowledge_path = (Path(__file__).parent.parent.parent.parent.parent
                          / "data" / "salesforce_knowledge.yaml")

        if not knowledge_path.exists():
            return ToolResult(output="", success=False,
                              error=f"Knowledge file not found at {knowledge_path}")
        try:
            with open(knowledge_path) as f:
                kb = yaml.safe_load(f)

            knowledge = kb.get("knowledge", {})
            if topic == "all":
                sections = knowledge
            else:
                val = knowledge.get(topic)
                if not val:
                    return ToolResult(
                        output=f"No knowledge found for topic: {topic}. "
                               f"Available: {', '.join(knowledge.keys())}",
                        success=True)
                sections = {topic: val}

            output_parts = ["# Salesforce Domain Knowledge\n"]
            for section_name, entries in sections.items():
                if not entries:
                    continue
                output_parts.append(f"\n## {section_name.replace('_', ' ').upper()}\n")
                for entry in entries:
                    output_parts.append(f"### {entry.get('title', 'Untitled')}")
                    if entry.get("severity"):
                        output_parts.append(f"**Severity: {entry['severity']}**")
                    output_parts.append(entry.get("content", ""))
                    if entry.get("fix"):
                        output_parts.append(f"**Fix:** {entry['fix']}")
                    output_parts.append("")

            output = "\n".join(output_parts)
            return ToolResult(output=output, success=True,
                              metadata={"topic": topic, "entries": sum(
                                  len(v) for v in sections.values() if isinstance(v, list))})
        except Exception as e:
            return ToolResult(output="", success=False,
                              error=f"Knowledge load error: {e}")


class SalesforceValidateTool(BaseTool):
    """Browser-based Salesforce org validation via CamouFox — screenshot LWCs after deploy."""

    @property
    def name(self) -> str:
        return "sf_validate"

    @property
    def description(self) -> str:
        return (
            "Navigate to a Salesforce org page using CamouFox (anti-fingerprint Firefox) "
            "and take a screenshot for visual validation. Use after deploying LWC changes "
            "to verify the UI renders correctly. The 'analyze' action takes a screenshot "
            "AND feeds it to a vision model to check for broken layouts, missing components, "
            "and error banners — automated UI judgment. Can also check for specific CSS "
            "selectors. Logs in via frontdoor.jsp using the sf CLI session token."
        )

    @property
    def parameters(self) -> list[ToolParameter]:
        return [
            ToolParameter("action", "string", "Validation action",
                enum=["screenshot", "check_element", "full_page", "analyze"]),
            ToolParameter("url", "string",
                "Direct Salesforce URL or path (e.g. /lightning/r/Opportunity/006xxx/view)",
                required=False),
            ToolParameter("record_id", "string",
                "Salesforce record ID to navigate to", required=False),
            ToolParameter("object_type", "string",
                "Object type for record navigation (Opportunity, Lead, etc.)",
                required=False),
            ToolParameter("selector", "string",
                "CSS selector to check for element presence (check_element action)",
                required=False),
            ToolParameter("target_org", "string",
                "Org alias for login (default: joedev)",
                required=False, default="joedev"),
            ToolParameter("wait_seconds", "integer",
                "Seconds to wait for LWC render after page load (default: 10)",
                required=False, default=10),
        ]

    async def execute(self, **kwargs: Any) -> ToolResult:
        import json as _json
        action = kwargs.get("action", "screenshot")
        url = kwargs.get("url", "")
        record_id = kwargs.get("record_id", "")
        object_type = kwargs.get("object_type", "")
        selector = kwargs.get("selector", "")
        target_org = kwargs.get("target_org", "joedev")
        wait = kwargs.get("wait_seconds", 10)

        try:
            from camoufox.async_api import AsyncCamoufox
        except ImportError:
            return ToolResult(
                output="CamouFox not installed. Run: pip install camoufox",
                success=False,
                error="camoufox not installed — run: pip install camoufox",
            )

        # Get org session from sf CLI
        from agentic_hub.core.sandbox import execute
        org_result = await execute(f"sf org display -o {target_org} --json", timeout=15)
        if org_result.returncode != 0:
            return ToolResult(output="", success=False,
                              error=f"sf org display failed: {org_result.stderr[:200]}")
        try:
            org_data = _json.loads(org_result.stdout)
            instance_url = org_data["result"]["instanceUrl"]
            access_token = org_data["result"]["accessToken"]
        except (KeyError, _json.JSONDecodeError) as e:
            return ToolResult(output="", success=False,
                              error=f"Failed to parse org info: {e}")

        # Build navigation target
        if url:
            nav_path = url if url.startswith("/") else url.replace(instance_url, "")
        elif record_id and object_type:
            nav_path = f"/lightning/r/{object_type}/{record_id}/view"
        elif record_id:
            nav_path = f"/{record_id}"
        else:
            nav_path = "/lightning/page/home"

        login_url = f"{instance_url}/secur/frontdoor.jsp?sid={access_token}&retURL={nav_path}"
        screenshot_dir = Path(__file__).parent.parent.parent.parent.parent / "data" / "screenshots"
        screenshot_dir.mkdir(parents=True, exist_ok=True)

        ts = int(time.time())
        screenshot_path = screenshot_dir / f"sf_validate_{ts}.png"

        start = time.monotonic()
        try:
            async with AsyncCamoufox(headless=True) as browser:
                page = await browser.new_page()
                await page.set_viewport_size({"width": 1920, "height": 1080})

                # CamouFox uses Firefox — frontdoor.jsp login works the same
                await page.goto(login_url, wait_until="networkidle", timeout=30000)
                # Wait for LWC framework to render custom components
                await page.wait_for_timeout(wait * 1000)

                full = action == "full_page"
                await page.screenshot(path=str(screenshot_path), full_page=full)

                element_found = None
                if selector:
                    element = await page.query_selector(selector)
                    element_found = element is not None

                title = await page.title()
                final_url = page.url

            elapsed_ms = int((time.monotonic() - start) * 1000)
            output_parts = [
                f"Page: {title}",
                f"URL: {final_url}",
                f"Screenshot saved: {screenshot_path}",
            ]
            if element_found is not None:
                icon = "✅" if element_found else "❌"
                output_parts.append(f"Element '{selector}': {icon}")

            # Vision analysis — feed screenshot to AI for automated UI judgment
            if action == "analyze":
                try:
                    import base64
                    img_bytes = screenshot_path.read_bytes()
                    img_b64 = base64.b64encode(img_bytes).decode()
                    vision_tool = VisionTool()
                    vision_result = await vision_tool.execute(
                        prompt=(
                            "Analyze this Salesforce Lightning page screenshot. Check for:\n"
                            "1. Are all expected components visible? (look for Lightning cards, data tables, forms)\n"
                            "2. Are there any error banners, toast messages, or broken layouts?\n"
                            "3. Is the page fully loaded or is there a spinner/loading state stuck?\n"
                            "4. Are there any obvious CSS issues (overlapping elements, cut-off text)?\n"
                            "5. Does the page look like a functional business application?\n"
                            "Be specific about what you see. Flag anything that looks wrong."
                        ),
                        image=img_b64,
                        source_type="base64",
                    )
                    if vision_result.success:
                        output_parts.append(f"\n--- Vision Analysis ---\n{vision_result.output}")
                    else:
                        output_parts.append(f"\nVision analysis failed: {vision_result.error}")
                except Exception as e:
                    output_parts.append(f"\nVision analysis error: {str(e)[:200]}")

            return ToolResult(
                output="\n".join(output_parts),
                success=True,
                metadata={"screenshot": str(screenshot_path),
                          "latency_ms": elapsed_ms, "title": title},
            )
        except Exception as e:
            elapsed_ms = int((time.monotonic() - start) * 1000)
            return ToolResult(
                output="", success=False,
                error=f"CamouFox validation failed: {str(e)[:300]}",
                metadata={"latency_ms": elapsed_ms},
            )


class PauseAndAskTool(BaseTool):
    """Pause execution and ask the user a question via phone notification."""

    @property
    def name(self) -> str:
        return "pause_and_ask"

    @property
    def description(self) -> str:
        return (
            "STOP and ask the user when you face an ambiguous decision that could go wrong. "
            "Sends a push notification to the user's phone with the question and options. "
            "Use this instead of guessing when: (1) multiple valid approaches exist and the "
            "choice affects behavior, (2) you're about to deploy/modify production code and "
            "aren't sure about the correct value, (3) the user's intent is unclear, "
            "(4) you discover something unexpected that changes the plan. "
            "ALWAYS prefer asking over guessing on Salesforce changes."
        )

    @property
    def parameters(self) -> list[ToolParameter]:
        return [
            ToolParameter("question", "string",
                "Clear, specific question for the user. Include what you've found "
                "and what the options are.", required=True),
            ToolParameter("options", "string",
                "Comma-separated list of options you've identified (e.g. "
                "'Option A: use sharing, Option B: without sharing')",
                required=False),
            ToolParameter("context", "string",
                "Brief context about what you were doing when you hit this decision point",
                required=False),
            ToolParameter("severity", "string",
                "How blocking is this? 'blocking' = can't proceed, 'advisory' = will proceed "
                "with best guess if no response in 2 min",
                required=False, enum=["blocking", "advisory"], default="blocking"),
        ]

    async def execute(self, **kwargs: Any) -> ToolResult:
        question = kwargs.get("question", "")
        options = kwargs.get("options", "")
        context = kwargs.get("context", "")
        severity = kwargs.get("severity", "blocking")

        if not question:
            return ToolResult(output="", success=False, error="question required")

        # Build notification body
        body_parts = []
        if context:
            body_parts.append(f"Context: {context}")
        body_parts.append(f"Question: {question}")
        if options:
            body_parts.append(f"Options: {options}")
        body_parts.append(f"[{severity.upper()}]")
        body = "\n".join(body_parts)

        # Send phone notification
        notification_sent = False
        try:
            from agentic_hub.core.shortcuts_client import get_shortcuts_client
            client = get_shortcuts_client()
            if client.is_configured:
                await client.notify("spider.Web needs input", body)
                notification_sent = True
        except Exception as e:
            logger.warning(f"Phone notify failed in pause_and_ask: {e}")

        # Log the question to a file so the user can see it in the web UI too
        question_log = Path(__file__).parent.parent.parent.parent.parent / "data" / "pending_questions.jsonl"
        try:
            import json as _json
            entry = {
                "question": question,
                "options": options,
                "context": context,
                "severity": severity,
                "timestamp": time.time(),
                "notified": notification_sent,
            }
            with open(question_log, "a") as f:
                f.write(_json.dumps(entry) + "\n")
        except Exception:
            pass

        output_parts = [
            f"PAUSED — waiting for user input.",
            f"Question: {question}",
        ]
        if options:
            output_parts.append(f"Options: {options}")
        if notification_sent:
            output_parts.append("Phone notification sent.")
        else:
            output_parts.append("Phone notification not configured — check web UI or chat.")
        output_parts.append(
            f"Severity: {severity}" +
            (" — cannot proceed without answer." if severity == "blocking"
             else " — will proceed with best guess if no response.")
        )

        return ToolResult(
            output="\n".join(output_parts),
            success=True,
            metadata={"severity": severity, "notified": notification_sent},
        )


class BatchEditTool(BaseTool):
    """Apply multiple file edits in a single tool call."""

    @property
    def name(self) -> str:
        return "batch_edit"

    @property
    def description(self) -> str:
        return (
            "Apply multiple file edits in one tool call — for multi-file refactors that "
            "would otherwise take many rounds. Each edit is a find-and-replace within a "
            "specific file. All edits are validated before any are applied (atomic). "
            "Use for: renaming across files, updating imports, multi-component LWC changes, "
            "Apex + test class changes together."
        )

    @property
    def parameters(self) -> list[ToolParameter]:
        return [
            ToolParameter("edits", "string",
                'JSON array of edits: [{"path": "file.cls", "old": "find this", "new": "replace with"}, ...]. '
                "Each edit replaces the FIRST occurrence of 'old' with 'new' in the file at 'path'. "
                "Paths are relative to ~/salesforce-backup/ or absolute.",
                required=True),
        ]

    async def execute(self, **kwargs: Any) -> ToolResult:
        import json as _json
        edits_str = kwargs.get("edits", "")
        if not edits_str:
            return ToolResult(output="", success=False, error="edits parameter required")

        try:
            edits = _json.loads(edits_str)
        except _json.JSONDecodeError as e:
            return ToolResult(output="", success=False, error=f"Invalid JSON: {e}")

        if not isinstance(edits, list):
            return ToolResult(output="", success=False, error="edits must be a JSON array")

        # Resolve paths and validate all edits before applying any
        home = Path.home()
        sf_root = home / "salesforce-backup"
        resolved_edits = []
        errors = []

        for i, edit in enumerate(edits):
            path_str = edit.get("path", "")
            old = edit.get("old", "")
            new = edit.get("new", "")

            if not path_str or not old:
                errors.append(f"Edit #{i+1}: missing 'path' or 'old'")
                continue

            # Resolve path
            p = Path(path_str)
            if not p.is_absolute():
                p = sf_root / path_str
            p = p.resolve()

            # Validate path is in allowed directories
            from agentic_hub.core.sandbox import _validate_path
            err = _validate_path(str(p))
            if err:
                errors.append(f"Edit #{i+1} ({path_str}): {err}")
                continue

            if not p.exists():
                errors.append(f"Edit #{i+1}: file not found: {p}")
                continue

            content = p.read_text()
            if old not in content:
                errors.append(f"Edit #{i+1} ({p.name}): search string not found")
                continue

            resolved_edits.append({"path": p, "old": old, "new": new, "index": i + 1})

        if errors:
            return ToolResult(
                output="Validation failed — no edits applied:\n" + "\n".join(f"  {e}" for e in errors),
                success=False,
                error=f"{len(errors)} edit(s) failed validation",
            )

        # All validated — apply atomically
        applied = []
        for edit in resolved_edits:
            p = edit["path"]
            content = p.read_text()
            new_content = content.replace(edit["old"], edit["new"], 1)
            p.write_text(new_content)
            applied.append(f"  #{edit['index']} {p.name}: applied")

        return ToolResult(
            output=f"Applied {len(applied)} edits:\n" + "\n".join(applied),
            success=True,
            metadata={"edits_applied": len(applied)},
        )


class AWSTool(BaseTool):
    """AWS CLI wrapper — Secrets Manager, Lambda, and S3 for UWM integration infra."""

    @property
    def name(self) -> str:
        return "aws"

    @property
    def description(self) -> str:
        return (
            "Execute AWS CLI operations for managing the UWM integration infrastructure. "
            "Covers Secrets Manager (read/update secrets for Salesforce OAuth, UWM API keys, "
            "webhook auth), Lambda (invoke functions, update code, check logs), and S3 "
            "(list/read MISMO XML exports). Region: us-east-2. "
            "SAFETY: read operations are free. Write operations (update secret, update "
            "Lambda code) show a confirmation prompt before executing."
        )

    @property
    def parameters(self) -> list[ToolParameter]:
        return [
            ToolParameter("service", "string", "AWS service to use",
                enum=["secretsmanager", "lambda", "s3"]),
            ToolParameter("action", "string", "Action to perform",
                enum=[
                    # Secrets Manager
                    "get_secret", "list_secrets", "update_secret",
                    # Lambda
                    "invoke", "list_functions", "get_function", "get_logs",
                    # S3
                    "list_objects", "get_object",
                ]),
            ToolParameter("name", "string",
                "Resource name — secret ID, function name, or S3 bucket/key",
                required=False),
            ToolParameter("payload", "string",
                "JSON payload for Lambda invoke or new secret value for update_secret",
                required=False),
            ToolParameter("region", "string",
                "AWS region (default: us-east-2)",
                required=False, default="us-east-2"),
        ]

    async def execute(self, **kwargs: Any) -> ToolResult:
        import json as _json
        from agentic_hub.core.sandbox import execute

        service = kwargs.get("service", "")
        action = kwargs.get("action", "")
        name = kwargs.get("name", "")
        payload = kwargs.get("payload", "")
        region = kwargs.get("region", "us-east-2")

        if not service or not action:
            return ToolResult(output="", success=False, error="service and action required")

        # Build AWS CLI command
        base = f"aws --region {region} --output json"

        if service == "secretsmanager":
            if action == "get_secret":
                if not name:
                    return ToolResult(output="", success=False, error="name required (secret ID)")
                cmd = f"{base} secretsmanager get-secret-value --secret-id '{name}'"
            elif action == "list_secrets":
                cmd = f"{base} secretsmanager list-secrets"
            elif action == "update_secret":
                if not name or not payload:
                    return ToolResult(output="", success=False, error="name and payload required")
                cmd = f"{base} secretsmanager put-secret-value --secret-id '{name}' --secret-string '{payload}'"
            else:
                return ToolResult(output="", success=False, error=f"Unknown secretsmanager action: {action}")

        elif service == "lambda":
            if action == "list_functions":
                cmd = f"{base} lambda list-functions --query 'Functions[].FunctionName' --output table"
            elif action == "get_function":
                if not name:
                    return ToolResult(output="", success=False, error="name required (function name)")
                cmd = f"{base} lambda get-function-configuration --function-name '{name}'"
            elif action == "invoke":
                if not name:
                    return ToolResult(output="", success=False, error="name required (function name)")
                outfile = f"/tmp/lambda_response_{int(time.time())}.json"
                invoke_cmd = f"{base} lambda invoke --function-name '{name}' {outfile}"
                if payload:
                    invoke_cmd = f"{base} lambda invoke --function-name '{name}' --payload '{payload}' {outfile}"
                cmd = f"{invoke_cmd} && cat {outfile} && rm -f {outfile}"
            elif action == "get_logs":
                if not name:
                    return ToolResult(output="", success=False, error="name required (function name)")
                cmd = (f"{base} logs filter-log-events "
                       f"--log-group-name '/aws/lambda/{name}' "
                       f"--limit 20 --query 'events[].message' --output text")
            else:
                return ToolResult(output="", success=False, error=f"Unknown lambda action: {action}")

        elif service == "s3":
            if action == "list_objects":
                if not name:
                    return ToolResult(output="", success=False, error="name required (bucket or bucket/prefix)")
                cmd = f"{base} s3 ls s3://{name} --recursive --human-readable"
            elif action == "get_object":
                if not name:
                    return ToolResult(output="", success=False, error="name required (bucket/key)")
                outfile = f"/tmp/s3_object_{int(time.time())}"
                cmd = f"{base} s3 cp s3://{name} {outfile} && cat {outfile} && rm -f {outfile}"
            else:
                return ToolResult(output="", success=False, error=f"Unknown s3 action: {action}")
        else:
            return ToolResult(output="", success=False, error=f"Unknown service: {service}")

        start = time.monotonic()
        result = await execute(cmd, timeout=30)
        elapsed_ms = int((time.monotonic() - start) * 1000)

        output = ""
        if result.stdout:
            # Try to pretty-print JSON responses
            try:
                data = _json.loads(result.stdout)
                # For secrets, parse the nested SecretString
                if action == "get_secret" and "SecretString" in data:
                    try:
                        secret_val = _json.loads(data["SecretString"])
                        # Mask sensitive values (show first 4 chars only)
                        masked = {}
                        for k, v in secret_val.items():
                            if isinstance(v, str) and len(v) > 8:
                                masked[k] = v[:4] + "****"
                            else:
                                masked[k] = v
                        data["SecretString"] = masked
                    except _json.JSONDecodeError:
                        data["SecretString"] = data["SecretString"][:4] + "****"
                output = _json.dumps(data, indent=2)[:8000]
            except (_json.JSONDecodeError, ValueError):
                output = result.stdout[:8000]
        if result.stderr and result.returncode != 0:
            output += f"\nSTDERR: {result.stderr[:500]}"

        return ToolResult(
            output=output or "(no output)",
            success=result.returncode == 0,
            error=result.stderr[:200] if result.returncode != 0 else None,
            metadata={"service": service, "action": action, "latency_ms": elapsed_ms},
        )
