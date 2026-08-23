from pathlib import Path
from film_director.utils.files import load_json, save_json


def load_workflow(path: Path) -> dict:
    return load_json(path)


def save_workflow(path: Path, workflow: dict):
    save_json(path, workflow)


def set_node_input(workflow, node_id: str, input_name: str, value):
    node = workflow[str(node_id)]
    node["inputs"][input_name] = value


def get_node_input(workflow, node_id: str, input_name: str):
    return workflow[str(node_id)]["inputs"].get(input_name)
