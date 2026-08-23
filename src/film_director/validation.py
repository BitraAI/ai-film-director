from __future__ import annotations

from functools import lru_cache
from pathlib import Path

import jsonschema
import yaml


@lru_cache(maxsize=None)
def _load_schema_cached(schema_str: str) -> dict:
    return yaml.safe_load(Path(schema_str).read_text(encoding="utf-8"))


def validate_file(data_file: Path, schema_file: Path) -> bool:
    data = yaml.safe_load(data_file.read_text(encoding="utf-8"))
    schema = _load_schema_cached(str(schema_file))
    jsonschema.validate(data, schema)
    return True
