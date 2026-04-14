"""Market Research Daemon — 24/7 background intelligence gathering.

Runs as a background asyncio task when the server starts.
Research spiders continuously fetch market data, analyze trends,
and store findings to disk. Money Maker reads this pre-fetched
intel instantly when the user asks — no delay.

Cycle: fetch raw data → spider analyzes → store findings → sleep → repeat
"""
from __future__ import annotations

import asyncio
import json
import logging
import subprocess
import time
from datetime import datetime
from pathlib import Path

logger = logging.getLogger(__name__)

# Daemon uptime tracking (for achievement: cron_overlord)
_daemon_started_at: float = 0.0


def get_daemon_uptime_hours() -> float:
    """Return how long the market daemon has been running, in hours."""
    if _daemon_started_at == 0.0:
        return 0.0
    return (time.time() - _daemon_started_at) / 3600

DATA_DIR = Path(__file__).parent.parent.parent.parent / "data"
INTEL_DIR = DATA_DIR / "market_intel"

# Research intervals (seconds)
MARKET_INTERVAL = 900     # 15 min — stock/crypto prices
DEEP_INTERVAL = 3600      # 1 hour — deep analysis via LLM
GAMBLING_INTERVAL = 1800  # 30 min — odds/lines (change less frequently)


def _ensure_dirs():
    INTEL_DIR.mkdir(parents=True, exist_ok=True)


def _save_intel(category: str, data: dict):
    """Save research findings to disk."""
    _ensure_dirs()
    filepath = INTEL_DIR / f"{category}.json"
    # Keep history — append to a rolling log
    history_file = INTEL_DIR / f"{category}_history.jsonl"

    # Current snapshot
    data["timestamp"] = datetime.now().isoformat()
    filepath.write_text(json.dumps(data, indent=2, default=str))

    # Append to rolling history (keep last 200 entries)
    with open(history_file, "a") as f:
        f.write(json.dumps(data, default=str) + "\n")

    # Trim history
    try:
        lines = history_file.read_text().strip().split("\n")
        if len(lines) > 200:
            history_file.write_text("\n".join(lines[-200:]) + "\n")
    except Exception:
        pass


_http_client: "httpx.AsyncClient | None" = None

async def _fetch_url(url: str, timeout: int = 15) -> str:
    """Fetch URL with httpx — no shell, no subprocess, no SSRF vector."""
    global _http_client
    import httpx
    if _http_client is None:
        _http_client = httpx.AsyncClient(timeout=timeout, follow_redirects=True)
    try:
        resp = await _http_client.get(url)
        return resp.text
    except Exception as e:
        return f"Error: {e}"


    # _fetch_cmd removed — all HTTP calls now use _fetch_url (httpx, no shell)


async def _fetch_stock_prices() -> dict:
    """Fetch current prices for major indices and watchlist."""
    symbols = ["SPY", "QQQ", "DIA", "IWM", "VTI",  # indices
               "AAPL", "MSFT", "NVDA", "GOOGL", "AMZN", "META", "TSLA",  # big tech
               "VYM", "SCHD", "JEPI", "O", "AGNC",  # dividends
               ]

    # Load user's watchlist and positions (with ticker validation)
    import re as _re
    TICKER_RE = _re.compile(r"^[A-Z0-9._-]{1,10}$")
    portfolio_file = DATA_DIR / "portfolio.json"
    if portfolio_file.exists():
        try:
            portfolio = json.loads(portfolio_file.read_text())
            for acct in portfolio.get("accounts", {}).values():
                for pos in acct.get("positions", []):
                    ticker = pos.get("ticker", "").upper()
                    if ticker and TICKER_RE.match(ticker) and ticker not in symbols:
                        symbols.append(ticker)
            for w in portfolio.get("watchlist", []):
                ticker = w.get("ticker", "").upper()
                if ticker and TICKER_RE.match(ticker) and ticker not in symbols:
                    symbols.append(ticker)
        except Exception:
            pass

    prices = {}
    # Batch fetch via Yahoo Finance (httpx, no shell)
    sym_str = ",".join(symbols[:30])  # limit batch size
    raw = await _fetch_url(
        f"https://query1.finance.yahoo.com/v7/finance/quote?symbols={sym_str}&fields=regularMarketPrice,regularMarketChange,regularMarketChangePercent,regularMarketDayHigh,regularMarketDayLow,regularMarketVolume,fiftyTwoWeekHigh,fiftyTwoWeekLow,trailingAnnualDividendYield"
    )

    try:
        data = json.loads(raw)
        for q in data.get("quoteResponse", {}).get("result", []):
            prices[q.get("symbol", "")] = {
                "price": q.get("regularMarketPrice", 0),
                "change": q.get("regularMarketChange", 0),
                "change_pct": q.get("regularMarketChangePercent", 0),
                "high": q.get("regularMarketDayHigh", 0),
                "low": q.get("regularMarketDayLow", 0),
                "volume": q.get("regularMarketVolume", 0),
                "52w_high": q.get("fiftyTwoWeekHigh", 0),
                "52w_low": q.get("fiftyTwoWeekLow", 0),
                "div_yield": q.get("trailingAnnualDividendYield", 0),
            }
    except Exception as e:
        logger.warning(f"Stock price fetch failed: {e}")

    return prices


