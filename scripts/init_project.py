import sys
from pathlib import Path
import yaml

from film_director.paths import create_project_tree


def main():
    if len(sys.argv) != 2:
        print("Usage: python scripts/init_project.py <project>")
        raise SystemExit(1)

    name = sys.argv[1]
    root = Path("projects") / name

    create_project_tree(root)

    project = {
        "project_id": name,
        "title": name.replace("-", " ").title(),
        "genre": "",
        "aspect_ratio": "16:9",
        "fps": 24,
        "duration_seconds": 0,
    }

    (root / "project.yaml").write_text(
        yaml.safe_dump(project, sort_keys=False),
        encoding="utf-8",
    )

    print(root)


if __name__ == "__main__":
    main()
