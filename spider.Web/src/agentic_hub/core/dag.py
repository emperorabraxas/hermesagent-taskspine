"""DAG executor — graph-based multi-agent workflow engine.

Replaces linear Pipeline with a DAG supporting:
  - Parallel fan-out (asyncio.gather)
  - Conditional branching (evaluate expressions, pick branch)
  - Merge/join (wait for all parallel paths)
  - Loop nodes (re-execute subgraph until condition fails, max iterations)
  - HITL nodes (pause for user input — Phase 6)

Existing Pipeline templates auto-convert via Pipeline.to_dag().
"""
from __future__ import annotations

import asyncio
import json
import logging
import uuid
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, AsyncIterator

from agentic_hub.config import load_models_config, get_settings
from agentic_hub.core.gpu_scheduler import get_gpu_scheduler
from agentic_hub.core.ollama_client import get_ollama
from agentic_hub.core.tools.registry import get_registry
from agentic_hub.core.tools.llm_response import LLMResponse

logger = logging.getLogger(__name__)


class NodeType(Enum):
    AGENT = "agent"           # Run an agent with a prompt
    CONDITION = "condition"   # Evaluate expression, pick branch
    PARALLEL = "parallel"     # Fan-out: trigger all successors concurrently
    MERGE = "merge"           # Fan-in: wait for all predecessors, combine outputs
    HITL = "hitl"             # Pause for human input (Phase 6)
    LOOP = "loop"             # Re-execute predecessors until condition fails


@dataclass
class DAGNode:
    id: str
    type: NodeType
    agent: str = ""                          # For AGENT nodes
    prompt_template: str = ""                # For AGENT/HITL nodes
    condition: str = ""                      # For CONDITION/LOOP nodes
    tools: list[str] | None = None           # Tool override (None = agent defaults)
    max_tool_rounds: int = 3                 # For AGENT nodes
    max_iterations: int = 5                  # For LOOP nodes
    label: str = ""                          # Display name
    metadata: dict = field(default_factory=dict)

    def to_dict(self) -> dict:
        return {
            "id": self.id, "type": self.type.value, "agent": self.agent,
            "prompt_template": self.prompt_template, "condition": self.condition,
            "tools": self.tools, "max_tool_rounds": self.max_tool_rounds,
            "max_iterations": self.max_iterations, "label": self.label,
            "metadata": self.metadata,
        }

    @classmethod
    def from_dict(cls, d: dict) -> DAGNode:
        return cls(
            id=d["id"], type=NodeType(d["type"]), agent=d.get("agent", ""),
            prompt_template=d.get("prompt_template", ""), condition=d.get("condition", ""),
            tools=d.get("tools"), max_tool_rounds=d.get("max_tool_rounds", 3),
            max_iterations=d.get("max_iterations", 5), label=d.get("label", ""),
            metadata=d.get("metadata", {}),
        )


@dataclass
class DAGEdge:
    source: str              # Node ID
    target: str              # Node ID
    condition_value: str = ""  # For CONDITION edges: "true"/"false"/"branch_name"

    def to_dict(self) -> dict:
        return {"source": self.source, "target": self.target, "condition_value": self.condition_value}

    @classmethod
    def from_dict(cls, d: dict) -> DAGEdge:
        return cls(source=d["source"], target=d["target"], condition_value=d.get("condition_value", ""))


