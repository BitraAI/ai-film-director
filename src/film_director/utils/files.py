from __future__ import annotations

import json
import tempfile
from pathlib import Path
from typing import Any

import yaml

from .jsonx import load_json as _load_json


def load_json(path: Path | str) -> Any:
    """Load JSON via robust jsonx helper (validates + better errors)."""
    return _load_json(path)


def save_json(path: Path | str, data: Any) -> None:
    """Save JSON atomically (temp file + rename) to avoid partial writes."""
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    # Use jsonx save but with atomic rename: write to temp then replace
    with tempfile.NamedTemporaryFile(
        mode="w", encoding="utf-8", dir=str(p.parent), delete=False, suffix=".tmp"
    ) as tmp:
        json.dump(data, tmp, indent=2, ensure_ascii=False)
        tmp.write("\n")
        tmp_path = Path(tmp.name)
    tmp_path.replace(p)


def load_yaml(path: Path | str) -> Any:
    p = Path(path)
    # Use read_text once, safe_load
    return yaml.safe_load(p.read_text(encoding="utf-8"))


def save_yaml(path: Path | str, data: Any) -> None:
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    text = yaml.safe_dump(data, sort_keys=False, allow_unicode=True)
    # atomic write
    with tempfile.NamedTemporaryFile(
        mode="w", encoding="utf-8", dir=str(p.parent), delete=False, suffix=".tmp"
    ) as tmp:
        tmp.write(text)
        tmp_path = Path(tmp.name)
    tmp_path.replace(p)
