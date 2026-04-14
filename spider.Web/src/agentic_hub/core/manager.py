"""Manager Agent — Opus as autonomous task decomposer and quality controller.

Flow:
  1. User request → Manager decomposes into subtasks (DAG)
  2. Each subtask delegated to appropriate spider
  3. Manager reviews each spider's output quality
  4. Manager synthesizes final deliverable

Falls back to standard pipeline dispatch when Opus is unavailable.
"""
from __future__ import annotations

import json
import logging
from typing import AsyncIterator

from agentic_hub.config import load_models_config, get_settings
from agentic_hub.core.dag import DAGDefinition, DAGNode, DAGEdge, DAGExecutor, NodeType

logger = logging.getLogger(__name__)

# Available spiders and their capabilities (injected into decomposition prompt)
SPIDER_CAPABILITIES = """Available agents:
- scholar: Research, analysis, RAG search, web lookup. Best for gathering information.
- oracle: Strategic synthesis, decision-making, debate. Best for analyzing and summarizing.
- automator: Shell commands, file operations, testing, deployment. Best for system tasks.
- code_team: Software engineering — Lead (Opus) + Coder (GPT). Best for writing/reviewing code.
"""

DECOMPOSE_PROMPT = """You are the Manager Agent for spider.Web, a multi-agent AI platform.

Your job: break down the user's request into a DAG (directed acyclic graph) of subtasks.
Each subtask is assigned to the best agent for that job.

{capabilities}

RULES:
1. Use the minimum number of steps needed (don't over-decompose simple tasks)
2. Use parallel steps when subtasks are independent (they'll run concurrently)
3. Always end with a synthesis step (oracle) that combines outputs
4. For code tasks, use scholar→code_team→automator (analyze→implement→test)
5. For research, use scholar + oracle in parallel → oracle synthesis
6. Simple tasks (1-2 steps) don't need a manager — but you're called for complex ones

Return ONLY valid JSON in this exact format:
{{
  "name": "descriptive_name",
  "description": "what this workflow does",
  "nodes": [
    {{"id": "unique_id", "type": "agent", "agent": "scholar|oracle|automator|code_team",
      "prompt_template": "instructions for this agent. Use {{user_message}} for the original request.",
      "label": "Step Name"}}
  ],
  "edges": [
    {{"source": "node_id", "target": "node_id"}}
  ]
}}

Node types: "agent" (run a spider), "merge" (combine outputs from multiple predecessors).
For parallel execution: multiple nodes with no edges between them.
For sequential: chain edges source→target.

User's request: {user_message}"""

REVIEW_PROMPT = """Review this agent output for quality and completeness.

Original task: {user_message}
Agent: {agent_name}
Step: {step_label}

Output to review:
{output}

Is this output:
1. Complete — addresses what was asked?
2. Accurate — no obvious errors?
3. Useful — provides actionable content?

If the output is acceptable, respond with: APPROVED
If it needs improvement, respond with: REVISION NEEDED: <specific feedback>"""

SYNTHESIZE_PROMPT = """You are the Manager Agent synthesizing the final deliverable.

Original request: {user_message}

The following agents contributed:

{agent_outputs}

Synthesize these into a single, coherent response that:
1. Directly addresses the user's original request
2. Incorporates the best insights from each agent
3. Resolves any contradictions between agents
4. Is clear, actionable, and well-structured

Do NOT mention the agents or the process — just deliver the final answer."""


