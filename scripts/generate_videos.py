import argparse
from pathlib import Path

from film_director.comfyui.client import ComfyUIClient
from film_director.config import (
    COMFYUI_URL,
    COMFYUI_TIMEOUT,
    POLL_INTERVAL,
)
from film_director.render.videos import render_video


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument("project")

    parser.add_argument(
        "--model",
        choices=[
            "ltx-2.5",
            "minimax-h3",
        ],
    )

    args = parser.parse_args()

    root = Path(args.project)

    prompt_dir = (
        root / "prompts" / "videos"
    )

    output_dir = (
        root / "renders" / "videos"
    )

    client = ComfyUIClient(
        COMFYUI_URL,
        COMFYUI_TIMEOUT,
        POLL_INTERVAL,
    )

    for prompt_file in sorted(
        prompt_dir.glob("*.yaml")
    ):
        render_video(
            prompt_file=prompt_file,
            output_dir=output_dir,
            client=client,
            model_override=args.model,
        )

        print(
            f"generated video: "
            f"{prompt_file.stem}"
        )


if __name__ == "__main__":
    main()
