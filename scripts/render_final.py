import sys
from pathlib import Path

from film_director.render.final import render_final


def main():
    if len(sys.argv) != 2:
        raise SystemExit(
            "Usage: "
            "python scripts/render_final.py "
            "<project>"
        )

    project_root = Path(sys.argv[1])

    output = render_final(
        project_root
    )

    print(
        f"final film: {output}"
    )


if __name__ == "__main__":
    main()