async def _fetch_crypto_prices() -> dict:
    """Fetch crypto prices from CoinGecko (httpx, no shell)."""
    raw = await _fetch_url(
        "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum,solana,cardano,dogecoin,chainlink,avalanche-2,polkadot,polygon-ecosystem-token,uniswap&vs_currencies=usd&include_24hr_change=true&include_24hr_vol=true&include_market_cap=true"
    )
    try:
        return json.loads(raw)
    except Exception:
        return {}


async def _fetch_fear_greed() -> dict:
    """Fetch crypto fear & greed index (httpx, no shell)."""
    raw = await _fetch_url("https://api.alternative.me/fng/?limit=1")
    try:
        data = json.loads(raw)
        entry = data.get("data", [{}])[0]
        return {"value": entry.get("value"), "label": entry.get("value_classification")}
    except Exception:
        return {}


async def market_data_loop():
    """Continuously fetch raw market data (every 15 min)."""
    logger.info("Market data daemon started — fetching every %ds", MARKET_INTERVAL)
    while True:
        try:
            stocks = await _fetch_stock_prices()
            crypto = await _fetch_crypto_prices()
            fng = await _fetch_fear_greed()

            intel = {
                "stocks": stocks,
                "crypto": crypto,
                "fear_greed": fng,
                "market_open": _is_market_open(),
            }
            _save_intel("market_data", intel)

            stock_count = len(stocks)
            crypto_count = len(crypto)
            logger.info(f"Market data updated: {stock_count} stocks, {crypto_count} crypto")

        except Exception as e:
            logger.warning(f"Market data fetch error: {e}")

        await asyncio.sleep(MARKET_INTERVAL)