@dataclass
class DAGDefinition:
    """Complete DAG workflow definition."""
    name: str
    nodes: list[DAGNode]
    edges: list[DAGEdge]
    description: str = ""

    def validate(self) -> list[str]:
        """Validate the DAG. Returns list of error messages (empty = valid)."""
        errors = []
        node_ids = {n.id for n in self.nodes}

        for edge in self.edges:
            if edge.source not in node_ids:
                errors.append(f"Edge source '{edge.source}' not found in nodes")
            if edge.target not in node_ids:
                errors.append(f"Edge target '{edge.target}' not found in nodes")

        # Check for entry nodes
        targets = {e.target for e in self.edges}
        entry_nodes = [n for n in self.nodes if n.id not in targets]
        if not entry_nodes:
            errors.append("No entry nodes (all nodes have incoming edges — possible cycle)")

        # Agent nodes must have an agent
        for n in self.nodes:
            if n.type == NodeType.AGENT and not n.agent:
                errors.append(f"Agent node '{n.id}' has no agent specified")
            if n.type in (NodeType.CONDITION, NodeType.LOOP) and not n.condition:
                errors.append(f"{n.type.value} node '{n.id}' has no condition expression")

        return errors

    def get_entry_nodes(self) -> list[str]:
        """Get nodes with no incoming edges."""
        targets = {e.target for e in self.edges}
        return [n.id for n in self.nodes if n.id not in targets]

    def get_successors(self, node_id: str) -> list[DAGEdge]:
        """Get outgoing edges from a node."""
        return [e for e in self.edges if e.source == node_id]

    def get_predecessors(self, node_id: str) -> list[DAGEdge]:
        """Get incoming edges to a node."""
        return [e for e in self.edges if e.target == node_id]

    def get_node(self, node_id: str) -> DAGNode | None:
        for n in self.nodes:
            if n.id == node_id:
                return n
        return None

    def to_dict(self) -> dict:
        return {
            "name": self.name, "description": self.description,
            "nodes": [n.to_dict() for n in self.nodes],
            "edges": [e.to_dict() for e in self.edges],
        }

    @classmethod
    def from_dict(cls, d: dict) -> DAGDefinition:
        return cls(
            name=d["name"], description=d.get("description", ""),
            nodes=[DAGNode.from_dict(n) for n in d["nodes"]],
            edges=[DAGEdge.from_dict(e) for e in d["edges"]],
        )


