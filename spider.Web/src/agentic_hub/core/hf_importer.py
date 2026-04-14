"""HuggingFace GGUF importer — download models from HF and register with Ollama.

Flow:
1. Query HF API for GGUF files in a repository
2. Let user pick a quantization level
3. Download the .gguf file
4. Generate an Ollama Modelfile
5. Run `ollama create` to register the model
"""
from __future__ import annotations

import asyncio
import logging
import re
import subprocess
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import AsyncIterator

from huggingface_hub import HfApi, hf_hub_download

logger = logging.getLogger(__name__)

# Quantization levels ranked by quality (higher = better quality, larger file)
QUANT_PRIORITY = [
    "Q8_0", "Q6_K", "Q5_K_M", "Q5_K_S", "Q4_K_M", "Q4_K_S",
    "Q4_0", "Q3_K_M", "Q3_K_S", "Q2_K", "IQ4_XS", "IQ3_M",
]

# Common chat templates by model family
CHAT_TEMPLATES = {
    "llama": "{{ if .System }}<|start_header_id|>system<|end_header_id|>\n\n{{ .System }}<|eot_id|>{{ end }}{{ if .Prompt }}<|start_header_id|>user<|end_header_id|>\n\n{{ .Prompt }}<|eot_id|>{{ end }}<|start_header_id|>assistant<|end_header_id|>\n\n{{ .Response }}<|eot_id|>",
    "chatml": "{{ if .System }}<|im_start|>system\n{{ .System }}<|im_end|>\n{{ end }}{{ if .Prompt }}<|im_start|>user\n{{ .Prompt }}<|im_end|>\n{{ end }}<|im_start|>assistant\n{{ .Response }}<|im_end|>",
    "mistral": "[INST] {{ if .System }}{{ .System }}\n\n{{ end }}{{ .Prompt }} [/INST] {{ .Response }}",
    "phi": "{{ if .System }}<|system|>\n{{ .System }}<|end|>\n{{ end }}{{ if .Prompt }}<|user|>\n{{ .Prompt }}<|end|>\n{{ end }}<|assistant|>\n{{ .Response }}<|end|>",
    "gemma": "{{ if .System }}<start_of_turn>user\n{{ .System }}\n{{ end }}{{ if .Prompt }}<start_of_turn>user\n{{ .Prompt }}<end_of_turn>\n{{ end }}<start_of_turn>model\n{{ .Response }}<end_of_turn>",
    "deepseek": "{{ if .System }}<|begin▁of▁sentence|>{{ .System }}{{ end }}{{ if .Prompt }}User: {{ .Prompt }}\n{{ end }}Assistant: {{ .Response }}<|end▁of▁sentence|>",
}

# Heuristic: map repo name patterns to chat templates
FAMILY_PATTERNS = {
    "llama": re.compile(r"llama|meta-llama", re.I),
    "chatml": re.compile(r"qwen|yi-|deepseek-coder|openchat|starling", re.I),
    "mistral": re.compile(r"mistral|mixtral|zephyr", re.I),
    "phi": re.compile(r"phi-?[234]", re.I),
    "gemma": re.compile(r"gemma", re.I),
    "deepseek": re.compile(r"deepseek-r1|deepseek-v[23]", re.I),
}


@dataclass
class GGUFFile:
    """A GGUF file found in a HuggingFace repository."""
    filename: str
    size_bytes: int
    quant: str
    repo_id: str

    @property
    def size_gb(self) -> float:
        return self.size_bytes / (1024 ** 3)


def _detect_quant(filename: str) -> str:
    """Extract quantization level from a GGUF filename."""
    # Match patterns like Q4_K_M, Q5_K_S, IQ4_XS, etc.
    match = re.search(r"((?:IQ|Q)\d[_A-Z]*\d?(?:_[KMSXL]+)?)", filename, re.I)
    if match:
        return match.group(1).upper()
    return "UNKNOWN"


def _detect_template(repo_id: str) -> str:
    """Guess the chat template from the repo name."""
    for family, pattern in FAMILY_PATTERNS.items():
        if pattern.search(repo_id):
            return family
    # Default to chatml (most widely used)
    return "chatml"


