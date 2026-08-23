import sys
from pathlib import Path

from film_director.validation import validate_file


STAGES = {
    "story/story.yaml": "schemas/story.schema.yaml",
    "screenplay/screenplay.yaml": "schemas/screenplay.schema.yaml",
    "characters/characters.yaml": "schemas/character.schema.yaml",
    "locations/locations.yaml": "schemas/location.schema.yaml",
    "props/props.yaml": "schemas/prop.schema.yaml",
    "storyboard/storyboard.yaml": "schemas/storyboard.schema.yaml",
    "shots/shots.yaml": "schemas/shot.schema.yaml",
}


def main():
    if len(sys.argv) != 2:
        raise SystemExit(
            "Usage: python scripts/validate_project.py <project>"
        )

    root = Path(sys.argv[1])
    failures = []

    for data, schema in STAGES.items():
        data_path = root / data

        if not data_path.exists():
            continue

        try:
            validate_file(
                data_path,
                Path(schema),
            )
            print(f"OK  {data}")
        except Exception as exc:
            failures.append((data, str(exc)))
            print(f"FAIL {data}: {exc}")

    if failures:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
