from pathlib import Path
import yaml


def build_manifest(root: Path):
    files = {
        "story": root / "story/story.yaml",
        "screenplay": root / "screenplay/screenplay.yaml",
        "characters": root / "characters/characters.yaml",
        "locations": root / "world/locations.yaml",
        "props": root / "world/props.yaml",
        "storyboard": root / "storyboard/storyboard.yaml",
        "shots": root / "shots/shots.yaml",
        "image_prompts": root / "prompts/images",
        "video_prompts": root / "prompts/videos",
        "audio_prompts": root / "prompts/audio",
        "final": root / "final/film.mp4",
    }

    return {
        "project_id": root.name,
        "stages": {
            key: value.exists()
            for key, value in files.items()
        },
    }


def save_manifest(root: Path):
    manifest = build_manifest(root)

    (root / "manifest.yaml").write_text(
        yaml.safe_dump(manifest, sort_keys=False),
        encoding="utf-8",
    )

    return manifest
