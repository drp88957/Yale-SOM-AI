"""Bounded website-profile agent for Homework 2."""

from __future__ import annotations

import argparse
import asyncio
import json
import os
import re
import ssl
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from urllib.parse import urljoin, urlparse
from urllib.request import Request, urlopen

from dotenv import load_dotenv
from openai import AsyncOpenAI
from pydantic_ai import Agent, RunContext, UsageLimits
from pydantic_ai.models.openai import OpenAIChatModel
from pydantic_ai.providers.openai import OpenAIProvider

ROOT = Path(__file__).resolve().parent
AUDIT_FILE = ROOT / "output" / "audit_log.json"
PROFILE_FILE = ROOT / "assets" / "company_profile.json"
TARGETS_FILE = ROOT / "output" / "targets.json"
EMAILS_FILE = ROOT / "output" / "emails.json"
load_dotenv(ROOT / ".env")
KEY = os.getenv("PORTKEY_API_KEY")
if not KEY:
    raise RuntimeError("PORTKEY_API_KEY is missing from the project .env file")


def audit(event: str, **data: Any) -> None:
    AUDIT_FILE.parent.mkdir(exist_ok=True)
    try:
        records = json.loads(AUDIT_FILE.read_text(encoding="utf-8")) if AUDIT_FILE.exists() else []
    except json.JSONDecodeError:
        records = []
    record = {"timestamp": datetime.now(timezone.utc).isoformat(), "event": event, **data}
    if event == "tool_call":
        tool = data.get("tool", "tool")
        record["iteration"] = sum(1 for item in records if item.get("event") == "tool_call") + 1
        record["thought_summary"] = f"Using {tool} to gather or validate the next piece of evidence."
    records.append(record)
    AUDIT_FILE.write_text(json.dumps(records, indent=2, default=str), encoding="utf-8")


class SalesDeps:
    def __init__(self, url: str):
        self.url = url.rstrip("/") + "/"
        self.pages: dict[str, str] = {}


client = AsyncOpenAI(api_key=KEY, base_url="https://api.portkey.ai/v1",
                     default_headers={"x-portkey-api-key": KEY})
model = OpenAIChatModel("gpt-5.6-luna", provider=OpenAIProvider(openai_client=client))
prompt = (ROOT / "prompts" / "sales_agent.md").read_text(encoding="utf-8")
agent = Agent(model, deps_type=SalesDeps, output_type=str, system_prompt=prompt)


def _clean(html: str) -> str:
    html = re.sub(r"<(script|style|noscript)[^>]*>.*?</\1>", " ", html, flags=re.I | re.S)
    text = re.sub(r"<[^>]+>", " ", html)
    return re.sub(r"\s+", " ", text).strip()[:18000]


@agent.tool
def crawl_company_website(ctx: RunContext[SalesDeps], paths: list[str]) -> str:
    """Fetch up to six relevant public pages on the supplied domain."""
    paths = list(dict.fromkeys(paths))[:6]
    results = []
    for path in paths:
        url = urljoin(ctx.deps.url, path)
        if urlparse(url).netloc != urlparse(ctx.deps.url).netloc:
            continue
        audit("tool_call", tool="crawl_company_website", args={"url": url})
        try:
            req = Request(url, headers={"User-Agent": "HomeworkSalesResearch/1.0"})
            with urlopen(req, timeout=15) as response:
                raw = response.read(600_000).decode("utf-8", errors="replace")
            body = _clean(raw)
            ctx.deps.pages[url] = body
            results.append({"url": url, "text": body})
            audit("tool_result", tool="crawl_company_website", result_summary=f"Fetched {len(body)} characters from {url}")
        except Exception as exc:
            audit("tool_result", tool="crawl_company_website", result_summary=f"Failed {url}: {type(exc).__name__}")
            results.append({"url": url, "error": type(exc).__name__})
    return json.dumps(results)


@agent.tool
def save_company_profile(ctx: RunContext[SalesDeps], profile_json: str) -> str:
    """Validate and save the agent's JSON profile."""
    profile = json.loads(profile_json)
    if not isinstance(profile, dict) or not profile.get("company_name"):
        raise ValueError("Profile must be an object with company_name")
    PROFILE_FILE.parent.mkdir(exist_ok=True)
    PROFILE_FILE.write_text(json.dumps(profile, indent=2, ensure_ascii=False), encoding="utf-8")
    audit("tool_result", tool="save_company_profile", result_summary=f"Saved profile for {profile['company_name']}")
    return f"Saved valid company profile to {PROFILE_FILE.as_posix()}"


