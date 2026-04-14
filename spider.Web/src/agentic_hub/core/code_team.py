"""Code Team — Lead Engineer and Coder have a real dialogue, then EXECUTE.

They TALK to each other. Think through the problem together.
Plan the approach. Debate tradeoffs. Write the code.
Then the Coder EXECUTES — writes files, deploys, tests, validates.

The user watches the conversation unfold in real-time via spider bubbles
and the chat panel. It's two engineers at a whiteboard, with a terminal.

Works FULLY LOCAL: DeepSeek R1 leads, Qwen codes. No cloud required.
When cloud is available: Opus leads, GPT-5.4 codes. Best of both worlds.
"""
from __future__ import annotations

import logging
from typing import AsyncIterator

from agentic_hub.config import get_settings, load_models_config
from agentic_hub.core.gpu_scheduler import get_gpu_scheduler
from agentic_hub.core.ollama_client import get_ollama
from agentic_hub.core.tools.llm_response import LLMResponse
from agentic_hub.core.tools.registry import get_registry

logger = logging.getLogger(__name__)

LOCAL_CODERS = [
    "huihui_ai/qwen3-coder-abliterated:latest",
    "qwen-fast:latest",
    "deepseek-r1:7b",
]

LOCAL_LEADS = [
    "deepseek-r1:7b", "deepseek-r1:latest",
    "qwen-fast:latest",
]