class DAGExecutor:
    """Execute a DAG workflow with parallel, conditional, and loop support."""

    def __init__(self, dag: DAGDefinition):
        self.dag = dag
        self._state: dict[str, Any] = {}
        self._node_status: dict[str, str] = {n.id: "pending" for n in dag.nodes}
        self._node_outputs: dict[str, str] = {}
        self._event_queue: asyncio.Queue[str] = asyncio.Queue()
        self._loop_counts: dict[str, int] = {}

    async def execute(
        self,
        user_message: str,
        conversation_history: list[dict] | None = None,
    ) -> AsyncIterator[str]:
        """Execute the DAG, yielding SSE-compatible events."""
        self._state["user_message"] = user_message
        self._state["conversation_history"] = conversation_history

        yield f"§SPIDER:dag:🕸️ DAG '{self.dag.name}' — {len(self.dag.nodes)} nodes"

        # Start from entry nodes
        ready = self.dag.get_entry_nodes()

        while ready:
            # Separate into parallel batch (all ready nodes with deps met)
            batch = [nid for nid in ready if self._deps_satisfied(nid)]
            if not batch:
                # Deadlock — remaining nodes have unmet deps
                yield f"§SPIDER:dag:⚠️ Deadlock detected — {len(ready)} nodes stuck"
                break

            if len(batch) == 1:
                # Single node — execute directly
                async for event in self._execute_node(batch[0]):
                    yield event
            else:
                # Parallel execution
                yield f"§SPIDER:dag:⚡ Parallel batch: {', '.join(batch)}"
                async for event in self._execute_parallel(batch):
                    yield event

            # Determine next ready nodes
            ready = self._get_next_ready()

        yield f"\n\n§SPIDER:dag:🏁 DAG '{self.dag.name}' complete"

    def _deps_satisfied(self, node_id: str) -> bool:
        """Check if all predecessor nodes are done."""
        preds = self.dag.get_predecessors(node_id)
        for edge in preds:
            if self._node_status.get(edge.source) != "done":
                return False
        return True

    def _get_next_ready(self) -> list[str]:
        """Find nodes that are pending and have all dependencies satisfied."""
        ready = []
        for node in self.dag.nodes:
            if self._node_status[node.id] != "pending":
                continue
            if self._deps_satisfied(node.id):
                ready.append(node.id)
        return ready

    async def _execute_parallel(self, node_ids: list[str]) -> AsyncIterator[str]:
        """Execute multiple nodes concurrently, collecting events."""
        # Collect all events from parallel nodes into a queue
        queue: asyncio.Queue[tuple[str, str | None]] = asyncio.Queue()

        async def _run_node(nid: str):
            async for event in self._execute_node(nid):
                await queue.put((nid, event))
            await queue.put((nid, None))  # Signal done

        tasks = [asyncio.create_task(_run_node(nid)) for nid in node_ids]
        done_count = 0

        while done_count < len(node_ids):
            nid, event = await queue.get()
            if event is None:
                done_count += 1
            else:
                yield event

        # Ensure all tasks complete
        await asyncio.gather(*tasks, return_exceptions=True)

    async def _execute_node(self, node_id: str) -> AsyncIterator[str]:
        """Execute a single node based on its type."""
        node = self.dag.get_node(node_id)
        if node is None:
            return

        self._node_status[node_id] = "running"
        label = node.label or f"{node.type.value}:{node_id}"
        yield f"§SPIDER:dag:▶️ {label}"

        if node.type == NodeType.AGENT:
            async for event in self._run_agent(node):
                yield event

        elif node.type == NodeType.CONDITION:
            await self._run_condition(node)
            yield f"§SPIDER:dag:🔀 {label} → {self._state.get(f'_condition_{node.id}', '?')}"

        elif node.type == NodeType.PARALLEL:
            # Fan-out: mark all successors as pending (they already are)
            yield f"§SPIDER:dag:⚡ {label} — fan-out"

        elif node.type == NodeType.MERGE:
            self._run_merge(node)
            yield f"§SPIDER:dag:🔗 {label} — merged {len(self.dag.get_predecessors(node.id))} inputs"

        elif node.type == NodeType.LOOP:
            async for event in self._run_loop(node):
                yield event

        elif node.type == NodeType.HITL:
            async for event in self._run_hitl(node):
                yield event

        self._node_status[node_id] = "done"
        yield f"§SPIDER:dag:✅ {label}"

    async def _run_agent(self, node: DAGNode) -> AsyncIterator[str]:
        """Execute an agent node with tool-calling loop."""
        settings = get_settings()
        config = load_models_config()
        registry = get_registry()
        ollama = get_ollama()

        agent_cfg = config.get("agents", {}).get(node.agent, {})
        model_name = agent_cfg.get("local_model", "")
        system_prompt = agent_cfg.get("system_prompt", "")
        cloud_model = agent_cfg.get("cloud_model", "")
        cloud_provider = agent_cfg.get("cloud_provider", "")

        # Resolve prompt template with state
        prompt = self._resolve_template(node.prompt_template)

        # Build tool schemas
        if node.tools is not None:
            tool_schemas = [t.to_json_schema() for t in registry.get_all_tools()
                            if t.name in node.tools]
        else:
            tool_schemas = registry.get_schemas_for_agent(node.agent)

        # Build messages
        messages: list[dict] = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})

        # Inject predecessor outputs as context
        preds = self.dag.get_predecessors(node.id)
        for edge in preds:
            pred_output = self._node_outputs.get(edge.source, "")
            if pred_output:
                messages.append({"role": "system", "content": f"Input from {edge.source}:\n{pred_output[:3000]}"})

        history = self._state.get("conversation_history")
        if history:
            messages.extend(history[-4:])
        messages.append({"role": "user", "content": prompt})

        # Tool-calling loop
        output = ""
        tool_count = 0

        for _ in range(node.max_tool_rounds + 1):
            llm_result: LLMResponse | None = None

            # Cloud first
            if cloud_model and cloud_provider:
                try:
                    from agentic_hub.core.cloud_client import get_cloud_client
                    client = get_cloud_client(cloud_provider)
                    if client and hasattr(client, "chat_completion"):
                        if cloud_provider == "anthropic":
                            sys_msg = "\n".join(m["content"] for m in messages if m["role"] == "system")
                            user_msgs = [m for m in messages if m["role"] != "system"]
                            anth_schemas = registry.get_schemas_for_agent(node.agent, provider="anthropic")
                            llm_result = await client.chat_completion(
                                messages=user_msgs, model=cloud_model, system=sys_msg,
                                tools=anth_schemas if tool_schemas else None, max_tokens=4096,
                            )
                        else:
                            llm_result = await client.chat_completion(
                                messages=messages, model=cloud_model,
                                tools=tool_schemas if tool_schemas else None, max_tokens=4096,
                            )
                except Exception as e:
                    logger.warning(f"DAG cloud {cloud_provider} failed: {e}")

            # Local fallback
            if llm_result is None and model_name:
                scheduler = get_gpu_scheduler()
                await scheduler.ensure_model(model_name)
                llm_result = await ollama.chat_completion(
                    model=model_name, messages=messages,
                    tools=tool_schemas if tool_schemas else None,
                    keep_alive=settings.model_keep_alive,
                )

            if llm_result is None:
                yield f"§SPIDER:dag:⚠️ {node.label or node.id} failed — no model"
                break

            if llm_result.has_tool_calls:
                messages.append({"role": "assistant", "content": llm_result.text or ""})
                for tc in llm_result.tool_calls:
                    tool = registry.get_tool(tc.name)
                    if tool:
                        yield f"§SPIDER:{node.agent}:🔧 {tc.name}"
                        result = await tool.execute(**tc.arguments)
                        tool_count += 1
                        messages.append({
                            "role": "tool" if cloud_provider != "anthropic" else "user",
                            "content": result.output[:5000],
                            **({"tool_call_id": tc.call_id} if tc.call_id else {}),
                        })
                continue
            else:
                output = llm_result.text or ""
                break

        self._node_outputs[node.id] = output
        self._state[f"node_{node.id}_output"] = output

        yield f"\n\n**{node.label or node.agent}**\n\n"
        yield output

    async def _run_condition(self, node: DAGNode) -> None:
        """Evaluate condition and mark successors accordingly."""
        try:
            result = eval(
                node.condition,
                {"__builtins__": {}},
                {"state": self._state, "outputs": self._node_outputs},
            )
            branch = str(result).lower()
        except Exception as e:
            logger.warning(f"DAG condition eval error: {e}")
            branch = "false"

        self._state[f"_condition_{node.id}"] = branch
        self._node_outputs[node.id] = branch

        # Only allow successors matching the branch to proceed
        for edge in self.dag.get_successors(node.id):
            if edge.condition_value and edge.condition_value.lower() != branch:
                # Skip this branch — mark target as skipped
                self._node_status[edge.target] = "done"
                self._node_outputs[edge.target] = ""

    def _run_merge(self, node: DAGNode) -> None:
        """Merge outputs from all predecessors."""
        preds = self.dag.get_predecessors(node.id)
        merged = []
        for edge in preds:
            output = self._node_outputs.get(edge.source, "")
            if output:
                merged.append(output)
        combined = "\n\n---\n\n".join(merged)
        self._node_outputs[node.id] = combined
        self._state[f"node_{node.id}_output"] = combined

    async def _run_loop(self, node: DAGNode) -> AsyncIterator[str]:
        """Loop: re-execute predecessor subgraph until condition fails."""
        count_key = node.id
        self._loop_counts.setdefault(count_key, 0)

        while self._loop_counts[count_key] < node.max_iterations:
            # Evaluate loop condition
            try:
                should_continue = eval(
                    node.condition,
                    {"__builtins__": {}},
                    {
                        "state": self._state,
                        "outputs": self._node_outputs,
                        "iteration": self._loop_counts[count_key],
                    },
                )
            except Exception:
                should_continue = False

            if not should_continue:
                break

            self._loop_counts[count_key] += 1
            yield f"§SPIDER:dag:🔄 {node.label or node.id} — iteration {self._loop_counts[count_key]}"

            # Re-execute predecessor nodes
            preds = self.dag.get_predecessors(node.id)
            for edge in preds:
                self._node_status[edge.source] = "pending"
                async for event in self._execute_node(edge.source):
                    yield event

        self._node_outputs[node.id] = self._node_outputs.get(
            self.dag.get_predecessors(node.id)[-1].source if self.dag.get_predecessors(node.id) else "",
            "",
        )
        yield f"§SPIDER:dag:🏁 Loop {node.label or node.id} finished after {self._loop_counts[count_key]} iterations"

    async def _run_hitl(self, node: DAGNode) -> AsyncIterator[str]:
        """Pause execution for human input via HITL manager."""
        from agentic_hub.core.hitl import get_hitl_manager, HITLType, HITLRequest

        hitl_mgr = get_hitl_manager()

        # Determine HITL type from metadata
        hitl_type_str = node.metadata.get("hitl_type", "approval").upper()
        try:
            hitl_type = HITLType[hitl_type_str]
        except KeyError:
            hitl_type = HITLType.APPROVAL

        # Resolve prompt template
        prompt = self._resolve_template(node.prompt_template) if node.prompt_template else "Approval required to continue"

        request = HITLRequest(
            request_id=f"{self.dag.name}:{node.id}",
            type=hitl_type,
            prompt=prompt,
            options=node.metadata.get("options", []),
            context=node.metadata.get("context", ""),
            timeout_seconds=node.metadata.get("timeout", 300),
            default_action=node.metadata.get("default_action", "timeout"),
            agent=node.agent or "dag",
            node_id=node.id,
        )

        yield f"§SPIDER:dag:⏸️ {node.label or node.id} — waiting for user input"
        yield f"\n\n**{node.label or 'User Input Required'}**: {prompt}\n\n"

        if request.options:
            for i, opt in enumerate(request.options, 1):
                yield f"{i}. {opt}\n"
            yield "\n"

        response = await hitl_mgr.request_input(request)

        self._node_outputs[node.id] = response.user_input or response.action
        self._state[f"hitl_{node.id}"] = response.action
        self._state[f"hitl_{node.id}_input"] = response.user_input

        yield f"§SPIDER:dag:▶️ User responded: {response.action}"

    def _resolve_template(self, template: str) -> str:
        """Resolve {variable} placeholders in a template."""
        try:
            return template.format(
                user_message=self._state.get("user_message", ""),
                previous_output=self._state.get("previous_output", ""),
                **{k: v for k, v in self._state.items() if isinstance(v, str)},
                **{f"node_{k}_output": v for k, v in self._node_outputs.items()},
            )
        except (KeyError, IndexError):
            # Graceful fallback for missing variables
            import re
            return re.sub(r"\{[^}]+\}", "", template)

    def get_status(self) -> dict:
        """Get execution status snapshot."""
        return {
            "dag": self.dag.name,
            "nodes": {
                nid: {"status": status, "output_length": len(self._node_outputs.get(nid, ""))}
                for nid, status in self._node_status.items()
            },
        }


