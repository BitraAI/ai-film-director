import os
from pathlib import Path


COMFYUI_URL = os.getenv("COMFYUI_URL", "http://127.0.0.1:8188")
OUTPUT_ROOT = Path(os.getenv("OUTPUT_ROOT", "projects"))
COMFYUI_TIMEOUT = int(os.getenv("COMFYUI_TIMEOUT", "600"))
POLL_INTERVAL = float(os.getenv("POLL_INTERVAL", "1"))
FFMPEG_BIN = os.getenv("FFMPEG_BIN", "ffmpeg")
