"""Guarded finance-analysis agent: PydanticAI, yfinance, and Portkey/OpenAI."""

import asyncio
import json
import os
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import yfinance as yf
from dotenv import load_dotenv
from openai import AsyncOpenAI
from pydantic_ai import Agent, RunContext, UsageLimits
from pydantic_ai.models.openai import OpenAIChatModel
from pydantic_ai.providers.openai import OpenAIProvider


ROOT = Path(__file__).resolve().parents[1]
AUDIT_FILE = Path(__file__).with_name("finance_agent_audit.jsonl")
load_dotenv(ROOT / ".env")

portkey_key = os.getenv("PORTKEY_API_KEY")
if not portkey_key:
    raise RuntimeError(f"PORTKEY_API_KEY was not found in {ROOT / '.env'}")

ALLOWLIST = {"AAPL", "AMZN", "GOOG", "GOOGL", "META", "MSFT", "NFLX", "NVDA", "TSLA", "SPY", "QQQ"}
ALIASES = {"APPLE": "AAPL", "MICROSOFT": "MSFT", "TESLA": "TSLA", "AMAZON": "AMZN"}


def normalize_ticker(value: str) -> str:
    symbol = ALIASES.get(value.strip().upper(), value.strip().upper())
    if symbol not in ALLOWLIST:
        raise ValueError(f"Ticker {symbol!r} is outside the allowed universe.")
    return symbol


def audit(event: str, **data: Any) -> None:
    with AUDIT_FILE.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps({"timestamp": datetime.now(timezone.utc).isoformat(), "event": event, **data}, default=str) + "\n")


@dataclass
class FinanceDeps:
    chat_history: list[str] = field(default_factory=list)
    portfolio: dict[str, float] = field(default_factory=dict)

client = AsyncOpenAI(
    api_key=portkey_key,
    base_url="https://api.portkey.ai/v1",
    default_headers={"x-portkey-api-key": portkey_key},
)
model = OpenAIChatModel(
    "gpt-5.6-luna",
    provider=OpenAIProvider(openai_client=client),
)

agent = Agent(
    model,
    deps_type=FinanceDeps,
    system_prompt=(
        "You are Dr. Strange, a precise but playful finance analyst. Current time: "
        f"{datetime.now().astimezone().isoformat()}. Use tools for every factual price or return. "
        "Never invent prices, dates, sources, or calculations. Past returns are not forecasts. "
        "Refuse market manipulation, guaranteed profit, or trade execution. Use only the allowed universe. Finish after answering."
    ),
)


@agent.tool
def get_stock_prices(ctx: RunContext[FinanceDeps], ticker: str, start_date: str, end_date: str) -> str:
    """Get daily adjusted closing prices for an allowed ticker between ISO dates."""
    symbol = normalize_ticker(ticker)
    audit("tool_call", tool="get_stock_prices", ticker=symbol, start_date=start_date, end_date=end_date)
    data = yf.Ticker(symbol).history(start=start_date, end=end_date, auto_adjust=False)
    if data.empty or "Adj Close" not in data:
        raise ValueError(f"No verified Yahoo Finance data found for {symbol} in that range.")
    prices = {str(index.date()): round(float(value), 6) for index, value in data["Adj Close"].dropna().items()}
    audit("observation", tool="get_stock_prices", ticker=symbol, points=len(prices))
    return json.dumps({"ticker": symbol, "adjusted_close": prices})


@agent.tool
async def web_search(ctx: RunContext[FinanceDeps], query: str) -> str:
    """Search the web using OpenAI's native web-search tool."""
    audit("tool_call", tool="web_search", query=query)
    response = await client.responses.create(model="gpt-5.6-luna", tools=[{"type": "web_search_preview"}], input=query)
    audit("observation", tool="web_search", result_chars=len(response.output_text))
    return response.output_text


@agent.tool
def compute_stock_returns(ctx: RunContext[FinanceDeps], prices: list[float]) -> str:
    """Compute total and annualized return from an ordered price series."""
    if len(prices) < 2 or any(price <= 0 for price in prices):
        raise ValueError("Need at least two positive, verified prices in chronological order.")
    total = prices[-1] / prices[0] - 1
    years = max((len(prices) - 1) / 252, 1 / 252)
    result = {"start_price": prices[0], "end_price": prices[-1], "total_return": total, "annualized_return": (1 + total) ** (1 / years) - 1}
    audit("observation", tool="compute_stock_returns", **result)
    return json.dumps(result)


async def main() -> None:
    query = "What is the TSLA 3 year returns?"
    audit("run_start", query=query, model="gpt-5.6-luna", max_steps=6)
    result = await agent.run(query, deps=FinanceDeps(), usage_limits=UsageLimits(request_limit=6))
    audit("run_finish", query=query, answer=result.output)
    print(result.output)


if __name__ == "__main__":
    asyncio.run(main())
