from pathlib import Path


def project_paths(root: Path) -> dict[str, Path]:
    return {
        "story": root / "story",
        "screenplay": root / "screenplay",
        "characters": root / "characters",
        "sheets": root / "characters" / "sheets",
        "world": root / "world",
        "storyboard": root / "storyboard",
        "shots": root / "shots",
        "image_prompts": root / "prompts" / "images",
        "video_prompts": root / "prompts" / "videos",
        "audio_prompts": root / "prompts" / "audio",
        "image_renders": root / "renders" / "images",
        "video_renders": root / "renders" / "videos",
        "audio": root / "audio",
        "final": root / "final",
    }


def create_project_tree(root: Path):
    for path in project_paths(root).values():
        path.mkdir(parents=True, exist_ok=True)
