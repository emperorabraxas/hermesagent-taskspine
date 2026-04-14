"""Tool registry — central catalog of all tools with per-agent permissions."""
from __future__ import annotations

import logging
from typing import Any

from agentic_hub.core.tools.base import BaseTool

logger = logging.getLogger(__name__)


class ToolRegistry:
    """Singleton registry of tools available to agents.

    Tools are registered with optional agent restrictions. If no agents specified,
    the tool is available to all agents. Agent permissions can also be loaded from
    models.yaml via configure_from_yaml().
    """

    def __init__(self):
        self._tools: dict[str, BaseTool] = {}
        # Tools registered without agents= are unrestricted (available to all).
        self._unrestricted_tools: set[str] = set()
        # agent_name -> set of RESTRICTED tool names explicitly granted to that agent.
        self._agent_permissions: dict[str, set[str]] = {}

    def register(self, tool: BaseTool, agents: list[str] | None = None) -> None:
        """Register a tool. Optionally restrict to specific agents.

        If agents is None, the tool is unrestricted (available to all agents).
        If agents is specified, the tool is ONLY available to those agents,
        but this does NOT affect other agents' access to unrestricted tools.
        """
        self._tools[tool.name] = tool
        logger.info(f"Tool registered: {tool.name}")
        if agents:
            for agent in agents:
                if agent not in self._agent_permissions:
                    self._agent_permissions[agent] = set()
                self._agent_permissions[agent].add(tool.name)
        else:
            self._unrestricted_tools.add(tool.name)

    def get_tool(self, name: str) -> BaseTool | None:
        """Get a tool by name."""
        return self._tools.get(name)

    def get_all_tools(self) -> list[BaseTool]:
        """Get all registered tools."""
        return list(self._tools.values())

    def get_tools_for_agent(
        self, agent_name: str, rbac_allowed: set[str] | None = None
    ) -> list[BaseTool]:
        """Get tools available to a specific agent, respecting permissions.

        Every agent gets ALL unrestricted tools (registered without agents=).
        Agents also get any restricted tools explicitly granted to them.
        This means restricting trading tools to money_maker doesn't remove
        shell/read/write/salesforce access from other agents.

        Args:
            agent_name: The agent requesting tools.
            rbac_allowed: Optional set of tool names allowed by RBAC.
                          None means no RBAC restriction (admin role).
        """
        # All unrestricted tools + any restricted tools granted to this agent
        allowed = set(self._unrestricted_tools)
        if agent_name in self._agent_permissions:
            allowed |= self._agent_permissions[agent_name]
        tools = [t for name, t in self._tools.items() if name in allowed]

        # Apply RBAC filter if present
        if rbac_allowed is not None:
            tools = [t for t in tools if t.name in rbac_allowed]
        return tools

    def get_schemas_for_agent(self, agent_name: str, provider: str = "openai") -> list[dict]:
        """Get JSON schemas for all tools available to an agent.

        Args:
            agent_name: The agent requesting tools.
            provider: 'openai' (default, also works for Ollama/xAI/DeepSeek)
                      or 'anthropic' (Anthropic's tool_use format).
        """
        tools = self.get_tools_for_agent(agent_name)
        if provider == "anthropic":
            return [t.to_anthropic_schema() for t in tools]
        return [t.to_json_schema() for t in tools]

    def configure_from_yaml(self, config: dict) -> None:
        """Load agent→tool permissions from models.yaml config.

        Expected format in models.yaml:
            agents:
              scholar:
                tools: [rag_search, read_file, web_fetch]
              automator:
                tools: [shell, read_file, write_file, list_dir]
        """
        agents_cfg = config.get("agents", {})
        for agent_name, agent_cfg in agents_cfg.items():
            tool_list = agent_cfg.get("tools")
            if tool_list is not None:
                self._agent_permissions[agent_name] = set(tool_list)
                logger.info(f"Agent {agent_name} tools: {tool_list}")

    def __len__(self) -> int:
        return len(self._tools)

    def __repr__(self) -> str:
        return f"<ToolRegistry: {len(self._tools)} tools>"


# --- Singleton ---
_registry: ToolRegistry | None = None


def get_registry() -> ToolRegistry:
    """Get or create the global tool registry."""
    global _registry
    if _registry is None:
        _registry = ToolRegistry()
        _register_builtins(_registry)
    return _registry