class HFImporter:
    """Import GGUF models from HuggingFace into Ollama."""

    def __init__(self):
        self._api = HfApi()

    def list_gguf_files(self, repo_id: str) -> list[GGUFFile]:
        """List all GGUF files in a HuggingFace repo."""
        try:
            files = self._api.list_repo_files(repo_id)
        except Exception as e:
            raise ValueError(f"Could not access repo '{repo_id}': {e}")

        gguf_files = []
        # Get file sizes
        repo_info = self._api.repo_info(repo_id, files_metadata=True)
        size_map = {}
        if repo_info.siblings:
            size_map = {s.rfilename: s.size for s in repo_info.siblings if s.size}

        for f in files:
            if f.endswith(".gguf"):
                quant = _detect_quant(f)
                gguf_files.append(GGUFFile(
                    filename=f,
                    size_bytes=size_map.get(f, 0),
                    quant=quant,
                    repo_id=repo_id,
                ))

        # Sort by quant quality
        def sort_key(g: GGUFFile) -> int:
            try:
                return QUANT_PRIORITY.index(g.quant)
            except ValueError:
                return 999

        gguf_files.sort(key=sort_key)
        return gguf_files

    def find_best_gguf(
        self, repo_id: str, preferred_quant: str = "Q4_K_M", max_size_gb: float = 6.0
    ) -> GGUFFile | None:
        """Find the best GGUF file matching constraints."""
        files = self.list_gguf_files(repo_id)
        if not files:
            return None

        # Try exact quant match first
        for f in files:
            if f.quant == preferred_quant.upper() and f.size_gb <= max_size_gb:
                return f

        # Fall back to best that fits
        for f in files:
            if f.size_gb <= max_size_gb:
                return f

        return files[-1] if files else None  # Smallest available

    def download_gguf(
        self, repo_id: str, filename: str, dest_dir: Path | None = None
    ) -> Path:
        """Download a GGUF file from HuggingFace. Returns local path."""
        if dest_dir is None:
            dest_dir = Path(tempfile.mkdtemp(prefix="spider-web-"))

        logger.info(f"Downloading {repo_id}/{filename}...")
        local_path = hf_hub_download(
            repo_id=repo_id,
            filename=filename,
            local_dir=str(dest_dir),
        )
        return Path(local_path)

    def generate_modelfile(
        self, gguf_path: Path, repo_id: str, template_family: str | None = None
    ) -> str:
        """Generate an Ollama Modelfile for a GGUF model."""
        if template_family is None:
            template_family = _detect_template(repo_id)

        template = CHAT_TEMPLATES.get(template_family, CHAT_TEMPLATES["chatml"])

        modelfile = f"""FROM {gguf_path}

TEMPLATE \"\"\"{template}\"\"\"

PARAMETER stop "<|im_end|>"
PARAMETER stop "<|eot_id|>"
PARAMETER stop "<|end|>"
PARAMETER stop "<end_of_turn>"
PARAMETER temperature 0.7
PARAMETER num_ctx 4096
"""
        return modelfile

    def create_ollama_model(
        self, model_name: str, modelfile_content: str, modelfile_dir: Path
    ) -> str:
        """Register a model with Ollama using `ollama create`. Returns output."""
        modelfile_path = modelfile_dir / "Modelfile"
        modelfile_path.write_text(modelfile_content)

        result = subprocess.run(
            ["ollama", "create", model_name, "-f", str(modelfile_path)],
            capture_output=True,
            text=True,
            timeout=300,
        )

        if result.returncode != 0:
            raise RuntimeError(f"ollama create failed: {result.stderr}")

        return result.stdout.strip()

    def import_model(
        self,
        repo_id: str,
        model_name: str | None = None,
        preferred_quant: str = "Q4_K_M",
        max_size_gb: float = 6.0,
        template_family: str | None = None,
    ) -> dict:
        """Full import pipeline: find → download → create.

        Returns info dict about the imported model.
        """
        # Step 1: Find the best GGUF
        gguf = self.find_best_gguf(repo_id, preferred_quant, max_size_gb)
        if gguf is None:
            raise ValueError(f"No suitable GGUF files found in {repo_id}")

        # Step 2: Generate model name if not provided
        if model_name is None:
            # e.g. "bartowski/Qwen2.5-Coder-7B-Instruct-GGUF" -> "qwen2.5-coder-7b"
            base = repo_id.split("/")[-1]
            base = re.sub(r"-GGUF$", "", base, flags=re.I)
            base = re.sub(r"-Instruct$", "", base, flags=re.I)
            model_name = base.lower()

        # Step 3: Download
        dest_dir = Path(tempfile.mkdtemp(prefix="spider-web-"))
        gguf_path = self.download_gguf(repo_id, gguf.filename, dest_dir)

        # Step 4: Generate Modelfile
        if template_family is None:
            template_family = _detect_template(repo_id)
        modelfile = self.generate_modelfile(gguf_path, repo_id, template_family)

        # Step 5: Register with Ollama
        output = self.create_ollama_model(model_name, modelfile, dest_dir)

        return {
            "model_name": model_name,
            "repo_id": repo_id,
            "gguf_file": gguf.filename,
            "quant": gguf.quant,
            "size_gb": round(gguf.size_gb, 2),
            "template": template_family,
            "ollama_output": output,
        }
