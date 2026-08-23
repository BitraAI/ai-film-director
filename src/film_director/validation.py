from pathlib import Path
import jsonschema
import yaml


def validate_file(data_file: Path, schema_file: Path):
    data = yaml.safe_load(data_file.read_text(encoding="utf-8"))
    schema = yaml.safe_load(schema_file.read_text(encoding="utf-8"))
    jsonschema.validate(data, schema)
    return True