# ── Pipeline → DAG conversion ──────────────────────────────────────

def pipeline_to_dag(pipeline) -> DAGDefinition:
    """Convert a linear Pipeline to a DAGDefinition."""
    nodes = []
    edges = []
    for i, step in enumerate(pipeline.steps):
        node = DAGNode(
            id=f"step_{i}",
            type=NodeType.AGENT,
            agent=step.agent,
            prompt_template=step.prompt_template,
            tools=step.tools,
            max_tool_rounds=step.max_tool_rounds,
            label=step.label or f"Step {i + 1}: {step.agent}",
        )
        if step.condition:
            node.metadata["original_condition"] = step.condition
        nodes.append(node)
        if i > 0:
            edges.append(DAGEdge(source=f"step_{i - 1}", target=f"step_{i}"))
    return DAGDefinition(name=pipeline.name, nodes=nodes, edges=edges, description=pipeline.description)


# ── Built-in DAG templates ─────────────────────────────────────────

PARALLEL_RESEARCH_DAG = DAGDefinition(
    name="Parallel Research",
    description="Scholar + Oracle + Automator research in parallel → Oracle synthesizes",
    nodes=[
        DAGNode(id="scholar_research", type=NodeType.AGENT, agent="scholar",
                prompt_template="Research this topic using available tools:\n\n{user_message}",
                label="Scholar: Research"),
        DAGNode(id="oracle_analysis", type=NodeType.AGENT, agent="oracle",
                prompt_template="Analyze this topic from a strategic perspective:\n\n{user_message}",
                tools=[], label="Oracle: Analyze"),
        DAGNode(id="automator_check", type=NodeType.AGENT, agent="automator",
                prompt_template="Check system state and gather technical context for:\n\n{user_message}",
                label="Automator: System Check"),
        DAGNode(id="merge", type=NodeType.MERGE, label="Merge All Perspectives"),
        DAGNode(id="synthesize", type=NodeType.AGENT, agent="oracle",
                prompt_template=(
                    "Synthesize these three perspectives into a unified conclusion:\n\n"
                    "{node_merge_output}\n\nOriginal question: {user_message}"
                ),
                tools=[], label="Oracle: Synthesize"),
    ],
    edges=[
        DAGEdge(source="scholar_research", target="merge"),
        DAGEdge(source="oracle_analysis", target="merge"),
        DAGEdge(source="automator_check", target="merge"),
        DAGEdge(source="merge", target="synthesize"),
    ],
)

