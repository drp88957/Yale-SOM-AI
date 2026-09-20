from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field


class DunkVerdict(BaseModel):
    kind: Literal["dunk"] = "dunk"
    clip_label: str
    scores: dict[str, float] = Field(description="height, creativity, difficulty, and landing scores from 0 to 10")
    total: float
    play_by_play: str
    rationale: str
    frame_paths: list[str] = Field(min_length=1)


class FoulVerdict(BaseModel):
    kind: Literal["foul"] = "foul"
    clip_label: str
    call: Literal["foul", "flop", "no_call"]
    confidence: float = Field(ge=0, le=1)
    play_by_play: str
    rationale: str
    frame_paths: list[str] = Field(min_length=1)