async def deep_analysis_loop():
    """Spider-powered deep analysis (every 1 hour).

    Uses the Markets research spider to analyze trends from the raw data.
    """
    logger.info("Deep analysis daemon started — analyzing every %ds", DEEP_INTERVAL)
    # Wait for first market data fetch
    await asyncio.sleep(60)

    while True:
        try:
            # Load latest market data
            market_file = INTEL_DIR / "market_data.json"
            if not market_file.exists():
                await asyncio.sleep(300)
                continue

            market_data = json.loads(market_file.read_text())

            # Use the Markets research spider for analysis
            from agentic_hub.config import get_settings, load_models_config
            from agentic_hub.core.gpu_scheduler import get_gpu_scheduler
            from agentic_hub.core.ollama_client import get_ollama

            config = load_models_config()
            mm_cfg = config.get("money_maker", {})
            markets_model = mm_cfg.get("research_spiders", {}).get("markets", {}).get("model", "qwen-fast")
            settings = get_settings()

            scheduler = get_gpu_scheduler()
            await scheduler.ensure_model(markets_model)
            ollama = get_ollama()

            # Build analysis prompt with current data
            stock_summary = ""
            for sym, d in list(market_data.get("stocks", {}).items())[:15]:
                pct = d.get("change_pct", 0)
                arrow = "🟢" if pct > 0 else "🔴" if pct < 0 else "⚪"
                stock_summary += f"  {arrow} {sym}: ${d.get('price', 0):.2f} ({pct:+.2f}%)\n"

            crypto_summary = ""
            for coin, d in market_data.get("crypto", {}).items():
                pct = d.get("usd_24h_change", 0)
                arrow = "🟢" if pct > 0 else "🔴"
                crypto_summary += f"  {arrow} {coin}: ${d.get('usd', 0):,.2f} ({pct:+.1f}%)\n"

            fng = market_data.get("fear_greed", {})
            fng_text = f"Fear & Greed: {fng.get('value', '?')} ({fng.get('label', '?')})" if fng else ""

            analysis = await ollama.chat(
                model=markets_model,
                messages=[
                    {"role": "system", "content": (
                        "You are a financial research analyst. Analyze the current market data below. "
                        "Provide: (1) Market sentiment summary, (2) Top 3 opportunities, (3) Top 3 risks, "
                        "(4) Sector rotation signals, (5) Crypto market cycle position. "
                        "Be specific. Use the actual numbers. No disclaimers."
                    )},
                    {"role": "user", "content": (
                        f"CURRENT MARKET DATA ({market_data.get('timestamp', 'now')}):\n\n"
                        f"STOCKS:\n{stock_summary}\n"
                        f"CRYPTO:\n{crypto_summary}\n"
                        f"{fng_text}\n"
                        f"Market {'OPEN' if market_data.get('market_open') else 'CLOSED'}"
                    )},
                ],
                stream=False,
                keep_alive=settings.model_keep_alive,
            )

            _save_intel("deep_analysis", {
                "analysis": analysis,
                "based_on": market_data.get("timestamp", ""),
            })
            logger.info("Deep analysis updated")

        except Exception as e:
            logger.warning(f"Deep analysis error: {e}")

        await asyncio.sleep(DEEP_INTERVAL)


def _is_market_open() -> bool:
    """Check if US stock market is currently open (rough check)."""
    now = datetime.now()
    # Weekday 9:30 AM - 4:00 PM ET (approximate — doesn't account for timezone perfectly)
    if now.weekday() >= 5:  # weekend
        return False
    hour = now.hour
    return 9 <= hour <= 16


def get_latest_intel() -> str:
    """Get all pre-fetched intel for injection into Money Maker's context.

    This is what Money Maker reads when the user asks a question —
    no delay, the data is already here.
    """
    _ensure_dirs()
    parts = []

    # Latest market data
    market_file = INTEL_DIR / "market_data.json"
    if market_file.exists():
        try:
            data = json.loads(market_file.read_text())
            ts = data.get("timestamp", "unknown")
            parts.append(f"=== LIVE MARKET DATA (as of {ts}) ===\n")

            for sym, d in data.get("stocks", {}).items():
                pct = d.get("change_pct", 0)
                div = d.get("div_yield", 0)
                div_str = f" | div {div*100:.1f}%" if div else ""
                parts.append(f"  {sym}: ${d.get('price',0):.2f} ({pct:+.2f}%){div_str}")

            parts.append("")
            for coin, d in data.get("crypto", {}).items():
                pct = d.get("usd_24h_change", 0)
                mcap = d.get("usd_market_cap", 0)
                parts.append(f"  {coin}: ${d.get('usd',0):,.2f} ({pct:+.1f}%) mcap: ${mcap/1e9:.1f}B")

            fng = data.get("fear_greed", {})
            if fng:
                parts.append(f"\n  Fear & Greed Index: {fng.get('value','?')} — {fng.get('label','?')}")
        except Exception:
            pass

    # Latest deep analysis
    analysis_file = INTEL_DIR / "deep_analysis.json"
    if analysis_file.exists():
        try:
            data = json.loads(analysis_file.read_text())
            parts.append(f"\n=== ANALYSIS (as of {data.get('timestamp','?')}) ===")
            parts.append(data.get("analysis", "No analysis yet."))
        except Exception:
            pass

    if not parts:
        return "No market intel available yet. Research spiders are still gathering data."

    return "\n".join(parts)


async def start_daemon():
    """Start all background research loops. Called on server startup."""
    global _daemon_started_at
    _daemon_started_at = time.time()
    _ensure_dirs()
    logger.info("Starting Money Maker research daemon...")
    asyncio.create_task(market_data_loop())
    asyncio.create_task(deep_analysis_loop())