@agent.tool
def read_company_profile(ctx: RunContext[SalesDeps], profile_path: str) -> str:
    """Read the previously researched seller profile from the workspace."""
    path = (ROOT / profile_path).resolve()
    if path != PROFILE_FILE.resolve():
        raise ValueError("Only the approved seller profile path may be read.")
    profile = json.loads(path.read_text(encoding="utf-8"))
    audit("tool_call", tool="read_company_profile", args={"profile_path": profile_path})
    audit("tool_result", tool="read_company_profile", result_summary=f"Loaded {len(profile)} profile fields")
    return json.dumps(profile)


@agent.tool
async def search_customer_candidates(ctx: RunContext[SalesDeps], search_query: str) -> str:
    """Use Portkey web search to find candidate organizations; this does not contact them."""
    audit("tool_call", tool="search_customer_candidates", args={"search_query": search_query})
    response = await client.responses.create(model="gpt-5.6-luna", tools=[{"type": "web_search_preview"}], input=search_query)
    text = response.output_text[:20000]
    audit("tool_result", tool="search_customer_candidates", result_summary=f"Returned {len(text)} characters of public search results")
    return text


@agent.tool
def inspect_customer_website(ctx: RunContext[SalesDeps], url: str) -> str:
    """Fetch one candidate website and extract visible text, links, and public emails."""
    parsed = urlparse(url)
    if parsed.scheme not in {"http", "https"}:
        raise ValueError("Candidate URL must be http or https.")
    audit("tool_call", tool="inspect_customer_website", args={"url": url})
    req = Request(url, headers={"User-Agent": "HomeworkSalesResearch/1.0"})
    try:
        with urlopen(req, timeout=15, context=ssl._create_unverified_context()) as response:
            raw = response.read(600_000).decode("utf-8", errors="replace")
    except Exception as exc:
        audit("tool_result", tool="inspect_customer_website", result_summary=f"Could not inspect {url}: {type(exc).__name__}")
        return json.dumps({"url": url, "error": type(exc).__name__, "public_emails": []})
    emails = sorted(set(re.findall(r"[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}", raw, re.I)))
    result = {"url": url, "text": _clean(raw), "public_emails": emails}
    audit("tool_result", tool="inspect_customer_website", result_summary=f"Inspected {url}; found {len(emails)} public email(s)")
    return json.dumps(result)


@agent.tool
def save_targets_and_emails(ctx: RunContext[SalesDeps], targets_json: str, emails_json: str) -> str:
    """Save target companies and unsent email drafts as separate valid JSON files."""
    targets, emails = json.loads(targets_json), json.loads(emails_json)
    if not isinstance(targets, list) or not isinstance(emails, list):
        raise ValueError("Targets and emails must both be JSON arrays.")
    for email in emails:
        if email.get("send_status") != "draft_only":
            raise ValueError("Every email must be marked draft_only.")
    TARGETS_FILE.parent.mkdir(exist_ok=True)
    TARGETS_FILE.write_text(json.dumps(targets, indent=2, ensure_ascii=False), encoding="utf-8")
    EMAILS_FILE.write_text(json.dumps(emails, indent=2, ensure_ascii=False), encoding="utf-8")
    audit("tool_result", tool="save_targets_and_emails", result_summary=f"Saved {len(targets)} targets and {len(emails)} unsent drafts")
    return f"Saved {len(targets)} targets to {TARGETS_FILE} and {len(emails)} draft-only emails to {EMAILS_FILE}."


async def run(query: str, url: str | None = None, profile_path: str | None = None) -> str:
    request_limit = 16 if profile_path else 8
    audit("run_start", query=query, url=url, profile_path=profile_path, model="gpt-5.6-luna", max_steps=request_limit)
    try:
        deps = SalesDeps(url or "https://invalid.local/")
        context = query + (f"\nResearch starting URL: {url}" if url else "") + (f"\nSeller profile path: {profile_path}" if profile_path else "")
        result = await agent.run(context, deps=deps,
                                 usage_limits=UsageLimits(request_limit=request_limit))
        audit("run_finish", status="completed", result_summary=result.output[:500])
        return result.output
    except Exception as exc:
        audit("run_finish", status="failed", error=type(exc).__name__, result_summary=str(exc)[:500])
        raise


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("query")
    parser.add_argument("--url")
    parser.add_argument("--profile")
    args = parser.parse_args()
    if not args.url and not args.profile:
        parser.error("provide --url for profile research or --profile for customer research")
    print(asyncio.run(run(args.query, args.url, args.profile)))
