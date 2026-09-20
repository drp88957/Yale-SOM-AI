from __future__ import annotations

import base64
import json
import os
from pathlib import Path
from typing import Any, Callable

import imageio.v2 as imageio
from openai import OpenAI

from models import DunkVerdict, FoulVerdict

HERE = Path(__file__).resolve().parent
FRAMES = HERE / "frames"
ToolCallback = Callable[[str], None] | None


def _notify(cb: ToolCallback, name: str) -> None:
    if cb:
        cb(name)


def sample_frames(video_path: str, every_n_sec: float = 0.5, max_frames: int = 16, on_tool: ToolCallback = None) -> dict[str, Any]:
    _notify(on_tool, "sample_frames")
    path = Path(video_path).resolve()
    if not path.is_file():
        raise FileNotFoundError(path)
    out_dir = FRAMES / path.stem
    out_dir.mkdir(parents=True, exist_ok=True)
    reader = imageio.get_reader(str(path))
    meta = reader.get_meta_data()
    fps = float(meta.get("fps") or 30.0)
    step = max(1, round(fps * every_n_sec))
    paths: list[str] = []
    try:
        for index, frame in enumerate(reader):
            if index % step or len(paths) >= max_frames:
                continue
            target = out_dir / f"frame_{len(paths):03d}_t{index / fps:.2f}s.jpg"
            imageio.imwrite(str(target), frame, quality=90)
            paths.append(str(target.relative_to(HERE)).replace("\\", "/"))
            if len(paths) >= max_frames:
                break
    finally:
        reader.close()
    if not paths:
        raise RuntimeError(f"No frames could be read from {path}")
    return {"frame_paths": paths, "fps": fps, "frame_count": len(paths), "clip_label": path.name}


def _load_key() -> str:
    for env_path in (HERE / ".env", HERE.parent / ".env"):
        if env_path.exists():
            for line in env_path.read_text(encoding="utf-8").splitlines():
                if line.startswith("PORTKEY_API_KEY="):
                    return line.split("=", 1)[1].strip().strip('"\'')
    return os.getenv("PORTKEY_API_KEY", "")


def _vision_client() -> OpenAI:
    key = _load_key()
    if not key:
        raise RuntimeError("PORTKEY_API_KEY was not found in lecture 6/.env, the parent .env, or the environment")
    return OpenAI(api_key=key, base_url="https://api.portkey.ai/v1", default_headers={"x-portkey-api-key": key})


def _image_data(path: Path) -> str:
    encoded = base64.b64encode(path.read_bytes()).decode("ascii")
    return f"data:image/jpeg;base64,{encoded}"


def describe_video(frame_paths: list[str], clip_label: str, on_tool: ToolCallback = None) -> dict[str, Any]:
    _notify(on_tool, "describe_video")
    frames = [HERE / p for p in frame_paths]
    content: list[dict[str, Any]] = [{"type": "text", "text": "Describe this sports clip from the sampled frames. Return JSON with keys play_by_play, sport_guess (dunk|soccer|unclear), key_moments (list), and notes. Be conservative about what is visible."}]
    content += [{"type": "image_url", "image_url": {"url": _image_data(p)}} for p in frames if p.is_file()]
    response = _vision_client().chat.completions.create(model="gpt-5.6-luna", messages=[{"role": "user", "content": content}], response_format={"type": "json_object"})
    data = json.loads(response.choices[0].message.content or "{}")
    return {"play_by_play": str(data.get("play_by_play", "")), "sport_guess": data.get("sport_guess", "unclear"), "key_moments": data.get("key_moments", []), "notes": str(data.get("notes", ""))}


def _evidence(frame_paths: list[str], description: str) -> str:
    return "\n".join(f"{p}: {description}" for p in frame_paths)


def _as_text(value: Any) -> str:
    if isinstance(value, list):
        return " ".join(str(item) for item in value)
    if isinstance(value, dict):
        return json.dumps(value, ensure_ascii=False)
    return str(value or "")


def score_dunk(frame_paths: list[str], description: str, clip_label: str, on_tool: ToolCallback = None) -> DunkVerdict:
    _notify(on_tool, "score_dunk")
    prompt = f"Judge this dunk. Return JSON fields scores (height, creativity, difficulty, landing, each 0-10), total, play_by_play, rationale, frame_paths. Use only these evidence paths and include at least one decisive path.\nDescription: {description}\nEvidence paths:\n{_evidence(frame_paths, description)}"
    response = _vision_client().chat.completions.create(model="gpt-5.6-luna", messages=[{"role": "user", "content": prompt}], response_format={"type": "json_object"})
    data = json.loads(response.choices[0].message.content or "{}")
    data["play_by_play"] = _as_text(data.get("play_by_play"))
    data["rationale"] = _as_text(data.get("rationale"))
    data.update(kind="dunk", clip_label=clip_label, frame_paths=frame_paths)
    return DunkVerdict.model_validate(data)


def call_foul(frame_paths: list[str], description: str, clip_label: str, on_tool: ToolCallback = None) -> FoulVerdict:
    _notify(on_tool, "call_foul")
    prompt = f"Judge contact in this sports clip. Return JSON fields call (foul|flop|no_call), confidence as a calibrated probability from 0 to 1 (not a default 0.5), play_by_play, rationale, and frame_paths. Use only these evidence paths and include the frames that show the decisive contact or absence of contact.\nDescription: {description}\nEvidence paths:\n{_evidence(frame_paths, description)}"
    response = _vision_client().chat.completions.create(model="gpt-5.6-luna", messages=[{"role": "user", "content": prompt}], response_format={"type": "json_object"})
    data = json.loads(response.choices[0].message.content or "{}")
    data["play_by_play"] = _as_text(data.get("play_by_play"))
    data["rationale"] = _as_text(data.get("rationale"))
    data.update(kind="foul", clip_label=clip_label, frame_paths=frame_paths)
    return FoulVerdict.model_validate(data)
