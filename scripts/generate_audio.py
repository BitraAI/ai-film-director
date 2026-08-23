from pathlib import Path
import sys

from film_director.comfyui.client import ComfyUIClient
from film_director.config import (
    COMFYUI_URL,
    COMFYUI_TIMEOUT,
    POLL_INTERVAL,
)
from film_director.render.audio import render_audio


def main():
    if len(sys.argv) != 2:
        raise SystemExit(
            "Usage: "
            "python scripts/generate_audio.py "
            "<project>"
        )

    root = Path(sys.argv[1])

    prompt_dir = (
        root / "prompts" / "audio"
    )

    output_dir = root / "audio"

    client = ComfyUIClient(
        COMFYUI_URL,
        COMFYUI_TIMEOUT,
        POLL_INTERVAL,
    )

    for prompt_file in sorted(
        prompt_dir.glob("*.yaml")
    ):
        render_audio(
            prompt_file=prompt_file,
            output_dir=output_dir,
            client=client,
        )

        print(
            f"generated audio: "
            f"{prompt_file.stem}"
        )


if __name__ == "__main__":
    main()
