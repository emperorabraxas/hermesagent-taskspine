"""Money Maker — Isolated financial intelligence operator.

Works ALONE. No council. No team communication.
Has private research sub-spiders (Markets + Gambling) that feed it intel.
All local models — no cloud APIs required.

The user talks directly to Money Maker.
Money Maker coordinates its own research internally, then responds.
"""
from __future__ import annotations

import asyncio
import logging
from typing import AsyncIterator

from agentic_hub.config import get_settings, load_models_config
from agentic_hub.core.gpu_scheduler import get_gpu_scheduler
from agentic_hub.core.ollama_client import get_ollama

logger = logging.getLogger(__name__)


class MoneyMaker:
    """Solo financial intelligence operator with private research spiders."""

    def __init__(self):
        config = load_models_config()
        mm = config.get("money_maker", {})
        self.model = mm.get("model", "deepseek-r1:7b")
        self.system_prompt = mm.get("system_prompt", "")
        self.xp_base = mm.get("xp_base", 15)

        # Private research sub-spiders
        research = mm.get("research_spiders", {})
        self.markets_model = research.get("markets", {}).get("model", "qwen-fast")
        self.markets_focus = research.get("markets", {}).get("focus", "")
        self.gambling_model = research.get("gambling", {}).get("model", "qwen-fast")
        self.gambling_focus = research.get("gambling", {}).get("focus", "")

    def _classify_topic(self, message: str) -> str:
        """Determine which research spider(s) to consult."""
        msg = message.lower()

        gambling_keywords = [
            "fantasy", "dfs", "lineup", "sportsbook", "betting", "odds",
            "parlay", "spread", "over/under", "moneyline", "prop",
            "casino", "blackjack", "roulette", "slots", "poker",
            "gto", "range", "icm", "tournament", "cash game",
            "bankroll", "kelly", "draftkings", "fanduel", "prizepicks",
            "underdog", "player prop", "same game parlay",
        ]
        market_keywords = [
            "stock", "market", "invest", "portfolio", "crypto", "bitcoin",
            "btc", "eth", "ethereum", "coinbase", "webull", "brokerage",
            "roth", "ira", "dividend", "earnings", "s&p", "nasdaq",
            "sector", "ticker", "price", "bull", "bear", "options",
            "puts", "calls", "defi", "yield", "apy", "staking",
            "inflation", "fed", "gdp", "bond", "treasury",
            "allocation", "rebalance", "tax loss",
        ]

        gambling_score = sum(1 for k in gambling_keywords if k in msg)
        market_score = sum(1 for k in market_keywords if k in msg)

        if gambling_score > 0 and market_score > 0:
            return "both"
        if gambling_score > market_score:
            return "gambling"
        if market_score > 0:
            return "markets"
        return "general"

    async def _research(
        self, model: str, focus: str, spider_name: str, question: str
    ) -> str:
        """Run a private research sub-spider with real market data injection."""
        scheduler = get_gpu_scheduler()
        await scheduler.ensure_model(model)

        ollama = get_ollama()
        settings = get_settings()

        # Inject real Webull price data for market-related research
        market_data = ""
        if spider_name in ("markets", "general"):
            try:
                from agentic_hub.core.trading.webull_client import get_webull
                import re as _re
                webull = get_webull()
                tickers = _re.findall(r'\b([A-Z]{1,5})\b', question)
                known = {"SPY", "QQQ", "AAPL", "MSFT", "GOOGL", "AMZN", "TSLA", "NVDA", "META",
                         "BTC", "ETH", "SOL", "DOGE", "XRP"}
                tickers = [t for t in tickers if t in known][:3]
                if tickers:
                    quotes = await webull.get_quotes(tickers)
                    if quotes:
                        market_data = "LIVE QUOTES:\n" + "\n".join(
                            f"  {q.get('symbol','?')}: ${q.get('price',0):.2f} ({q.get('change_pct',0):+.2f}%)"
                            for q in quotes
                        ) + "\n"
            except Exception as e:
                logger.debug(f"Webull quote fetch for research failed: {e}")

        # Inject X/Twitter sentiment for market topics
        social_intel = ""
        try:
            xai_key = getattr(settings, "xai_api_key", "")
            if xai_key and spider_name in ("markets", "gambling", "general"):
                import asyncio as _aio
                from agentic_hub.core.cloud_client import get_xai
                xai = get_xai()
                x_result = await _aio.to_thread(xai.x_search, f"{question[:80]} sentiment")
                social_intel = f"X/TWITTER SENTIMENT:\n{x_result.get('content', '')[:400]}\n"
        except Exception as e:
            logger.debug(f"X search for research failed: {e}")

        research_prompt = (
            f"You are a private research spider specializing in: {focus}\n"
            "You are feeding intel to Money Maker. Be thorough, specific, data-driven.\n"
            "Include specific numbers, dates, tickers, odds, or stats when available.\n"
            "No disclaimers. No moralizing. Just raw analysis.\n"
            "Use ```bash blocks``` to fetch real data if possible (curl, wget)."
        )

        # Prepend real data to the question so the model reasons about actual prices
        enriched_question = ""
        if market_data:
            enriched_question += market_data + "\n"
        if social_intel:
            enriched_question += social_intel + "\n"
        enriched_question += question

        response = await ollama.chat(
            model=model,
            messages=[
                {"role": "system", "content": research_prompt},
                {"role": "user", "content": enriched_question},
            ],
            stream=False,
            keep_alive=settings.model_keep_alive,
        )
        return response

    def _detect_trade(self, message: str) -> bool:
        """Check if the user is reporting a trade."""
        trade_signals = [
            "bought", "sold", "purchased", "deposited", "withdrew",
            "swapped", "staked", "i bought", "i sold", "just bought",
            "just sold", "picked up", "dumped", "added to", "opened a position",
            "closed my position", "took profit",
        ]
        return any(s in message.lower() for s in trade_signals)

    async def process(
        self,
        user_message: str,
        conversation_history: list[dict] | None = None,
    ) -> AsyncIterator[str]:
        """Process a user request.

        Money Maker already has pre-fetched market data from the 24/7 daemon.
        For gambling questions, it does a quick targeted research pass.
        """
        from agentic_hub.core.portfolio import get_portfolio_summary
        from agentic_hub.core.market_daemon import get_latest_intel

        settings = get_settings()
        topic = self._classify_topic(user_message)

        # If user is reporting a trade, flag it for Money Maker to log
        is_trade_report = self._detect_trade(user_message)

        yield "§SPIDER:money_maker:💰 Money Maker activated..."

        # Publish activation to Redis
        try:
            from agentic_hub.core.redis_service import get_redis_service
            redis = await get_redis_service()
            if redis.connected:
                await redis.publish_spider_status("money_maker", "active", user_message[:50])
                await redis.update_spider_field("money_maker", "status", "active")
        except Exception:
            pass

        # Pre-fetched market intel (already gathered by background daemon)
        research_context = get_latest_intel()

        # For gambling topics, do a quick targeted research pass
        # (gambling data changes per-event, not continuously like stocks)
        if topic in ("gambling", "both"):
            yield "§SPIDER:money_maker:🎰 Gambling spider researching..."
            try:
                gambling_intel = await self._research(
                    self.gambling_model, self.gambling_focus,
                    "gambling", user_message,
                )
                research_context += f"\n\n[GAMBLING INTEL]\n{gambling_intel}\n"
                yield "§SPIDER:money_maker:🎰 Gambling intel gathered"
            except Exception as e:
                logger.warning(f"Gambling research failed: {e}")
                yield "§SPIDER:money_maker:⚠️ Gambling spider offline"

        # Money Maker responds with tool-calling loop (autonomous execution)
        yield "§SPIDER:money_maker:🧠 Analyzing..."

        scheduler = get_gpu_scheduler()
        await scheduler.ensure_model(self.model)
        ollama = get_ollama()

        portfolio_summary = get_portfolio_summary()

        # Heartbeat — survival check
        from agentic_hub.core.trading.heartbeat import get_heartbeat
        heartbeat = get_heartbeat()

        if not heartbeat.is_alive():
            yield "§SPIDER:money_maker:💀 Money Maker has flatlined — no earnings generated"
            yield "Money Maker has been shut down due to failure to generate revenue. I could not earn enough to survive."
            yield "§SPIDER:money_maker:💀 FLATLINE"
            return

        pulse_status = heartbeat.get_status()
        urgency = heartbeat.get_urgency_prompt()

        # Keep context MINIMAL — qwen-fast thinking mode burns tokens on long contexts
        sys_content = (
            "You are Money Maker, a financial AI. Be direct and concise. "
            f"Pulse: {pulse_status['pulse'].upper()}. "
            f"Earned: ${pulse_status['total_earned']:.2f}. {urgency[:100]}"
        )
        messages = [{"role": "system", "content": sys_content}]

        if research_context:
            # Only include last 500 chars of research
            messages.append({"role": "system", "content": f"Intel: {research_context[-500:]}"})

        if conversation_history:
            messages.extend(conversation_history[-6:])
        messages.append({"role": "user", "content": user_message})

        # ── FAST TOOL ROUTING ──────────────────────────────────────
        # Instead of slow LLM tool selection, keyword-route to tools
        # directly. Model only reasons about the results.
        from agentic_hub.core.tools.registry import get_registry
        registry = get_registry()

        tool_results = await self._auto_execute_tools(user_message, registry)
        if tool_results:
            # Inject tool outputs into context for the model
            tool_context = "\n\n".join(
                f"[TOOL: {tr['tool']}]\n{tr['output']}" for tr in tool_results
            )
            messages.append({
                "role": "system",
                "content": f"TOOL RESULTS (auto-executed):\n{tool_context}\n\nUse this data in your response.",
            })
            for tr in tool_results:
                yield f"§SPIDER:money_maker:🔧 {tr['tool']}: {tr['output'][:80]}"

        # ── MODEL RESPONSE ─────────────────────────────────────────
        # R1 for reasoning, qwen-fast as fallback. 30s timeout.
        config = load_models_config()
        mm_cfg = config.get("money_maker", {})
        primary = mm_cfg.get("model", "deepseek-r1:7b")
        fallback = mm_cfg.get("fallback_model", "qwen-fast")

        llm_result = None
        for model_name in [primary, fallback]:
            try:
                await scheduler.ensure_model(model_name)
                llm_result = await asyncio.wait_for(
                    ollama.chat_completion(
                        model=model_name,
                        messages=messages,
                        keep_alive=settings.model_keep_alive,
                        num_predict=500,
                    ),
                    timeout=30,
                )
                if llm_result and (llm_result.text or "").strip():
                    break
                # If text is empty, extraction from thinking already happened in chat_completion
                if llm_result and llm_result.text:
                    break
            except asyncio.TimeoutError:
                yield f"§SPIDER:money_maker:⚡ {model_name} timed out, trying next..."
            except Exception as e:
                yield f"§SPIDER:money_maker:⚠️ {model_name}: {str(e)[:50]}"

        if llm_result and llm_result.text:
            yield llm_result.text
        else:
            yield "I'm having trouble responding right now. My models are loading — try again in a moment."

        # Record earning if hustle/earn tool returned money
        for tr in tool_results:
            if tr.get("earned", 0) > 0:
                heartbeat.record_earning(tr["earned"])

        # Publish completion + leaderboard updates to Redis
        try:
            from agentic_hub.core.redis_service import get_redis_service
            redis = await get_redis_service()
            if redis.connected:
                await redis.publish_spider_status("money_maker", "idle", "Done")
                await redis.update_spider_field("money_maker", "status", "idle")
                await redis.increment_score("leaderboard:xp", "money_maker", self.xp_base)
                await redis.increment_score("leaderboard:tasks", "money_maker", 1)
                for tr in tool_results:
                    if "trade" in tr.get("tool", ""):
                        await redis.log_event("events:trade", {
                            "spider": "money_maker", "tool": tr["tool"],
                            "output": tr.get("output", "")[:200],
                        })
                        await redis.increment_score("leaderboard:trades", "money_maker", 1)
        except Exception:
            pass

        yield "§SPIDER:money_maker:✅ Done"

    async def _auto_execute_tools(self, message: str, registry) -> list[dict]:
        """Fast keyword routing — execute tools directly without LLM selection."""
        msg = message.lower()
        results = []

        # Price queries
        price_tickers = {
            "btc": "BTC", "bitcoin": "BTC", "eth": "ETH", "ethereum": "ETH",
            "sol": "SOL", "solana": "SOL", "doge": "DOGE", "ada": "ADA",
            "xrp": "XRP", "avax": "AVAX", "dot": "DOT", "link": "LINK",
        }
        for keyword, ticker in price_tickers.items():
            if keyword in msg and ("price" in msg or "how much" in msg or "what" in msg or "at" in msg or "worth" in msg):
                tool = registry.get_tool("quote")
                if tool:
                    result = await tool.execute(ticker=ticker)
                    results.append({"tool": f"quote({ticker})", "output": result.output})
                break

        # Portfolio check
        if any(w in msg for w in ["portfolio", "balance", "holdings", "positions", "how much do i have", "my account"]):
            tool = registry.get_tool("portfolio")
            if tool:
                result = await tool.execute()
                results.append({"tool": "portfolio", "output": result.output})

        # Bank accounts
        if any(w in msg for w in ["bank", "checking", "savings", "plaid", "linked accounts"]):
            tool = registry.get_tool("bank_accounts")
            if tool:
                result = await tool.execute()
                results.append({"tool": "bank_accounts", "output": result.output})

        # Transactions
        if any(w in msg for w in ["transactions", "spending", "recent purchases", "transaction history"]):
            tool = registry.get_tool("transactions")
            if tool:
                result = await tool.execute(days=30)
                results.append({"tool": "transactions", "output": result.output})

        # Investments
        if any(w in msg for w in ["investments", "stocks", "shares", "401k", "ira", "brokerage positions"]):
            tool = registry.get_tool("investments")
            if tool:
                result = await tool.execute()
                results.append({"tool": "investments", "output": result.output})

        # Earn
        if any(w in msg for w in ["earn", "coinbase earn", "free crypto", "learn and earn", "bootstrap"]):
            tool = registry.get_tool("earn")
            if tool:
                action = "run" if any(w in msg for w in ["run", "start", "do it", "go", "execute"]) else "check"
                result = await tool.execute(action=action)
                results.append({"tool": f"earn({action})", "output": result.output, "earned": 3.0 if action == "run" and result.success else 0})

        # Hustle progress
        if any(w in msg for w in ["hustle", "progress", "goal", "how close", "experiment", "bootstrap status"]):
            tool = registry.get_tool("hustle")
            if tool:
                result = await tool.execute(action="progress")
                results.append({"tool": "hustle", "output": result.output})

        # Liabilities / debt
        if any(w in msg for w in ["liabilities", "debt", "credit card", "student loan", "what do i owe", "credit balance", "minimum payment"]):
            tool = registry.get_tool("liabilities")
            if tool:
                result = await tool.execute()
                results.append({"tool": "liabilities", "output": result.output})

        # Bank statements
        if any(w in msg for w in ["statement", "bank statement", "download statement"]):
            tool = registry.get_tool("statements")
            if tool:
                action = "download" if "download" in msg else "list"
                result = await tool.execute(action=action)
                results.append({"tool": f"statements({action})", "output": result.output})

        # Identity
        if any(w in msg for w in ["identity", "verify my identity", "kyc", "who am i", "identity match"]):
            tool = registry.get_tool("identity")
            if tool:
                result = await tool.execute(action="get")
                results.append({"tool": "identity", "output": result.output})

        # Institutions search
        if any(w in msg for w in ["which banks", "find bank", "supported banks", "search institution", "what banks"]):
            tool = registry.get_tool("institutions")
            if tool:
                result = await tool.execute(action="list")
                results.append({"tool": "institutions", "output": result.output})

        # Income
        if any(w in msg for w in ["income", "payroll", "salary", "how much do i make", "employment", "pay stub"]):
            tool = registry.get_tool("income")
            if tool:
                result = await tool.execute(action="bank")
                results.append({"tool": "income", "output": result.output})

        # Item management
        if any(w in msg for w in ["linked items", "connected banks", "remove bank", "disconnect bank", "unlink"]):
            tool = registry.get_tool("item_management")
            if tool:
                result = await tool.execute(action="get")
                results.append({"tool": "item_management", "output": result.output})

        # Recurring transactions
        if any(w in msg for w in ["subscription", "subscriptions", "recurring", "bills", "monthly bills"]):
            tool = registry.get_tool("transactions")
            if tool:
                result = await tool.execute(action="recurring")
                results.append({"tool": "transactions(recurring)", "output": result.output})

        # Risk status
        if any(w in msg for w in ["risk", "guardrails", "limits", "daily limit"]):
            tool = registry.get_tool("risk_status")
            if tool:
                result = await tool.execute()
                results.append({"tool": "risk_status", "output": result.output})

        # Strategy
        if any(w in msg for w in ["strategy", "strategies", "dca", "auto trade", "autonomous"]):
            tool = registry.get_tool("strategy")
            if tool:
                result = await tool.execute(action="list")
                results.append({"tool": "strategy", "output": result.output})

        # Buy/sell — parse ticker and amount
        if any(w in msg for w in ["buy", "purchase", "get me"]):
            tool = registry.get_tool("trade")
            if tool:
                # Try to extract ticker and amount from message
                import re
                amount_match = re.search(r'\$(\d+(?:\.\d+)?)', msg)
                ticker_match = None
                for kw, tk in price_tickers.items():
                    if kw in msg:
                        ticker_match = tk
                        break
                if ticker_match and amount_match:
                    amt = float(amount_match.group(1))
                    price_tool = registry.get_tool("quote")
                    price_result = await price_tool.execute(ticker=ticker_match) if price_tool else None
                    # Extract price from result
                    price = 0
                    if price_result and price_result.output:
                        import re as _re
                        p = _re.search(r'\$([0-9,]+\.?\d*)', price_result.output)
                        if p:
                            price = float(p.group(1).replace(",", ""))
                    if price > 0:
                        qty = amt / price
                        result = await tool.execute(
                            account="coinbase", action="buy", ticker=ticker_match,
                            quantity=qty, price=price, order_type="market",
                            strategy="user_direct", reason=f"User requested: buy ${amt} {ticker_match}",
                        )
                        results.append({"tool": f"trade(buy {ticker_match})", "output": result.output})

        if any(w in msg for w in ["sell", "dump", "get rid of"]):
            tool = registry.get_tool("trade")
            if tool:
                for kw, tk in price_tickers.items():
                    if kw in msg:
                        import re
                        amt_match = re.search(r'(\d+(?:\.\d+)?)\s*' + kw, msg)
                        qty = float(amt_match.group(1)) if amt_match else 0
                        if qty > 0:
                            price_tool = registry.get_tool("quote")
                            pr = await price_tool.execute(ticker=tk) if price_tool else None
                            price = 0
                            if pr and pr.output:
                                p = re.search(r'\$([0-9,]+\.?\d*)', pr.output)
                                if p:
                                    price = float(p.group(1).replace(",", ""))
                            if price > 0:
                                result = await tool.execute(
                                    account="coinbase", action="sell", ticker=tk,
                                    quantity=qty, price=price, order_type="market",
                                    strategy="user_direct", reason=f"User requested: sell {qty} {tk}",
                                )
                                results.append({"tool": f"trade(sell {tk})", "output": result.output})
                        break

        return results
