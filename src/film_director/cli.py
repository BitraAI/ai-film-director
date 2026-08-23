import argparse
from pathlib import Path

from .manifest import save_manifest
from .pipeline.director import FilmDirector


def main():
    parser = argparse.ArgumentParser(
        prog="film-director"
    )

    sub = parser.add_subparsers(dest="command", required=True)

    status = sub.add_parser("status")
    status.add_argument("project")

    manifest = sub.add_parser("manifest")
    manifest.add_argument("project")

    args = parser.parse_args()

    root = Path(args.project)

    if args.command == "status":
        director = FilmDirector(root)

        for stage, value in director.status().items():
            print(
                f"{stage:15} "
                f"{'READY' if value else 'MISSING'}"
            )

        print(f"\nnext: {director.next_stage()}")

    elif args.command == "manifest":
        print(save_manifest(root))


if __name__ == "__main__":
    main()