class ManagerAgent:
    """Opus-powered autonomous task decomposition and quality control."""

    def __init__(self):
        self._settings = get_settings()
        self._config = load_models_config()

    async def process(
        self,
        user_message: str,
        conversation_history: list[dict] | None = None,
    ) -> AsyncIterator[str]:
        """Full manager flow: decompose → delegate → review → synthesize."""
        yield "§SPIDER:manager:🧠 Analyzing task complexity..."

        # Step 1: Decompose into DAG
        dag = await self._decompose(user_message)
        if dag is None:
            yield "§SPIDER:manager:⚠️ Could not decompose task — falling back to direct routing"
            return

        yield f"§SPIDER:manager:📊 Decomposed into {len(dag.nodes)} subtasks"
        yield f"\n\n**Manager Plan: {dag.description}**\n\n"

        # Show the plan
        for node in dag.nodes:
            if node.type == NodeType.AGENT:
                yield f"- **{node.label}** → {node.agent}\n"

        yield "\n---\n\n"

        # Step 2: Execute the DAG
        executor = DAGExecutor(dag)
        async for event in executor.execute(user_message, conversation_history):
            yield event

        # Step 3: Synthesize if multiple outputs
        agent_outputs = executor._node_outputs
        if len([v for v in agent_outputs.values() if v.strip()]) > 1:
            yield "\n\n---\n\n"
            yield "§SPIDER:manager:📝 Synthesizing final output..."

            synthesis = await self._synthesize(user_message, agent_outputs, dag)
            if synthesis:
                yield "\n\n**Final Synthesis**\n\n"
                yield synthesis

        yield "\n\n§SPIDER:manager:✅ Manager workflow complete"

    async def _decompose(self, user_message: str) -> DAGDefinition | None:
        """Use Opus/cloud LLM to decompose task into a DAG."""
        prompt = DECOMPOSE_PROMPT.format(
            capabilities=SPIDER_CAPABILITIES,
            user_message=user_message,
        )

        messages = [{"role": "user", "content": prompt}]

        # Try cloud (prefer Opus for decomposition)
        response_text = await self._call_manager_llm(
            messages,
            system="You are a task decomposition engine. Return ONLY valid JSON.",
        )

        if not response_text:
            return None

        # Parse JSON from response
        try:
            # Extract JSON from potential markdown code blocks
            text = response_text.strip()
            if "```json" in text:
                text = text.split("```json")[1].split("```")[0].strip()
            elif "```" in text:
                text = text.split("```")[1].split("```")[0].strip()

            data = json.loads(text)
            dag = DAGDefinition.from_dict(data)

            errors = dag.validate()
            if errors:
                logger.warning(f"Manager DAG validation errors: {errors}")
                return None

            return dag

        except (json.JSONDecodeError, KeyError, ValueError) as e:
            logger.warning(f"Manager decomposition parse error: {e}")
            return None

    async def _synthesize(
        self,
        user_message: str,
        agent_outputs: dict[str, str],
        dag: DAGDefinition,
    ) -> str | None:
        """Synthesize all agent outputs into final deliverable."""
        # Build agent output summary
        output_parts = []
        for node in dag.nodes:
            if node.type == NodeType.AGENT and node.id in agent_outputs:
                output = agent_outputs[node.id]
                if output.strip():
                    output_parts.append(
                        f"### {node.label} ({node.agent})\n{output[:3000]}"
                    )

        if not output_parts:
            return None

        prompt = SYNTHESIZE_PROMPT.format(
            user_message=user_message,
            agent_outputs="\n\n".join(output_parts),
        )

        return await self._call_manager_llm(
            [{"role": "user", "content": prompt}],
            system="You are a synthesis expert. Combine multiple perspectives into one clear answer.",
        )

    async def _call_manager_llm(
        self,
        messages: list[dict],
        system: str = "",
        max_tokens: int = 4096,
    ) -> str | None:
        """Call the manager's LLM (Opus preferred, local fallback)."""
        settings = self._settings

        # Try Anthropic (Opus) first — best for task decomposition
        if settings.anthropic_api_key:
            try:
                from agentic_hub.core.cloud_client import get_cloud_client
                client = get_cloud_client("anthropic")
                if client:
                    result = await client.chat_completion(
                        messages=messages,
                        model="claude-opus-4-20250514",
                        system=system,
                        max_tokens=max_tokens,
                    )
                    if result and result.text:
                        return result.text
            except Exception as e:
                logger.warning(f"Manager Opus call failed: {e}")

        # Try OpenAI (GPT-5.4)
        if settings.openai_api_key:
            try:
                from agentic_hub.core.cloud_client import get_cloud_client
                client = get_cloud_client("openai")
                if client:
                    msgs = messages.copy()
                    if system:
                        msgs.insert(0, {"role": "system", "content": system})
                    result = await client.chat_completion(
                        messages=msgs, model="gpt-4.1", max_tokens=max_tokens,
                    )
                    if result and result.text:
                        return result.text
            except Exception as e:
                logger.warning(f"Manager OpenAI call failed: {e}")

        # Local fallback (DeepSeek R1 — best local reasoning)
        try:
            from agentic_hub.core.ollama_client import get_ollama
            from agentic_hub.core.gpu_scheduler import get_gpu_scheduler
            model = "deepseek-r1:7b"
            scheduler = get_gpu_scheduler()
            await scheduler.ensure_model(model)
            ollama = get_ollama()
            msgs = messages.copy()
            if system:
                msgs.insert(0, {"role": "system", "content": system})
            result = await ollama.chat_completion(
                model=model, messages=msgs,
                keep_alive=settings.model_keep_alive,
            )
            if result and result.text:
                return result.text
        except Exception as e:
            logger.warning(f"Manager local call failed: {e}")

        return None


# Singleton
_manager: ManagerAgent | None = None


def get_manager() -> ManagerAgent:
    global _manager
    if _manager is None:
        _manager = ManagerAgent()
    return _manager
