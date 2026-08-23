from __future__ import annotations

from pathlib import Path
from typing import Any

from film_director.utils.files import load_json, save_json


def load_workflow(path: Path) -> dict[str, Any]:
    return load_json(path)


def save_workflow(path: Path, workflow: dict[str, Any]) -> None:
    save_json(path, workflow)


def set_node_input(workflow: dict[str, Any], node_id: str, input_name: str, value: Any) -> None:
    key = str(node_id)
    if key not in workflow:
        raise KeyError(f"Node {node_id!r} not found in workflow")
    node = workflow[key]
    if "inputs" not in node or not isinstance(node["inputs"], dict):
        node["inputs"] = {}
    node["inputs"][input_name] = value
