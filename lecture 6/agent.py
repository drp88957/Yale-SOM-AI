from __future__ import annotations

import os
from pathlib import Path
from typing import Any, Callable

from dotenv import load_dotenv
from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIChatModel
from pydantic_ai.providers.openai import OpenAIProvider
from openai import AsyncOpenAI

from models import DunkVerdict, FoulVerdict
from video_tools import call_foul, describe_video, sample_frames, score_dunk

HERE = Path(__file__).resolve().parent
load_dotenv(HERE / ".env")
load_dotenv(HERE.parent / ".env")

Result = DunkVerdict | FoulVerdict


def _model() -> OpenAIChatModel:
    key = os.getenv("PORTKEY_API_KEY")
    if not key:
        raise RuntimeError("PORTKEY_API_KEY is missing from lecture 6/.env or the parent .env")
    client = AsyncOpenAI(api_key=key, base_url="https://api.portkey.ai/v1", default_headers={"x-portkey-api-key": key})
    return OpenAIChatModel("gpt-5.6-luna", provider=OpenAIProvider(openai_client=client))


def run_agent(video_path: str, on_tool: Callable[[str], None] | None = None) -> dict[str, Any]:
    events: list[dict[str, str]] = []
    callback = on_tool

    def notify(name: str) -> None:
        events.append({"name": name})
        if callback:
            callback(name)

    agent = Agent(_model(), output_type=Result, system_prompt=(HERE / "prompts" / "prompt.md").read_text(encoding="utf-8"))

    @agent.tool_plain
    def sample_frames_tool(every_n_sec: float = 0.5, max_frames: int = 16) -> dict[str, Any]:
        return sample_frames(video_path, every_n_sec, max_frames, notify)

    @agent.tool_plain
    def describe_video_tool(frame_paths: list[str], clip_label: str) -> dict[str, Any]:
        return describe_video(frame_paths, clip_label, notify)

    @agent.tool_plain
    def score_dunk_tool(frame_paths: list[str], description: str, clip_label: str) -> DunkVerdict:
        return score_dunk(frame_paths, description, clip_label, notify)

    @agent.tool_plain
    def call_foul_tool(frame_paths: list[str], description: str, clip_label: str) -> FoulVerdict:
        return call_foul(frame_paths, description, clip_label, notify)

    result = agent.run_sync(
        f"Judge the sports video at {video_path}. Always sample it first, describe the sampled frames, then call exactly one final judging tool. Return its structured verdict."
    )
    return {"verdict": result.output, "tool_events": events}
