import argparse
from pathlib import Path

from film_director.comfyui.client import ComfyUIClient
from film_director.config import (
    COMFYUI_URL,
    COMFYUI_TIMEOUT,
    POLL_INTERVAL,
)
from film_director.render.images import render_image


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument("project")

    parser.add_argument(
        "--model",
        choices=[
            "krea2",
            "flux2-klein",
            "qwen-image",
        ],
    )

    args = parser.parse_args()

    root = Path(args.project)

    prompt_dir = (
        root / "prompts" / "images"
    )

    output_dir = (
        root / "renders" / "images"
    )

    client = ComfyUIClient(
        COMFYUI_URL,
        COMFYUI_TIMEOUT,
        POLL_INTERVAL,
    )

    for prompt_file in sorted(
        prompt_dir.glob("*.yaml")
    ):
        render_image(
            prompt_file=prompt_file,
            output_dir=output_dir,
            client=client,
            model_override=args.model,
        )

        print(
            f"generated image: "
            f"{prompt_file.stem}"
        )


if __name__ == "__main__":
    main()
