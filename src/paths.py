from pathlib import Path


def project_paths(root: Path) -> dict[str, Path]:
    return {
        "story": root / "story",
        "screenplay": root / "screenplay",
        "characters": root / "characters",
        "sheets": root / "characters" / "sheets",
        "locations": root / "locations",
        "props": root / "props",
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
    # model-specific subfolders for image prompts (krea2, flux2-klein, qwen-image)
    for model in ["krea2", "flux2-klein", "qwen-image"]:
        (root / "prompts" / "images" / model).mkdir(parents=True, exist_ok=True)
    # model-specific subfolders for video prompts (ltx-2.5, minimax-h3)
    for model in ["ltx-2.5", "minimax-h3"]:
        (root / "prompts" / "videos" / model).mkdir(parents=True, exist_ok=True)