CONDITIONAL_CODE_DAG = DAGDefinition(
    name="Conditional Code",
    description="Scholar analyzes → condition (simple vs complex) → Code Team or full pipeline",
    nodes=[
        DAGNode(id="analyze", type=NodeType.AGENT, agent="scholar",
                prompt_template=(
                    "Analyze this coding task. Determine if it is 'simple' (one file, "
                    "few lines) or 'complex' (multi-file, architecture changes).\n\n"
                    "End your response with exactly: COMPLEXITY: simple or COMPLEXITY: complex\n\n"
                    "Task: {user_message}"
                ),
                tools=["read_file", "list_dir", "rag_search"], label="Scholar: Analyze"),
        DAGNode(id="check_complexity", type=NodeType.CONDITION,
                condition="'complex' in outputs.get('analyze', '').lower()",
                label="Check Complexity"),
        DAGNode(id="simple_fix", type=NodeType.AGENT, agent="code_team",
                prompt_template="Apply this simple fix:\n\n{node_analyze_output}\n\nTask: {user_message}",
                label="Code Team: Quick Fix"),
        DAGNode(id="full_implement", type=NodeType.AGENT, agent="code_team",
                prompt_template=(
                    "Full implementation needed:\n\n{node_analyze_output}\n\nTask: {user_message}"
                ),
                max_tool_rounds=5, label="Code Team: Full Implement"),
        DAGNode(id="test", type=NodeType.AGENT, agent="automator",
                prompt_template="Test the changes from:\n\n{previous_output}\n\nTask: {user_message}",
                label="Automator: Test"),
    ],
    edges=[
        DAGEdge(source="analyze", target="check_complexity"),
        DAGEdge(source="check_complexity", target="simple_fix", condition_value="false"),
        DAGEdge(source="check_complexity", target="full_implement", condition_value="true"),
        DAGEdge(source="full_implement", target="test"),
    ],
)


