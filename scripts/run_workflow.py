import argparse
from pathlib import Path

import yaml

from comfyui.client import ComfyUIClient
from comfyui.adapters import prepare_workflow
from config import (
    COMFYUI_URL,
    COMFYUI_TIMEOUT,
    POLL_INTERVAL,
)


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument("model")
    parser.add_argument("prompt")

    parser.add_argument("--negative", default=None)
    parser.add_argument("--seed", type=int, default=None)
    parser.add_argument("--output", type=Path, default=None)

    args = parser.parse_args()

    workflow = prepare_workflow(
        args.model,
        args.prompt,
        args.negative,
        args.seed,
    )

    client = ComfyUIClient(
        COMFYUI_URL,
        COMFYUI_TIMEOUT,
        POLL_INTERVAL,
    )

    result = client.execute(workflow)

    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(
            yaml.safe_dump(result, sort_keys=False),
            encoding="utf-8",
        )

    print(result)


if __name__ == "__main__":
    main()
