import sys
from pathlib import Path
import yaml


def main():
    root = Path(sys.argv[1])

    checks = {
        "story": root / "story/story.yaml",
        "screenplay": root / "screenplay/screenplay.yaml",
        "characters": root / "characters/characters.yaml",
        "locations": root / "locations/locations.yaml",
        "props": root / "props/props.yaml",
        "storyboard": root / "storyboard/storyboard.yaml",
        "shots": root / "shots/shots.yaml",
        "image_prompts": root / "prompts/images",
        "video_prompts": root / "prompts/videos",
        "audio_prompts": root / "prompts/audio",
        "final": root / "final/film.mp4",
    }

    status = {
        name: path.exists()
        for name, path in checks.items()
    }

    manifest = {
        "project_id": root.name,
        "stages": status,
    }

    (root / "manifest.yaml").write_text(
        yaml.safe_dump(manifest, sort_keys=False),
        encoding="utf-8",
    )

    for name, value in status.items():
        print(f"{name:20} {'READY' if value else 'MISSING'}")


if __name__ == "__main__":
    main()
