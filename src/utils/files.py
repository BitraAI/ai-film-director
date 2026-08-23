import json
from pathlib import Path
import yaml


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def save_json(path: Path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(data, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )


def load_yaml(path: Path):
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def save_yaml(path: Path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        yaml.safe_dump(
            data,
            sort_keys=False,
            allow_unicode=True,
        ),
        encoding="utf-8",
    )
