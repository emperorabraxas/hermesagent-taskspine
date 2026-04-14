"""Multi-step pipeline system — chain agents with state passing.

Pipelines define sequences of agent steps where each step can:
- Use a specific agent with specific tools
- Reference previous step outputs via {variables}
- Conditionally skip based on state
- Run the full tool-calling loop per step
"""
from __future__ import annotations

import logging
import re
from dataclasses import dataclass, field
from typing import Any, AsyncIterator

from agentic_hub.config import load_models_config, get_settings
from agentic_hub.core.gpu_scheduler import get_gpu_scheduler
from agentic_hub.core.ollama_client import get_ollama
from agentic_hub.core.tools.registry import get_registry
from agentic_hub.core.tools.llm_response import LLMResponse

logger = logging.getLogger(__name__)


@dataclass
class PipelineStep:
    """One step in a pipeline."""
    agent: str                          # Agent to use (scholar, automator, oracle, code_team)
    prompt_template: str                # Can use {user_message}, {previous_output}, {step_N_output}
    tools: list[str] | None = None      # Override tool set (None = use agent defaults)
    condition: str | None = None        # Python expression — skip step if False
    max_tool_rounds: int = 3
    label: str = ""                     # Display name for this step


@dataclass
class PipelineResult:
    """Result from one pipeline step."""
    agent: str
    output: str
    tool_calls_count: int = 0
    tokens_in: int = 0
    tokens_out: int = 0


class Pipeline:
    """A sequence of agent steps with state passing between them."""

    def __init__(self, name: str, steps: list[PipelineStep], description: str = ""):
        self.name = name
        self.steps = steps
        self.description = description

    def to_dag(self):
        """Convert this linear pipeline to a DAGDefinition."""
        from agentic_hub.core.dag import pipeline_to_dag
        return pipeline_to_dag(self)

    async def execute(
        self,
        user_message: str,
        conversation_history: list[dict] | None = None,
    ) -> AsyncIterator[str]:
        """Execute all pipeline steps, yielding SSE-compatible events."""
        state: dict[str, Any] = {"user_message": user_message}
        previous_output = ""
        settings = get_settings()
        config = load_models_config()
        registry = get_registry()
        ollama = get_ollama()

        yield f"§SPIDER:pipeline:🔗 Pipeline '{self.name}' — {len(self.steps)} steps"

        for i, step in enumerate(self.steps):
            step_label = step.label or f"Step {i + 1}: {step.agent}"

            # Check condition
            if step.condition:
                try:
                    if not eval(step.condition, {"__builtins__": {}}, {"state": state}):
                        yield f"§SPIDER:pipeline:⏭️ Skipping {step_label} (condition not met)"
                        continue
                except Exception as e:
                    logger.warning(f"Pipeline condition error: {e}")

            yield f"§SPIDER:pipeline:▶️ {step_label}"
            yield f"\n\n**{step_label}**\n\n"

            # Resolve prompt template
            prompt = step.prompt_template.format(
                user_message=user_message,
                previous_output=previous_output,
                **{f"step_{j}_output": state.get(f"step_{j}_output", "") for j in range(i)},
            )

            # Get agent config
            agent_cfg = config.get("agents", {}).get(step.agent, {})
            model_name = agent_cfg.get("local_model", "")
            system_prompt = agent_cfg.get("system_prompt", "")
            cloud_model = agent_cfg.get("cloud_model", "")
            cloud_provider = agent_cfg.get("cloud_provider", "")

            # Get tools for this step
            if step.tools is not None:
                tool_schemas = [t.to_json_schema() for t in registry.get_all_tools()
                                if t.name in step.tools]
            else:
                tool_schemas = registry.get_schemas_for_agent(step.agent)

            # Build messages
            messages = []
            if system_prompt:
                messages.append({"role": "system", "content": system_prompt})
            if previous_output:
                messages.append({"role": "system", "content": f"Previous step output:\n{previous_output[:3000]}"})
            if conversation_history:
                messages.extend(conversation_history[-4:])
            messages.append({"role": "user", "content": prompt})

            # Tool-calling loop for this step
            step_output = ""
            tool_count = 0
            tokens_in = 0
            tokens_out = 0

            for tool_round in range(step.max_tool_rounds + 1):
                llm_result: LLMResponse | None = None

                # Try cloud first
                if cloud_model and cloud_provider:
                    try:
                        from agentic_hub.core.cloud_client import get_cloud_client
                        client = get_cloud_client(cloud_provider)
                        if client and hasattr(client, 'chat_completion'):
                            if cloud_provider == "anthropic":
                                system_msg = "\n".join(m["content"] for m in messages if m["role"] == "system")
                                user_msgs = [m for m in messages if m["role"] != "system"]
                                anthropic_schemas = registry.get_schemas_for_agent(step.agent, provider="anthropic")
                                llm_result = await client.chat_completion(
                                    messages=user_msgs, model=cloud_model, system=system_msg,
                                    tools=anthropic_schemas if tool_schemas else None, max_tokens=4096,
                                )
                            else:
                                llm_result = await client.chat_completion(
                                    messages=messages, model=cloud_model,
                                    tools=tool_schemas if tool_schemas else None, max_tokens=4096,
                                )
                    except Exception as e:
                        logger.warning(f"Pipeline cloud {cloud_provider} failed: {e}")

                if llm_result is None and model_name:
                    scheduler = get_gpu_scheduler()
                    await scheduler.ensure_model(model_name)
                    llm_result = await ollama.chat_completion(
                        model=model_name, messages=messages,
                        tools=tool_schemas if tool_schemas else None,
                        keep_alive=settings.model_keep_alive,
                    )

                if llm_result is None:
                    yield f"§SPIDER:pipeline:⚠️ {step_label} failed — no model available"
                    break

                tokens_in += llm_result.tokens_in
                tokens_out += llm_result.tokens_out

                if llm_result.has_tool_calls:
                    messages.append({"role": "assistant", "content": llm_result.text or ""})
                    for tc in llm_result.tool_calls:
                        tool = registry.get_tool(tc.name)
                        if tool:
                            yield f"§SPIDER:{step.agent}:🔧 {tc.name}"
                            result = await tool.execute(**tc.arguments)
                            tool_count += 1
                            messages.append({
                                "role": "tool" if cloud_provider != "anthropic" else "user",
                                "content": result.output[:5000],
                                **({"tool_call_id": tc.call_id} if tc.call_id else {}),
                            })
                    continue
                else:
                    step_output = llm_result.text or ""
                    break

            # Store result in state
            previous_output = step_output
            state[f"step_{i}_output"] = step_output

            yield step_output
            yield f"\n\n§SPIDER:pipeline:✅ {step_label} complete ({tokens_in}+{tokens_out} tokens, {tool_count} tools)"

        yield f"\n\n§SPIDER:pipeline:🏁 Pipeline '{self.name}' complete"


