from __future__ import annotations

import os
from pathlib import Path

# Lightweight .env loader without external dependency — parses KEY=VALUE, skips comments.
def _load_dotenv(path: Path = Path(".env")) -> None:
    if not path.is_file():
        return
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, v = line.split("=", 1)
        k = k.strip()
        v = v.strip().strip('"').strip("'")
        if k and k not in os.environ:
            os.environ[k] = v


_load_dotenv()

COMFYUI_URL: str = os.getenv("COMFYUI_URL", "http://127.0.0.1:8188")
OUTPUT_ROOT: Path = Path(os.getenv("OUTPUT_ROOT", "projects"))
COMFYUI_TIMEOUT: int = int(os.getenv("COMFYUI_TIMEOUT", "600"))
POLL_INTERVAL: float = float(os.getenv("POLL_INTERVAL", "1"))
FFMPEG_BIN: str = os.getenv("FFMPEG_BIN", "ffmpeg")
