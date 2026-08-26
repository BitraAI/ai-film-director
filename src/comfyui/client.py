from __future__ import annotations

import json
import time
import uuid
import random
from pathlib import Path
from typing import Any

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


class ComfyUIClient:
    """HTTP client for ComfyUI with pooling, retries and adaptive polling.

    - Reuses a ``requests.Session`` with keep-alive / connection pooling.
    - Uses ``time.monotonic`` for timeout correctness.
    - Polls ``/history`` with exponential backoff + jitter to reduce
      server load while staying responsive for fast jobs.
    - Retries transient HTTP errors (429, 5xx) on queue/history.
    """

    def __init__(
        self,
        base_url: str,
        timeout: int = 600,
        poll_interval: float = 1.0,
        *,
        max_retries: int = 3,
        backoff_factor: float = 0.5,
    ):
        self.base_url = base_url.rstrip("/")
        self.timeout = float(timeout)
        self.poll_interval = float(poll_interval)
        self.client_id = str(uuid.uuid4())
        self.session = requests.Session()
        # Retry on transient errors; respect Retry-After for 429.
        retry = Retry(
            total=max_retries,
            backoff_factor=backoff_factor,
            status_forcelist=(429, 500, 502, 503, 504),
            allowed_methods=("GET", "POST"),
            raise_on_status=False,
        )
        adapter = HTTPAdapter(max_retries=retry, pool_connections=10, pool_maxsize=10)
        self.session.mount("http://", adapter)
        self.session.mount("https://", adapter)

    def close(self) -> None:
        self.session.close()

    def __enter__(self) -> ComfyUIClient:
        return self

    def __exit__(self, *_) -> None:
        self.close()

    # -- low-level API -------------------------------------------------

    def queue(self, workflow: dict[str, Any]) -> dict[str, Any]:
        response = self.session.post(
            f"{self.base_url}/prompt",
            json={"prompt": workflow, "client_id": self.client_id},
            timeout=30,
        )
        response.raise_for_status()
        return response.json()

    def history(self, prompt_id: str) -> dict[str, Any]:
        response = self.session.get(
            f"{self.base_url}/history/{prompt_id}",
            timeout=30,
        )
        response.raise_for_status()
        return response.json()

    def wait(self, prompt_id: str) -> dict[str, Any]:
        start = time.monotonic()
        attempt = 0
        # adaptive poll: start at poll_interval, backoff to max 5s
        interval = self.poll_interval
        max_interval = 5.0

        while time.monotonic() - start < self.timeout:
            try:
                history = self.history(prompt_id)
            except requests.RequestException:
                # Transient failure — backoff and retry without counting as stage error
                # Retry already handled by HTTPAdapter, this is for network edge cases.
                if time.monotonic() - start >= self.timeout:
                    break
                sleep = min(interval * (1.5**attempt) + random.uniform(0, 0.3), max_interval)
                time.sleep(sleep)
                attempt = min(attempt + 1, 6)
                continue

            if prompt_id in history:
                result = history[prompt_id]
                status = result.get("status", {})
                if status.get("completed"):
                    return result
                if status.get("status_str") == "error":
                    raise RuntimeError(json.dumps(result, indent=2))

            # exponential backoff with jitter, capped
            sleep = min(interval + random.uniform(0, 0.25), max_interval)
            # gradually increase interval if job is long-running
            interval = min(interval * 1.15, max_interval)
            time.sleep(sleep)

        raise TimeoutError(f"ComfyUI timeout after {self.timeout}s: {prompt_id}")

    def upload_image(self, image_path: Path) -> str:
        """Upload an image to ComfyUI input directory and return server filename."""
        p = Path(image_path)
        if not p.is_file():
            raise FileNotFoundError(f"Image not found: {p}")
        # Determine mime
        suffix = p.suffix.lower()
        mime = {
            ".png": "image/png",
            ".jpg": "image/jpeg",
            ".jpeg": "image/jpeg",
            ".webp": "image/webp",
        }.get(suffix, "image/png")
        with p.open("rb") as f:
            files = {"image": (p.name, f, mime)}
            data = {"overwrite": "true"}
            resp = self.session.post(
                f"{self.base_url}/upload/image",
                files=files,
                data=data,
                timeout=30,
            )
            resp.raise_for_status()
            j = resp.json()
            # ComfyUI returns {"name": "filename.png", "subfolder": "", "type": "input"}
            return j.get("name") or p.name

    def execute(self, workflow: dict[str, Any]) -> dict[str, Any]:
        queued = self.queue(workflow)
        prompt_id = queued["prompt_id"]
        return self.wait(prompt_id)
