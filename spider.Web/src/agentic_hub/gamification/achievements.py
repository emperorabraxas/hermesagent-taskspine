"""Achievement system — badge definitions, unlock checks."""
from __future__ import annotations

import logging
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from agentic_hub.models.gamification import Achievement, XPEvent, Streak

logger = logging.getLogger(__name__)

DATA_DIR = Path(__file__).parent.parent.parent.parent / "data"


@dataclass
class AchievementDef:
    key: str
    name: str
    description: str
    icon: str  # Emoji for CLI, replaced with proper icons in web UI


# All achievement definitions
ACHIEVEMENTS: dict[str, AchievementDef] = {
    # First actions
    "first_chat": AchievementDef("first_chat", "First Contact", "Send your first message", "💬"),
    "first_code": AchievementDef("first_code", "Hello World", "Generate your first code with Code Team", "💻"),
    "first_research": AchievementDef("first_research", "Knowledge Seeker", "Complete your first research query", "🔍"),
    "first_automation": AchievementDef("first_automation", "Automaton", "Run your first automation task", "⚙️"),
    "all_agents": AchievementDef("all_agents", "Web Complete", "Use all 4 agents at least once", "🕸️"),

    # Streaks
    "streak_3": AchievementDef("streak_3", "Getting Sticky", "3-day usage streak", "🔥"),
    "streak_7": AchievementDef("streak_7", "Weekly Web", "7-day usage streak", "🕷️"),
    "streak_30": AchievementDef("streak_30", "Month of Silk", "30-day usage streak", "👑"),

    # Levels
    "level_5": AchievementDef("level_5", "Thread Spinner", "Reach level 5", "🧵"),
    "level_10": AchievementDef("level_10", "Web Weaver", "Reach level 10", "🕸️"),
    "level_25": AchievementDef("level_25", "Silk Master", "Reach level 25", "✨"),
    "level_50": AchievementDef("level_50", "Arachnid Lord", "Reach level 50", "🏆"),

    # Privacy
    "privacy_champion": AchievementDef("privacy_champion", "Privacy Champion", "100 local-only interactions", "🔒"),
    "local_500": AchievementDef("local_500", "Off the Grid", "500 local-only interactions", "🛡️"),

    # Volume
    "messages_100": AchievementDef("messages_100", "Conversationalist", "Send 100 messages", "📝"),
    "messages_1000": AchievementDef("messages_1000", "Chatterbox", "Send 1000 messages", "📚"),

    # Time
    "night_owl": AchievementDef("night_owl", "Night Owl", "Use the system after midnight", "🦉"),
    "early_bird": AchievementDef("early_bird", "Early Bird", "Use the system before 6 AM", "🐦"),

    # === SET A: Operational / Productivity ===
    # Throughput
    "tasks_100": AchievementDef("tasks_100", "System Adopted", "Complete 100 tasks", "🏗️"),
    "tasks_1000": AchievementDef("tasks_1000", "Power User", "Complete 1,000 tasks", "💪"),
    "batch_commander": AchievementDef("batch_commander", "Batch Commander", "Complete a council session (all spiders debate)", "🎖️"),

    # Reliability
    "zero_failure_25": AchievementDef("zero_failure_25", "Zero Failure Run", "25 consecutive tasks with no errors", "✨"),
    "self_healing": AchievementDef("self_healing", "Self-Healing", "Validation gate retry succeeds (R1 reject → revise → approve)", "🩹"),
    "retry_architect": AchievementDef("retry_architect", "Retry Architect", "R1 rejects, agent revises, R1 approves", "🔄"),

    # Automation
    "hands_free": AchievementDef("hands_free", "Hands-Free Operator", "Idle daemon completes a research cycle without user", "🤖"),
    "cron_overlord": AchievementDef("cron_overlord", "Cron Overlord", "Market daemon running for 24+ hours straight", "⏰"),
    "full_autopilot": AchievementDef("full_autopilot", "Full Autopilot", "/improve generates + validates + executes code without input", "✈️"),

    # Debugging
    "first_fix": AchievementDef("first_fix", "First Fix", "Resolve an agent failure (command error → re-run succeeds)", "🩹"),

    # Money Maker
    "money_first": AchievementDef("money_first", "First Trade", "Log your first trade via Money Maker", "💰"),

    # Speed
    "sub_second": AchievementDef("sub_second", "Sub-Second Thinker", "Task completes in under 1 second", "⚡"),

    # === SET B: Advanced / Multi-Agent Intelligence ===

    # Coordination & Architecture
    "swarm_initiated": AchievementDef("swarm_initiated", "Swarm Initiated", "Run 3+ agents collaboratively", "🐝"),
    "hierarchy_builder": AchievementDef("hierarchy_builder", "Hierarchy Builder", "Code Team Lead→Coder manager-worker pattern used", "📊"),
    "specialist_network": AchievementDef("specialist_network", "Specialist Network", "Used all 5 agent types", "🕸️"),
    "consensus_engine": AchievementDef("consensus_engine", "Consensus Engine", "3+ council sessions completed", "🗳️"),
    "delegation_master": AchievementDef("delegation_master", "Delegation Master", "/improve — spiders self-delegate work", "📋"),

    # Reasoning & Planning
    "planner_activated": AchievementDef("planner_activated", "Planner Activated", "3+ Code Team sessions", "📐"),
    "recursive_thinker": AchievementDef("recursive_thinker", "Recursive Thinker", "Code Team ran 2+ revision rounds", "🔄"),
    "tree_explorer": AchievementDef("tree_explorer", "Tree Explorer", "Used both council AND code_team", "🌳"),
    "strategy_optimizer": AchievementDef("strategy_optimizer", "Strategy Optimizer", "R1 rejected then approved — plan improved", "📈"),

    # Memory & Context
    "memory_keeper": AchievementDef("memory_keeper", "Memory Keeper", "20+ messages in a single conversation", "🧠"),
    "long_term_recall": AchievementDef("long_term_recall", "Long-Term Recall", "10+ RAG-augmented interactions", "📖"),
    "context_architect": AchievementDef("context_architect", "Context Architect", "Mastered context — 5000+ XP and 5+ RAG queries", "🏗️"),
    "knowledge_weaver": AchievementDef("knowledge_weaver", "Knowledge Weaver", "RAG + idle research merged in one response", "🧶"),

    # Autonomy
    "goal_setter": AchievementDef("goal_setter", "Goal Setter", "Idle daemon completed a research cycle", "🎯"),
    "self_improver": AchievementDef("self_improver", "Self-Improver", "/improve — agent modified spider.Web's own code", "🔧"),
    "drift_corrector": AchievementDef("drift_corrector", "Drift Corrector", "R1 detected and rejected a bad response", "🧭"),
    "autonomous_loop": AchievementDef("autonomous_loop", "Autonomous Loop", "Code Team ran max revision rounds (3)", "♻️"),

    # Tooling & Execution
    "toolchain_master": AchievementDef("toolchain_master", "Toolchain Master", "5+ tool capabilities in one interaction", "🔗"),
    "code_executor": AchievementDef("code_executor", "Code Executor", "Generated code + sandbox executed it successfully", "▶️"),
    "sandbox_operator": AchievementDef("sandbox_operator", "Sandbox Operator", "10+ sandbox command executions", "📦"),
    "file_system_agent": AchievementDef("file_system_agent", "File System Agent", "Read + write files in one session", "📁"),

    # Observability & Control
    "full_trace_visibility": AchievementDef("full_trace_visibility", "Full Trace Visibility", "Viewed full council output — all spider chains visible", "🔍"),
    "state_inspector": AchievementDef("state_inspector", "State Inspector", "R1 validation gate ran — saw intermediate reasoning", "🔬"),
    "intervention_expert": AchievementDef("intervention_expert", "Intervention Expert", "Privileged command required user approval", "🛑"),
    "deterministic_mode": AchievementDef("deterministic_mode", "Deterministic Mode", "50+ local-only interactions + level 10", "🎲"),

    # Security / Safety
    "guardrail_builder": AchievementDef("guardrail_builder", "Guardrail Builder", "5+ R1 validation passes", "🛡️"),
    "prompt_defender": AchievementDef("prompt_defender", "Prompt Defender", "Sandbox blocklist caught a dangerous command", "⚔️"),
    "secret_keeper": AchievementDef("secret_keeper", "Secret Keeper", "100+ local-only interactions — data kept local", "🔐"),
    "boundary_enforcer": AchievementDef("boundary_enforcer", "Boundary Enforcer", "3+ commands blocked by sandbox security", "🚧"),

    # Gemini 3.1 Pro Suggestions (Spider Consultation — April 2026)
    "regex_wrangler": AchievementDef("regex_wrangler", "Regex Wrangler", "Extract and execute 50 bash blocks in the sandbox", "🧶"),
    "ghost_in_shell": AchievementDef("ghost_in_shell", "Ghost in the Shell", "Reach a 5x combo multiplier with rapid-fire requests", "👻"),
    "wolf_of_wall_street": AchievementDef("wolf_of_wall_street", "Wolf of Wall Street", "Money Maker daemon runs uninterrupted for 24 hours", "🐺"),
    "librarian": AchievementDef("librarian", "Librarian", "Max out the 50-message memory cap in a single session", "📖"),

    # Revenue-Linked Progression (Inspo Integration — @androoooooooo8)
    "first_dollar": AchievementDef("first_dollar", "First Dollar", "Money Maker earned his first dollar", "💵"),
    "ten_bucks": AchievementDef("ten_bucks", "Ten Bucks", "Money Maker earned $10", "💰"),
    "fifty_earned": AchievementDef("fifty_earned", "Half a Hundred", "Money Maker earned $50", "💰"),
    "hundred_club": AchievementDef("hundred_club", "Hundred Club", "Money Maker earned $100", "🤑"),
    "series_65_funded": AchievementDef("series_65_funded", "Series 65 Funded", "$600 earned — licensing goal reached", "🏆"),
    "first_trade": AchievementDef("first_trade", "First Trade", "Money Maker executed his first trade", "📊"),
    "strategy_deployed": AchievementDef("strategy_deployed", "Strategy Deployed", "First autonomous strategy running", "⚡"),
    "factory_online": AchievementDef("factory_online", "Factory Online", "All systems go — agents, trading, strategies", "🏭"),
}