def _register_builtins(registry: ToolRegistry) -> None:
    """Register all built-in tools."""
    from agentic_hub.core.tools.builtin import (
        ShellTool, ReadFileTool, WriteFileTool, ListDirectoryTool,
        WebFetchTool, RAGSearchTool, PythonEvalTool, EntitySearchTool,
        EditFileTool, GlobTool, GrepTool, GitTool,
        WebSearchTool, CodeExecTool,
        VisionTool, PDFTool, ThinkDeepTool, StructuredOutputTool,
        ImageGenTool, TTSTool, TranscribeTool, ModerateTool,
        EmbedTool, XSearchTool, CodeFillTool, DBSearchTool, LeaderboardTool,
        HFSearchModelsTool, HFSummarizeTool, HFTranslateTool,
        HFClassifyTool, HFNERTool, HFQATool,
        BatchJobTool, FileManagerTool, FineTuneTool, VectorStoreTool,
        ModelManagerTool, TokenCountTool, ImageEditTool, VideoGenTool,
        ComputerUseTool, FuzzySearchTool, CacheTool, BalanceCheckTool,
        OracleGuardrailsTool, RerankTool, PhoneNotifyTool,
        SalesforceTool, SalesforceKnowledgeTool, SalesforceValidateTool,
        PauseAndAskTool, BatchEditTool, AWSTool,
    )
    # Core tools — full access, all spiders can use everything
    registry.register(ShellTool())
    registry.register(ReadFileTool())
    registry.register(WriteFileTool())
    registry.register(ListDirectoryTool())
    registry.register(WebFetchTool())
    registry.register(RAGSearchTool())
    registry.register(PythonEvalTool())
    registry.register(EntitySearchTool())

    # Dev tools — the Claude Code replacements
    registry.register(EditFileTool())
    registry.register(GlobTool())
    registry.register(GrepTool())
    registry.register(GitTool())
    registry.register(WebSearchTool())
    registry.register(CodeExecTool())

    # Cloud-powered tools — full access, all spiders
    try:
        registry.register(VisionTool())
        registry.register(PDFTool())
        registry.register(ThinkDeepTool())
        registry.register(StructuredOutputTool())
        registry.register(ImageGenTool())
        registry.register(TTSTool())
        registry.register(TranscribeTool())
        registry.register(ModerateTool())
        registry.register(EmbedTool())
        registry.register(XSearchTool())
        registry.register(CodeFillTool())
        registry.register(DBSearchTool())
        registry.register(LeaderboardTool())
    except Exception as e:
        logger.warning(f"Cloud tools registration failed (non-fatal): {e}")

    # Hugging Face Hub tools — full access, all spiders
    try:
        registry.register(HFSearchModelsTool())
        registry.register(HFSummarizeTool())
        registry.register(HFTranslateTool())
        registry.register(HFClassifyTool())
        registry.register(HFNERTool())
        registry.register(HFQATool())
    except Exception as e:
        logger.warning(f"HF tools registration failed (non-fatal): {e}")

    # Admin / management tools — full access, all spiders
    try:
        registry.register(BatchJobTool())
        registry.register(FileManagerTool())
        registry.register(FineTuneTool())
        registry.register(VectorStoreTool())
        registry.register(ModelManagerTool())
        registry.register(TokenCountTool())
        registry.register(ImageEditTool())
        registry.register(VideoGenTool())
        registry.register(ComputerUseTool())
        registry.register(FuzzySearchTool())
        registry.register(CacheTool())
        registry.register(BalanceCheckTool())
    except Exception as e:
        logger.warning(f"Admin tools registration failed (non-fatal): {e}")

    # iPhone / Apple Shortcuts — full access
    try:
        registry.register(PhoneNotifyTool())
    except Exception as e:
        logger.warning(f"Phone notify registration failed (non-fatal): {e}")

    # Oracle Cloud AI tools — full access
    try:
        registry.register(OracleGuardrailsTool())
        registry.register(RerankTool())
    except Exception as e:
        logger.warning(f"Oracle tools registration failed (non-fatal): {e}")

    # Salesforce tools — full access, no agent restrictions (all spiders can use)
    try:
        registry.register(SalesforceTool())       # sf CLI: deploy, retrieve, test, query
        registry.register(SalesforceKnowledgeTool())  # domain knowledge / gotchas
        registry.register(SalesforceValidateTool())   # browser validation / screenshots
    except Exception as e:
        logger.warning(f"Salesforce tools registration failed (non-fatal): {e}")

    # Autonomy tools — all spiders
    try:
        registry.register(PauseAndAskTool())      # stop + phone notify on ambiguity
        registry.register(BatchEditTool())         # multi-file edits in one round
    except Exception as e:
        logger.warning(f"Autonomy tools registration failed (non-fatal): {e}")

    # AWS tools — Secrets Manager, Lambda, S3 for UWM integration infra
    try:
        registry.register(AWSTool())
    except Exception as e:
        logger.warning(f"AWS tool registration failed (non-fatal): {e}")

    # Trading tools — Money Maker only (trade, portfolio access restricted)
    try:
        from agentic_hub.core.trading.tools import TradeTool, QuoteTool, PortfolioTool, RiskStatusTool, HustleTool, StrategyTool, EarnTool
        from agentic_hub.core.trading.plaid_tools import (
            PlaidAccountsTool, PlaidTransactionsTool, PlaidInvestmentsTool,
            PlaidTransferTool, PlaidTransferRecurringTool, PlaidTransferRefundTool,
            PlaidIdentityTool, PlaidIdentityVerificationTool,
            PlaidAssetsTool, PlaidIncomeTool, PlaidSignalTool,
            PlaidLiabilitiesTool, PlaidStatementsTool, PlaidBeaconTool,
            PlaidInstitutionsTool, PlaidItemTool, PlaidLinkTool,
            PlaidSandboxTool, PlaidNetworkTool, PlaidEnrichTool,
            PlaidWebhookTool,
        )
        registry.register(TradeTool(), agents=["money_maker"])
        registry.register(QuoteTool(), agents=["money_maker", "scholar", "oracle"])
        registry.register(PortfolioTool(), agents=["money_maker"])
        registry.register(RiskStatusTool(), agents=["money_maker"])
        registry.register(HustleTool(), agents=["money_maker"])
        registry.register(StrategyTool(), agents=["money_maker"])
        registry.register(EarnTool(), agents=["money_maker"])
        # Plaid: read-only tools → money_maker + scholar
        registry.register(PlaidAccountsTool(), agents=["money_maker", "scholar"])
        registry.register(PlaidTransactionsTool(), agents=["money_maker", "scholar"])
        registry.register(PlaidInvestmentsTool(), agents=["money_maker", "scholar"])
        registry.register(PlaidLiabilitiesTool(), agents=["money_maker", "scholar"])
        registry.register(PlaidStatementsTool(), agents=["money_maker", "scholar"])
        registry.register(PlaidInstitutionsTool(), agents=["money_maker", "scholar"])
        registry.register(PlaidNetworkTool(), agents=["money_maker", "scholar"])
        registry.register(PlaidEnrichTool(), agents=["money_maker", "scholar"])
        # Plaid: mutating tools → money_maker only
        registry.register(PlaidTransferTool(), agents=["money_maker"])
        registry.register(PlaidTransferRecurringTool(), agents=["money_maker"])
        registry.register(PlaidTransferRefundTool(), agents=["money_maker"])
        registry.register(PlaidIdentityTool(), agents=["money_maker"])
        registry.register(PlaidIdentityVerificationTool(), agents=["money_maker"])
        registry.register(PlaidAssetsTool(), agents=["money_maker"])
        registry.register(PlaidIncomeTool(), agents=["money_maker"])
        registry.register(PlaidSignalTool(), agents=["money_maker"])
        registry.register(PlaidBeaconTool(), agents=["money_maker"])
        registry.register(PlaidItemTool(), agents=["money_maker"])
        registry.register(PlaidLinkTool(), agents=["money_maker"])
        registry.register(PlaidSandboxTool(), agents=["money_maker"])
        registry.register(PlaidWebhookTool(), agents=["money_maker"])
    except Exception:
        pass  # Trading dependencies optional

    # Load YAML overrides if available
    try:
        from agentic_hub.config import load_models_config
        config = load_models_config()
        registry.configure_from_yaml(config)
    except Exception:
        pass  # Use defaults if config unavailable
