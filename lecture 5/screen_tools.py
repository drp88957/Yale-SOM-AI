"""Screen capture helpers for the browser agent."""

from __future__ import annotations

import base64
import io
from datetime import datetime, timezone

import mss
from PIL import Image


def capture_screen() -> tuple[dict, bytes]:
    """Capture the primary monitor and return metadata plus PNG bytes."""
    with mss.mss() as sct:
        monitor = sct.monitors[1] if len(sct.monitors) > 1 else sct.monitors[0]
        shot = sct.grab(monitor)
        image = Image.frombytes("RGB", shot.size, shot.rgb)
        buffer = io.BytesIO()
        image.save(buffer, format="PNG")
    metadata = {"captured_at": datetime.now(timezone.utc).isoformat(), "region": "full"}
    return metadata, buffer.getvalue()


def png_data_url(png_bytes: bytes) -> str:
    return "data:image/png;base64," + base64.b64encode(png_bytes).decode("ascii")
