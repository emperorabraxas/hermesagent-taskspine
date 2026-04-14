"""Automator agent — workflow automation, git ops, shell commands."""
from __future__ import annotations

from typing import AsyncIterator

from agentic_hub.agents.base import AgentInfo, BaseAgent
from agentic_hub.config import get_settings, load_models_config
from agentic_hub.core.gpu_scheduler import get_gpu_scheduler
from agentic_hub.core.ollama_client import get_ollama


class AutomatorAgent(BaseAgent):
    def __init__(self):
        config = load_models_config()
        agent_cfg = config["agents"]["automator"]
        settings = get_settings()
        self._model = settings.automator_model or agent_cfg["local_model"]
        self._system_prompt = agent_cfg.get("system_prompt", "")
        self._info = AgentInfo(
            name="automator",
            display_name=agent_cfg["display_name"],
            description=agent_cfg["description"],
            local_model=self._model,
            xp_base=agent_cfg.get("xp_base", 15),
        )

    @property
    def info(self) -> AgentInfo:
        return self._info

    async def process(
        self,
        user_message: str,
        conversation_history: list[dict] | None = None,
        stream: bool = True,
    ) -> str | AsyncIterator[str]:
        scheduler = get_gpu_scheduler()
        await scheduler.ensure_model(self._model)

        messages = []
        if self._system_prompt:
            messages.append({"role": "system", "content": self._system_prompt})
        if conversation_history:
            messages.extend(conversation_history[-6:])
        messages.append({"role": "user", "content": user_message})

        ollama = get_ollama()
        return await ollama.chat(
            model=self._model,
            messages=messages,
            stream=stream,
            keep_alive=get_settings().model_keep_alive,
        )