class AchievementChecker:
    """Checks and unlocks achievements after each interaction."""

    def _unlock(self, session: AsyncSession, user_id: int, key: str,
                unlocked: set, newly_unlocked: list):
        """Helper: unlock an achievement if not already unlocked."""
        if key not in unlocked and key in ACHIEVEMENTS:
            session.add(Achievement(user_id=user_id, achievement_key=key))
            newly_unlocked.append(ACHIEVEMENTS[key])
            unlocked.add(key)
            logger.info(f"Achievement unlocked: {key}")

    async def check_and_unlock(
        self,
        session: AsyncSession,
        agent: str,
        source: str,
        total_xp: int,
        level: int,
        current_streak: int,
        hour: int,
        user_id: int = 1,
        context: dict[str, Any] | None = None,
    ) -> list[AchievementDef]:
        """Check all achievement conditions, unlock any new ones. Returns newly unlocked."""
        ctx = context or {}

        # Get already-unlocked achievements
        result = await session.execute(
            select(Achievement.achievement_key).where(Achievement.user_id == user_id)
        )
        unlocked = {row[0] for row in result.all()}
        newly_unlocked: list[AchievementDef] = []

        # --- SET A: Simple boolean checks (no DB queries) ---
        checks = [
            # First actions
            ("first_chat", agent in ("oracle", "scholar", "automator", "code_team")),
            ("first_code", agent == "code_team"),
            ("first_research", agent == "scholar"),
            ("first_automation", agent == "automator"),
            # Streaks
            ("streak_3", current_streak >= 3),
            ("streak_7", current_streak >= 7),
            ("streak_30", current_streak >= 30),
            # Levels
            ("level_5", level >= 5),
            ("level_10", level >= 10),
            ("level_25", level >= 25),
            ("level_50", level >= 50),
            # Time
            ("night_owl", 0 <= hour < 4),
            ("early_bird", 4 <= hour < 6),
            # Set A operational (context-based)
            ("batch_commander", source == "council"),
            ("self_healing", ctx.get("r1_approved_after_reject", False)),
            ("full_autopilot", ctx.get("improve_used", False) and ctx.get("code_generated", False) and ctx.get("exec_all_success", False)),
            ("first_fix", ctx.get("had_failure_then_success", False)),
            ("sub_second", ctx.get("latency_ms", 9999) < 1000),

            # --- SET B: Context-based (no DB queries) ---
            # Coordination & Architecture
            ("swarm_initiated", source == "council" or ctx.get("council_spiders", 0) >= 3),
            ("hierarchy_builder", agent == "code_team" and ctx.get("code_team_rounds", -1) >= 0),
            ("delegation_master", ctx.get("improve_used", False)),
            # Reasoning & Planning
            ("recursive_thinker", ctx.get("code_team_rounds", 0) >= 2),
            ("strategy_optimizer", ctx.get("r1_approved_after_reject", False)),
            # Memory & Context
            ("memory_keeper", ctx.get("memory_messages", 0) >= 20),
            ("knowledge_weaver", ctx.get("rag_chunks", 0) > 0 and ctx.get("idle_context", False)),
            # Autonomy
            ("drift_corrector", ctx.get("r1_rejected", False)),
            ("autonomous_loop", ctx.get("code_team_rounds", 0) >= 3),
            # Tooling & Execution
            ("code_executor", ctx.get("code_generated", False) and ctx.get("exec_all_success", False)),
            ("file_system_agent", ctx.get("file_read", False) and ctx.get("sandbox_used", False)),
            # Observability & Control
            ("state_inspector", ctx.get("r1_validated", False)),
            ("intervention_expert", ctx.get("approval_required", False)),
            # Security / Safety
            ("prompt_defender", ctx.get("sandbox_blocked", False)),
            # Gemini 3.1 Pro suggestions
            ("ghost_in_shell", ctx.get("combo_multiplier", 0) >= 5.0),
            ("librarian", ctx.get("memory_messages", 0) >= 50),
        ]

        for key, condition in checks:
            if condition:
                self._unlock(session, user_id, key, unlocked, newly_unlocked)

        # --- Toolchain master: needs list check ---
        if "toolchain_master" not in unlocked:
            tools = set()
            if ctx.get("rag_chunks"):
                tools.add("rag")
            if ctx.get("idle_context"):
                tools.add("idle")
            if ctx.get("sandbox_used") or ctx.get("exec_count", 0) > 0:
                tools.add("sandbox")
            if ctx.get("r1_validated"):
                tools.add("r1")
            if ctx.get("code_generated"):
                tools.add("codegen")
            if ctx.get("file_read"):
                tools.add("fileread")
            if ctx.get("approval_required"):
                tools.add("approval")
            if ctx.get("code_team_rounds") is not None and ctx.get("code_team_rounds", -1) >= 0:
                tools.add("code_team")
            if source == "council":
                tools.add("council")
            if agent in ("scholar", "oracle", "automator"):
                tools.add("agent")
            if len(tools) >= 5:
                self._unlock(session, user_id, "toolchain_master", unlocked, newly_unlocked)

        # --- DB query batch: counts we need for multiple achievements ---
        # Only query if there are unchecked DB-dependent achievements
        db_achievements = {
            "all_agents", "specialist_network", "privacy_champion", "local_500",
            "messages_100", "messages_1000", "tasks_100", "tasks_1000",
            "consensus_engine", "planner_activated", "long_term_recall",
            "self_improver", "full_trace_visibility", "context_architect",
            "deterministic_mode", "guardrail_builder", "secret_keeper",
            "boundary_enforcer", "tree_explorer", "sandbox_operator",
            "zero_failure_25", "retry_architect",
        }
        pending_db = db_achievements - unlocked
        if not pending_db:
            # All DB-dependent achievements already unlocked — skip queries
            pass
        else:
            # --- Query 1: Distinct agent count ---
            if {"all_agents", "specialist_network"} & pending_db:
                agent_count_result = await session.execute(
                    select(func.count(func.distinct(XPEvent.agent)))
                    .where(XPEvent.user_id == user_id)
                )
                distinct_agents = agent_count_result.scalar() or 0
                if distinct_agents >= 4:
                    self._unlock(session, user_id, "all_agents", unlocked, newly_unlocked)
                if distinct_agents >= 5:
                    self._unlock(session, user_id, "specialist_network", unlocked, newly_unlocked)

            # --- Query 2: Local source count (privacy + deterministic + secret_keeper) ---
            if {"privacy_champion", "local_500", "deterministic_mode", "secret_keeper"} & pending_db:
                local_count_result = await session.execute(
                    select(func.count(XPEvent.id))
                    .where(XPEvent.user_id == user_id)
                    .where(XPEvent.source == "local")
                )
                local_count = local_count_result.scalar() or 0
                if local_count >= 100:
                    self._unlock(session, user_id, "privacy_champion", unlocked, newly_unlocked)
                if local_count >= 500:
                    self._unlock(session, user_id, "local_500", unlocked, newly_unlocked)
                if local_count >= 50 and level >= 10:
                    self._unlock(session, user_id, "deterministic_mode", unlocked, newly_unlocked)
                if local_count >= 100:
                    self._unlock(session, user_id, "secret_keeper", unlocked, newly_unlocked)

            # --- Query 3: Total message count ---
            if {"messages_100", "messages_1000", "tasks_100", "tasks_1000"} & pending_db:
                msg_count_result = await session.execute(
                    select(func.count(XPEvent.id)).where(XPEvent.user_id == user_id)
                )
                msg_count = msg_count_result.scalar() or 0
                if msg_count >= 100:
                    self._unlock(session, user_id, "messages_100", unlocked, newly_unlocked)
                    self._unlock(session, user_id, "tasks_100", unlocked, newly_unlocked)
                if msg_count >= 1000:
                    self._unlock(session, user_id, "messages_1000", unlocked, newly_unlocked)
                    self._unlock(session, user_id, "tasks_1000", unlocked, newly_unlocked)

            # --- Query 4: Council source count ---
            if {"consensus_engine", "full_trace_visibility", "tree_explorer"} & pending_db:
                council_count_result = await session.execute(
                    select(func.count(XPEvent.id))
                    .where(XPEvent.user_id == user_id)
                    .where(XPEvent.source == "council")
                )
                council_count = council_count_result.scalar() or 0
                if council_count >= 1:
                    self._unlock(session, user_id, "full_trace_visibility", unlocked, newly_unlocked)
                if council_count >= 3:
                    self._unlock(session, user_id, "consensus_engine", unlocked, newly_unlocked)

            # --- Query 5: Code team agent count ---
            if {"planner_activated", "tree_explorer"} & pending_db:
                ct_count_result = await session.execute(
                    select(func.count(XPEvent.id))
                    .where(XPEvent.user_id == user_id)
                    .where(XPEvent.agent == "code_team")
                )
                ct_count = ct_count_result.scalar() or 0
                if ct_count >= 3:
                    self._unlock(session, user_id, "planner_activated", unlocked, newly_unlocked)

            # --- Tree explorer: needs both council + code_team ---
            if "tree_explorer" not in unlocked:
                has_council = "full_trace_visibility" in unlocked  # already proved council
                has_ct = "planner_activated" in unlocked or agent == "code_team"
                if not has_council:
                    c = await session.execute(
                        select(func.count(XPEvent.id))
                        .where(XPEvent.user_id == user_id)
                        .where(XPEvent.source == "council")
                    )
                    has_council = (c.scalar() or 0) >= 1
                if not has_ct:
                    c = await session.execute(
                        select(func.count(XPEvent.id))
                        .where(XPEvent.user_id == user_id)
                        .where(XPEvent.agent == "code_team")
                    )
                    has_ct = (c.scalar() or 0) >= 1
                if has_council and has_ct:
                    self._unlock(session, user_id, "tree_explorer", unlocked, newly_unlocked)

            # --- Query 6: Reason-based counts (single grouped query) ---
            reason_dependent = {"long_term_recall", "context_architect", "self_improver",
                "guardrail_builder", "boundary_enforcer", "sandbox_operator", "retry_architect",
                "regex_wrangler"}
            if reason_dependent & pending_db:
                tracked_reasons = ("rag_query", "improve_task", "r1_validated", "sandbox_blocked", "sandbox_exec")
                reason_rows = await session.execute(
                    select(XPEvent.reason, func.count(XPEvent.id))
                    .where(XPEvent.user_id == user_id)
                    .where(XPEvent.reason.in_(tracked_reasons))
                    .group_by(XPEvent.reason)
                )
                reason_counts = {row[0]: row[1] for row in reason_rows.all()}

                rag_count = reason_counts.get("rag_query", 0)
                if rag_count >= 10:
                    self._unlock(session, user_id, "long_term_recall", unlocked, newly_unlocked)
                if total_xp >= 5000 and rag_count >= 5:
                    self._unlock(session, user_id, "context_architect", unlocked, newly_unlocked)
                if reason_counts.get("improve_task", 0) >= 1:
                    self._unlock(session, user_id, "self_improver", unlocked, newly_unlocked)
                if reason_counts.get("r1_validated", 0) >= 5:
                    self._unlock(session, user_id, "guardrail_builder", unlocked, newly_unlocked)
                if reason_counts.get("r1_validated", 0) >= 3:
                    self._unlock(session, user_id, "retry_architect", unlocked, newly_unlocked)
                if reason_counts.get("sandbox_blocked", 0) >= 3:
                    self._unlock(session, user_id, "boundary_enforcer", unlocked, newly_unlocked)
                if reason_counts.get("sandbox_exec", 0) >= 10:
                    self._unlock(session, user_id, "sandbox_operator", unlocked, newly_unlocked)
                if reason_counts.get("sandbox_exec", 0) >= 50:
                    self._unlock(session, user_id, "regex_wrangler", unlocked, newly_unlocked)

            # --- Zero failure run: last 25 events have no error reasons ---
            if "zero_failure_25" not in unlocked:
                try:
                    last_25 = await session.execute(
                        select(XPEvent.reason)
                        .where(XPEvent.user_id == user_id)
                        .order_by(XPEvent.id.desc())
                        .limit(25)
                    )
                    reasons = [row[0] for row in last_25.all()]
                    if len(reasons) >= 25 and not any("fail" in r or "error" in r for r in reasons):
                        self._unlock(session, user_id, "zero_failure_25", unlocked, newly_unlocked)
                except Exception:
                    pass

        # --- Money Maker — first trade (portfolio check) ---
        if "money_first" not in unlocked and agent == "money_maker":
            try:
                from agentic_hub.core.portfolio import load_portfolio
                p = load_portfolio()
                if p.get("stats", {}).get("trades_count", 0) > 0:
                    self._unlock(session, user_id, "money_first", unlocked, newly_unlocked)
            except Exception:
                pass

        # --- File-check achievements (no DB needed) ---

        # Goal setter + Hands free: idle research completed
        if "goal_setter" not in unlocked or "hands_free" not in unlocked:
            idle_file = DATA_DIR / "idle_research" / "scholar_latest.json"
            if idle_file.exists():
                try:
                    import json, time
                    data = json.loads(idle_file.read_text())
                    ts = data.get("timestamp", "")
                    if ts:
                        from datetime import datetime as dt
                        file_time = dt.fromisoformat(ts)
                        age_hours = (dt.now() - file_time).total_seconds() / 3600
                        if age_hours < 24:
                            self._unlock(session, user_id, "goal_setter", unlocked, newly_unlocked)
                            self._unlock(session, user_id, "hands_free", unlocked, newly_unlocked)
                except Exception:
                    pass

        # Cron overlord: market daemon uptime >= 24h
        if "cron_overlord" not in unlocked or "wolf_of_wall_street" not in unlocked:
            try:
                from agentic_hub.core.market_daemon import get_daemon_uptime_hours
                uptime = get_daemon_uptime_hours()
                if uptime >= 24:
                    self._unlock(session, user_id, "cron_overlord", unlocked, newly_unlocked)
                    self._unlock(session, user_id, "wolf_of_wall_street", unlocked, newly_unlocked)
            except Exception:
                pass

        return newly_unlocked

    async def get_all_achievements(
        self, session: AsyncSession, user_id: int = 1
    ) -> list[dict]:
        """Get all achievements with unlock status."""
        result = await session.execute(
            select(Achievement.achievement_key, Achievement.unlocked_at)
            .where(Achievement.user_id == user_id)
        )
        unlocked = {row[0]: row[1] for row in result.all()}

        return [
            {
                "key": defn.key,
                "name": defn.name,
                "description": defn.description,
                "icon": defn.icon,
                "unlocked": defn.key in unlocked,
                "unlocked_at": str(unlocked[defn.key]) if defn.key in unlocked else None,
            }
            for defn in ACHIEVEMENTS.values()
        ]
