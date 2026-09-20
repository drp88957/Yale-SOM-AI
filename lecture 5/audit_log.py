"""Optional JSON audit logging for agent turns."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path


def append_turn(user_text: str, result: dict) -> None:
    path = Path(__file__).resolve().parent / "output" / "audit_log.json"
    path.parent.mkdir(exist_ok=True)
    records = json.loads(path.read_text(encoding="utf-8")) if path.exists() else []
    records.append({"at": datetime.now(timezone.utc).isoformat(), "user": user_text, "tool_events": result.get("tool_events", [])})
    path.write_text(json.dumps(records, indent=2), encoding="utf-8")
