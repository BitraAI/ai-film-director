from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def load_json(
    path: str | Path,
) -> dict[str, Any]:
    """
    Load a JSON file and return its parsed object.
    """
    file_path = Path(path)

    if not file_path.exists():
        raise FileNotFoundError(
            f"JSON file not found: {file_path}"
        )

    if not file_path.is_file():
        raise IsADirectoryError(
            f"Expected JSON file, got directory: {file_path}"
        )

    try:
        return json.loads(
            file_path.read_text(
                encoding="utf-8"
            )
        )
    except json.JSONDecodeError as exc:
        raise ValueError(
            f"Invalid JSON in {file_path}: "
            f"line {exc.lineno}, "
            f"column {exc.colno}: "
            f"{exc.msg}"
        ) from exc


def save_json(
    path: str | Path,
    data: Any,
    *,
    indent: int = 2,
    ensure_ascii: bool = False,
):
    """
    Save an object as formatted JSON.
    """
    file_path = Path(path)

    file_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    file_path.write_text(
        json.dumps(
            data,
            indent=indent,
            ensure_ascii=ensure_ascii,
        ) + "\n",
        encoding="utf-8",
    )


def load_json_text(
    text: str,
) -> Any:
    """
    Parse JSON directly from a string.
    """
    try:
        return json.loads(text)
    except json.JSONDecodeError as exc:
        raise ValueError(
            f"Invalid JSON text: "
            f"line {exc.lineno}, "
            f"column {exc.colno}: "
            f"{exc.msg}"
        ) from exc


def save_json_text(
    data: Any,
    *,
    indent: int = 2,
    ensure_ascii: bool = False,
) -> str:
    """
    Serialize an object to formatted JSON text.
    """
    return (
        json.dumps(
            data,
            indent=indent,
            ensure_ascii=ensure_ascii,
        )
        + "\n"
    )


def deep_copy_json(
    data: Any,
) -> Any:
    """
    Create a JSON-compatible deep copy.
    """
    return json.loads(
        json.dumps(
            data,
            ensure_ascii=False,
        )
    )


def get_path(
    data: Any,
    *keys: str | int,
    default: Any = None,
) -> Any:
    """
    Safely retrieve a nested JSON value.

    Example:
        get_path(workflow, "node", "inputs", "text")
    """
    current = data

    for key in keys:
        try:
            if isinstance(current, dict):
                current = current[key]
            elif isinstance(current, list):
                current = current[key]
            else:
                return default
        except (
            KeyError,
            IndexError,
            TypeError,
        ):
            return default

    return current


def set_path(
    data: dict,
    keys: list[str | int],
    value: Any,
):
    """
    Set a nested value inside a JSON-compatible dictionary.

    Example:
        set_path(
            workflow,
            ["12", "inputs", "text"],
            "cinematic prompt",
        )
    """
    if not keys:
        raise ValueError(
            "keys cannot be empty"
        )

    current = data

    for key in keys[:-1]:
        if key not in current:
            current[key] = {}

        current = current[key]

    current[keys[-1]] = value

    return data
