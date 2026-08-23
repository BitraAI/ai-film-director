from __future__ import annotations

import sys
from pathlib import Path

from film_director.manifest import build_manifest

import yaml


def main() -> None:
    if len(sys.argv) != 2:
        raise SystemExit("Usage: python scripts/build_manifest.py <project>")

    root = Path(sys.argv[1])
    manifest = build_manifest(root)

    (root / "manifest.yaml").write_text(
        yaml.safe_dump(manifest, sort_keys=False),
        encoding="utf-8",
    )

    for name, value in manifest["stages"].items():
        print(f"{name:20} {'READY' if value else 'MISSING'}")


if __name__ == "__main__":
    main()