# === BUILT-IN PIPELINE TEMPLATES ===

RESEARCH_PIPELINE = Pipeline(
    name="Deep Research",
    description="Scholar researches → R1 validates → Oracle synthesizes",
    steps=[
        PipelineStep(
            agent="scholar",
            prompt_template=(
                "Research this topic thoroughly using all available tools. "
                "Search the knowledge base, read relevant files, and gather data.\n\n"
                "Topic: {user_message}"
            ),
            label="Scholar: Research",
        ),
        PipelineStep(
            agent="oracle",
            prompt_template=(
                "The Scholar has gathered the following research:\n\n{previous_output}\n\n"
                "Synthesize this into a clear, actionable summary. Identify key findings, "
                "gaps, and recommendations. Be concise but comprehensive.\n\n"
                "Original question: {user_message}"
            ),
            tools=[],  # Oracle synthesizes, no tools needed
            label="Oracle: Synthesize",
        ),
    ],
)

CODE_PIPELINE = Pipeline(
    name="Full Code Pipeline",
    description="Scholar understands → Code Team implements → Automator tests",
    steps=[
        PipelineStep(
            agent="scholar",
            prompt_template=(
                "Analyze the codebase to understand what needs to change for this task. "
                "Read relevant files and identify the implementation approach.\n\n"
                "Task: {user_message}"
            ),
            label="Scholar: Analyze",
        ),
        PipelineStep(
            agent="code_team",
            prompt_template=(
                "Based on this analysis:\n\n{previous_output}\n\n"
                "Implement the solution. Write the code, create/modify files as needed.\n\n"
                "Task: {user_message}"
            ),
            label="Code Team: Implement",
        ),
        PipelineStep(
            agent="automator",
            prompt_template=(
                "The Code Team just implemented changes:\n\n{previous_output}\n\n"
                "Run any relevant tests, linting, or validation to verify the changes work.\n\n"
                "Original task: {user_message}"
            ),
            label="Automator: Test & Verify",
        ),
    ],
)

ANALYSIS_PIPELINE = Pipeline(
    name="Data Analysis",
    description="Scholar gathers → Oracle analyzes → Scholar summarizes",
    steps=[
        PipelineStep(
            agent="scholar",
            prompt_template=(
                "Gather all relevant data for this analysis. Search the knowledge base, "
                "read files, and collect information.\n\n"
                "Analysis request: {user_message}"
            ),
            label="Scholar: Gather Data",
        ),
        PipelineStep(
            agent="oracle",
            prompt_template=(
                "Analyze this data:\n\n{previous_output}\n\n"
                "Identify patterns, trends, anomalies, and insights. "
                "Be analytical and data-driven.\n\n"
                "Original request: {user_message}"
            ),
            tools=[],
            label="Oracle: Analyze",
        ),
        PipelineStep(
            agent="scholar",
            prompt_template=(
                "Based on this analysis:\n\n{previous_output}\n\n"
                "Write a concise executive summary with key findings and "
                "actionable recommendations.\n\n"
                "Original request: {user_message}"
            ),
            tools=[],
            label="Scholar: Summarize",
        ),
    ],
)

# Pipeline registry
PIPELINES: dict[str, Pipeline] = {
    "research": RESEARCH_PIPELINE,
    "code": CODE_PIPELINE,
    "analysis": ANALYSIS_PIPELINE,
}


def get_pipeline(name: str) -> Pipeline | None:
    return PIPELINES.get(name)
