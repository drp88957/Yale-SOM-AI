"""PydanticAI screen-aware agent backed by OpenAI through Portkey."""

from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv
from openai import AsyncOpenAI
from pydantic_ai import Agent, BinaryContent, RunContext
from pydantic_ai.models.openai import OpenAIChatModel
from pydantic_ai.providers.openai import OpenAIProvider

from screen_tools import capture_screen

ROOT = Path(__file__).resolve().parent
load_dotenv(ROOT.parent / ".env")

if not os.getenv("PORTKEY_API_KEY"):
    raise RuntimeError("PORTKEY_API_KEY is missing from the project .env file")

SYSTEM_PROMPT = (ROOT / "prompts" / "prompt.md").read_text(encoding="utf-8")

_portkey_client = AsyncOpenAI(
    api_key=os.environ["PORTKEY_API_KEY"],
    base_url="https://api.portkey.ai/v1",
    default_headers={"x-portkey-api-key": os.environ["PORTKEY_API_KEY"]},
)
_model = OpenAIChatModel("gpt-5.6-luna", provider=OpenAIProvider(openai_client=_portkey_client))

agent = Agent(
    _model,
    output_type=str,
    system_prompt=SYSTEM_PROMPT,
)


@agent.tool
def look_at_screen(ctx: RunContext) -> str:
    """Capture the visible desktop so the agent can answer visual questions."""
    metadata, png = capture_screen()
    ctx.deps["last_shot"] = metadata
    ctx.deps["screenshot"] = png
    return "Screenshot captured. The screenshot is attached to this tool result; inspect it before answering."


def run_agent(user_text: str) -> dict:
    metadata, png = capture_screen()
    deps: dict = {"last_shot": metadata, "screenshot": png}
    prompt = [user_text, BinaryContent(data=png, media_type="image/png")]
    result = agent.run_sync(prompt, deps=deps)
    tool_events = [{"name": "Look at screen"}]
    return {"text": result.output, "tool_events": tool_events, "last_shot": deps.get("last_shot")}