# DAG registry
DAGS: dict[str, DAGDefinition] = {
    "parallel_research": PARALLEL_RESEARCH_DAG,
    "conditional_code": CONDITIONAL_CODE_DAG,
}


def get_dag(name: str) -> DAGDefinition | None:
    return DAGS.get(name)


# ── DAG persistence ────────────────────────────────────────────────
import json as _json
from pathlib import Path

_DAG_DIR = Path(__file__).parent.parent.parent.parent / "data" / "workflows"


def save_dag(dag: DAGDefinition) -> Path:
    """Save a DAG definition to data/workflows/."""
    _DAG_DIR.mkdir(parents=True, exist_ok=True)
    path = _DAG_DIR / f"{dag.name.lower().replace(' ', '_')}.json"
    path.write_text(_json.dumps(dag.to_dict(), indent=2))
    return path


def load_saved_dags() -> dict[str, DAGDefinition]:
    """Load all saved DAG definitions."""
    if not _DAG_DIR.exists():
        return {}
    dags = {}
    for f in _DAG_DIR.glob("*.json"):
        try:
            data = _json.loads(f.read_text())
            dag = DAGDefinition.from_dict(data)
            dags[dag.name] = dag
        except Exception as e:
            logger.warning(f"Failed to load DAG {f}: {e}")
    return dags
