from __future__ import annotations

from pathlib import Path

import yaml


def _dir_has_files(path: Path, pattern: str = "*.yaml") -> bool:
    return path.is_dir() and any(path.glob(pattern))


def build_manifest(root: Path) -> dict:
    root = Path(root)
    stages = {
        "story": (root / "story" / "story.yaml").is_file(),
        "screenplay": (root / "screenplay" / "screenplay.yaml").is_file(),
        "characters": (root / "characters" / "characters.yaml").is_file(),
        "locations": (root / "locations" / "locations.yaml").is_file(),
        "props": (root / "props" / "props.yaml").is_file(),
        "storyboard": (root / "storyboard" / "storyboard.yaml").is_file(),
        "shots": (root / "shots" / "shots.yaml").is_file(),
        "image_prompts": _dir_has_files(root / "prompts" / "images"),
        "video_prompts": _dir_has_files(root / "prompts" / "videos"),
        "audio_prompts": _dir_has_files(root / "prompts" / "audio"),
        "final": (root / "final" / "film.mp4").is_file(),
    }
    return {"project_id": root.name, "stages": stages}


def save_manifest(root: Path) -> dict:
    root = Path(root)
    manifest = build_manifest(root)
    (root / "manifest.yaml").write_text(
        yaml.safe_dump(manifest, sort_keys=False),
        encoding="utf-8",
    )
    return manifest