class CodeTeam:
    """Two engineers talking through a problem together — cloud or local.

    After the lead approves the code, the Coder enters a tool-calling
    execution phase where it can write files, deploy to Salesforce,
    run tests, and validate — all within the same session.
    """

    def __init__(self):
        config = load_models_config()
        ct = config.get("code_team", {})
        self.opus_model = ct.get("opus_model", "claude-opus-4-6-20250819")
        self.codex_model = ct.get("codex_model", "gpt-5.4")
        self.local_coder = ct.get("local_coder", "huihui_ai/qwen3-coder-abliterated")
        self.local_lead = ct.get("local_reviewer", "deepseek-r1:7b")
        self.max_rounds = ct.get("max_rounds", 3)
        orch_cfg = config.get("orchestrator", {})
        self.max_tool_rounds = orch_cfg.get("max_tool_rounds", 10)

    async def _find_local_model(self, candidates: list[str]) -> str:
        """Find the first available model from candidates."""
        ollama = get_ollama()
        available = {m.get("name", "") for m in await ollama.list_models()}
        for m in candidates:
            if m in available:
                return m
        return candidates[-1]  # last resort

    async def _coder_say(self, messages: list[dict], settings) -> tuple[str, str]:
        """Coder speaks — cloud GPT-5.4 or local Qwen. Plain text, no tools."""
        if settings.openai_api_key:
            try:
                from agentic_hub.core.cloud_client import get_openai
                r = await get_openai().chat(messages=messages, model=self.codex_model, max_tokens=4096, temperature=0.5)
                return r, "Codex"
            except Exception as e:
                logger.warning(f"Cloud coder failed: {e}")
        model = await self._find_local_model(LOCAL_CODERS)
        await get_gpu_scheduler().ensure_model(model)
        r = await get_ollama().chat(model=model, messages=messages, stream=False, keep_alive=settings.model_keep_alive)
        return r, model.split(":")[0]

    async def _lead_say(self, messages: list[dict], system: str, settings) -> tuple[str, str]:
        """Lead engineer speaks — cloud Opus or local DeepSeek R1."""
        if settings.anthropic_api_key:
            try:
                from agentic_hub.core.cloud_client import get_anthropic
                r = await get_anthropic().chat(messages=messages, model=self.opus_model, system=system, max_tokens=2048, temperature=0.4)
                return r, "Opus"
            except Exception as e:
                logger.warning(f"Cloud lead (Opus) failed: {e}")
        # Local fallback — DeepSeek R1 as lead engineer
        model = await self._find_local_model(LOCAL_LEADS)
        await get_gpu_scheduler().ensure_model(model)
        lead_messages = [{"role": "system", "content": system}] + messages
        r = await get_ollama().chat(model=model, messages=lead_messages, stream=False, keep_alive=settings.model_keep_alive)
        return r, f"R1 ({model.split(':')[0]})"

    async def _coder_execute(
        self, messages: list[dict], tools: list[dict], settings
    ) -> LLMResponse:
        """Coder with tool-calling — cloud GPT-5.4 or local Qwen. Returns LLMResponse."""
        if settings.openai_api_key:
            try:
                from agentic_hub.core.cloud_client import get_openai
                return await get_openai().chat_completion(
                    messages=messages, model=self.codex_model,
                    tools=tools, max_tokens=4096, temperature=0.3,
                )
            except Exception as e:
                logger.warning(f"Cloud coder (tool-calling) failed: {e}")
        # Local fallback
        model = await self._find_local_model(LOCAL_CODERS)
        await get_gpu_scheduler().ensure_model(model)
        return await get_ollama().chat_completion(
            model=model, messages=messages, tools=tools,
            keep_alive=settings.model_keep_alive,
        )

    async def solve(self, user_message: str, conversation_history: list[dict] | None = None) -> AsyncIterator[str]:
        settings = get_settings()

        # Load domain knowledge for context-aware coding
        domain_ctx = ""
        try:
            from agentic_hub.core.domain_context import get_domain_context
            domain_ctx = "\n\n" + get_domain_context()
        except Exception:
            pass

        # The conversation between the two engineers
        dialogue = []

        # === STEP 1: Lead engineer kicks off the discussion ===
        yield "§SPIDER:reviewer:🤔 Thinking about the approach..."
        yield "**Lead:** "

        lead_system = (
            "You are a senior engineer discussing a coding problem with your partner. "
            "Think out loud. Be direct and conversational — like two people at a whiteboard."
            + domain_ctx
        )
        try:
            lead_opening, lead_name = await self._lead_say([{
                "role": "user",
                "content": f"A user asked: {user_message}\n\nYou're about to discuss this with your coding partner. Start by breaking down the problem — what's the approach? What are the key decisions? Keep it conversational and brief (3-5 sentences). Don't write code yet."
            }], lead_system, settings)

            dialogue.append({"role": "lead", "text": lead_opening, "name": lead_name})
            yield lead_opening
            snippet = lead_opening[:70].replace('\n', ' ')
            yield f"\n\n§SPIDER:reviewer:💬 {lead_name}: \"{snippet}...\""
        except Exception as e:
            logger.warning(f"Lead opening failed: {e}")
            lead_name = "Lead"
            dialogue.append({"role": "lead", "text": "", "name": lead_name})

        # === STEP 2: Coder responds ===
        yield "\n\n§SPIDER:coder:💭 Thinking..."

        coder_prompt = f"The user wants: {user_message}"
        if dialogue and dialogue[-1]["text"]:
            coder_prompt += f"\n\nYour partner ({dialogue[-1]['name']}) said: {dialogue[-1]['text']}\n\nRespond to their points, then write the code. If you disagree with their approach, say why. Keep the discussion part brief, then provide complete code."
        else:
            coder_prompt += "\n\nWrite the complete solution."

        yield "\n\n**Coder:** "
        coder_system = (
            "You are an expert programmer in a pair programming session. "
            "Respond to your partner's thoughts, then write complete code. "
            "Be conversational but get to the code quickly."
            + domain_ctx
        )
        coder_response, coder_name = await self._coder_say([
            {"role": "system", "content": coder_system},
            {"role": "user", "content": coder_prompt},
        ], settings)

        dialogue.append({"role": "coder", "text": coder_response, "name": coder_name})
        yield coder_response
        snippet = coder_response[:70].replace('\n', ' ')
        yield f"\n\n§SPIDER:coder:💬 {coder_name}: \"{snippet}...\""

        # === STEP 3: Lead reviews — ALWAYS happens (cloud or local) ===
        yield f"\n\n§SPIDER:reviewer:🔍 {lead_name} reviewing..."
        yield f"\n\n**{lead_name}:** "

        try:
            lead_review, _ = await self._lead_say([{
                "role": "user",
                "content": (
                    f"User asked: {user_message}\n\n"
                    f"You said: {dialogue[0]['text']}\n\n"
                    f"{coder_name} responded with: {coder_response}\n\n"
                    "Continue the conversation. Did they address your points? "
                    "Is the code correct? What would you change? "
                    "If it's good, say so and present the final clean version to the user. "
                    "If it needs changes, be specific about what to fix."
                ),
            }], "You are a senior engineer reviewing your partner's code in a pair programming session. Be direct and honest. If the code is good, present it cleanly. If not, say exactly what's wrong.", settings)

            dialogue.append({"role": "lead", "text": lead_review, "name": lead_name})
            yield lead_review
            snippet = lead_review[:70].replace('\n', ' ')
            yield f"\n\n§SPIDER:reviewer:💬 {lead_name}: \"{snippet}...\""

            # If lead isn't satisfied, revision rounds (up to max_rounds)
            rounds = 0
            while rounds < self.max_rounds - 1:
                if "APPROVED" in lead_review[:100]:
                    break
                if not any(w in lead_review.lower() for w in ["fix", "change", "wrong", "bug", "issue", "missing", "should"]):
                    break

                rounds += 1
                yield f"\n\n§SPIDER:coder:🔧 Addressing feedback (round {rounds + 1})..."
                yield f"\n\n**{coder_name}:** "

                final_code, _ = await self._coder_say([
                    {"role": "system", "content": "You are pair programming. Your partner found issues. Fix them ALL. Show the complete corrected code."},
                    {"role": "user", "content": user_message},
                    {"role": "assistant", "content": coder_response},
                    {"role": "user", "content": f"Partner's feedback:\n{lead_review}\n\nAddress every point. Show the fixed code."},
                ], settings)

                dialogue.append({"role": "coder", "text": final_code, "name": coder_name})
                yield final_code
                yield f"\n\n§SPIDER:coder:✅ Revised"

                # Lead reviews the revision
                yield f"\n\n§SPIDER:reviewer:✅ {lead_name} reviewing revision..."
                yield f"\n\n**{lead_name}:** "
                try:
                    lead_review, _ = await self._lead_say([{
                        "role": "user",
                        "content": f"Revised version:\n{final_code}\n\nQuick sign-off — is this good to ship? If not, what still needs fixing? 2-3 sentences max.",
                    }], "Give a brief verdict. Be concise. If the code is correct say APPROVED.", settings)
                    yield lead_review
                    yield f"\n\n§SPIDER:reviewer:✅ {lead_name} done"
                except Exception:
                    yield "Looks good. Ship it."
                    break

                coder_response = final_code

            # Emit revision round count for achievement tracking
            yield f"§META:code_team_rounds:{rounds}"

        except Exception as e:
            logger.warning(f"Lead review failed: {e}")
            yield f"\n\n*{lead_name} couldn't review — here's the code as-is.*"

        # === STEP 4: EXECUTE — Coder gets tools to ship the approved code ===
        # This is the key difference: after dialogue, the Coder can now
        # write files, deploy, test, and validate using the full tool registry.
        approved_code = dialogue[-1]["text"] if dialogue else coder_response
        async for chunk in self._execute_phase(
            user_message, approved_code, domain_ctx, settings
        ):
            yield chunk

    async def _execute_phase(
        self,
        user_message: str,
        approved_code: str,
        domain_ctx: str,
        settings,
    ) -> AsyncIterator[str]:
        """Step 4: Coder executes the approved plan with tool access.

        Enters a tool-calling loop where the Coder can write files,
        deploy to Salesforce, run tests, take screenshots, and fix errors.
        """
        registry = get_registry()
        tool_schemas = registry.get_schemas_for_agent("code_team")

        if not tool_schemas:
            return

        yield "\n\n---\n"
        yield "§SPIDER:coder:🚀 Executing approved code..."
        yield "\n\n**Executing:**\n"

        exec_system = (
            "You are a developer executing an approved code plan. You have tools available "
            "to write files, edit files, deploy to Salesforce, run tests, and validate UI. "
            "Execute the plan step by step:\n"
            "1. Write/edit the code files using write_file, edit_file, or batch_edit\n"
            "2. If this is Salesforce work, use the salesforce tool to deploy\n"
            "3. Run tests with the salesforce tool (action: test)\n"
            "4. If deploy fails, read the errors, fix the code, and redeploy\n"
            "5. For LWC changes, use sf_validate to screenshot the result\n"
            "6. If you're unsure about a decision, use pause_and_ask\n\n"
            "DO NOT just output code as text. USE THE TOOLS to actually write files and deploy.\n"
            "Only stop when the entire plan is fully executed. When (and only when) everything is done, "
            "end your final message with the exact marker: EXECUTION_COMPLETE\n"
            "If you are not done yet, continue calling tools. Do not end early with a summary.\n"
            "If the code doesn't need to be deployed (e.g., it's a script or config), "
            "just write it to the correct file."
            + domain_ctx
        )

        messages = [
            {"role": "system", "content": exec_system},
            {"role": "user", "content": (
                f"Original request: {user_message}\n\n"
                f"Approved code from pair programming session:\n\n{approved_code[:8000]}\n\n"
                "Now execute this: write the files, deploy if needed, run tests, validate. "
                "Use the tools — don't just repeat the code as text."
            )},
        ]

        def _execution_complete(text: str | None) -> bool:
            return bool(text) and "EXECUTION_COMPLETE" in text.upper()

        tool_round = 0
        while tool_round < self.max_tool_rounds:
            yield f"§SPIDER:coder:🔧 Tool round {tool_round + 1}..."

            llm_result = await self._coder_execute(messages, tool_schemas, settings)

            # Add assistant response to conversation (even if it made no tool calls).
            messages.append({"role": "assistant", "content": llm_result.text or ""})

            if not llm_result.has_tool_calls:
                # Some models will stop "early" with a partial summary. Keep looping unless the model
                # explicitly signals completion.
                if llm_result.text:
                    yield llm_result.text

                if _execution_complete(llm_result.text):
                    break

                # Nudge: continue execution with tools until completion.
                messages.append({
                    "role": "user",
                    "content": (
                        "You are not done yet. Continue executing the plan using tools. "
                        "Only respond without tool calls when finished, and end with EXECUTION_COMPLETE."
                    ),
                })
                tool_round += 1
                yield f"§META:exec_count:{tool_round}"
                continue

            # Execute each tool call
            for tc in llm_result.tool_calls:
                tool = registry.get_tool(tc.name)
                if not tool:
                    yield f"\n⚠️ Unknown tool: {tc.name}\n"
                    messages.append({
                        "role": "tool",
                        "content": f"Error: tool '{tc.name}' not found",
                        **({"tool_call_id": tc.call_id} if tc.call_id else {}),
                    })
                    continue

                args_summary = ', '.join(f'{k}={repr(v)[:40]}' for k, v in tc.arguments.items())
                yield f"\n`{tc.name}({args_summary})`\n"
                yield f"§EXEC:start:code_team:{tc.name}"

                result = await tool.execute(**tc.arguments)

                if result.success:
                    yield f"§EXEC:done:code_team:✅ {tc.name}"
                    yield f"  ✅ {result.output[:200]}\n"
                else:
                    yield f"§EXEC:error:code_team:{result.error or 'failed'}"
                    yield f"  ❌ {result.error or result.output[:200]}\n"

                # Feed result back to LLM
                messages.append({
                    "role": "tool",
                    "content": result.output[:5000],
                    **({"tool_call_id": tc.call_id} if tc.call_id else {}),
                })

            tool_round += 1
            yield f"§META:exec_count:{tool_round}"

        if tool_round >= self.max_tool_rounds:
            yield f"\n⚠️ Reached max tool rounds ({self.max_tool_rounds}). Some work may be incomplete.\n"

        yield "\n§SPIDER:coder:✅ Execution complete"
        yield f"§META:code_team_tool_rounds:{tool_round}"
