from pathlib import Path

import yaml
import requests

from comfyui.adapters import prepare_workflow
from comfyui.client import ComfyUIClient
from config import COMFYUI_URL


def _resolve_image_for_shot(prompt_file: Path, shot_id: str) -> Path | None:
    """Resolve image input for a shot from renders/images only.

    Projects no longer use project_root/images; all images are under
    renders/images. We also check legacy locations for backward compat
    but do not create `images/` anymore.
    """
    try:
        project_root = prompt_file.parents[3]
    except IndexError:
        project_root = Path.cwd()
    # Primary location
    base = project_root / "renders" / "images"
    for ext in [".png", ".jpg", ".jpeg", ".webp"]:
        p = base / f"{shot_id}{ext}"
        if p.is_file():
            return p
    if base.is_dir():
        for p in base.glob(f"{shot_id}*.*"):
            if p.suffix.lower() in {".png", ".jpg", ".jpeg", ".webp"} and p.is_file():
                return p
    # Recursive search under renders/images
    if base.is_dir():
        for p in base.rglob(f"{shot_id}*.*"):
            if p.suffix.lower() in {".png", ".jpg", ".jpeg", ".webp"}:
                return p
    return None


def _extract_outputs(result: dict) -> dict:
    """Extract ComfyUI outputs dict from history result."""
    if not isinstance(result, dict):
        return {}
    if "outputs" in result:
        return result.get("outputs", {})
    # history is {prompt_id: {"outputs": {...}, "status": ...}}
    for v in result.values():
        if isinstance(v, dict) and "outputs" in v:
            return v.get("outputs", {})
    return {}


def render_video(
    prompt_file: Path,
    output_dir: Path,
    client: ComfyUIClient,
    model_override: str | None = None,
):
    data = yaml.safe_load(
        prompt_file.read_text(encoding="utf-8")
    )

    model = model_override or data["model"]
    shot_id = data.get("shot_id") or data.get("prompt_id") or prompt_file.stem
    prompt_text = data.get("prompt", "")
    duration = data.get("duration")
    fps = data.get("fps")

    # Resolve image from images folder for I2V
    image_filename: str | None = None
    image_path = _resolve_image_for_shot(prompt_file, shot_id)
    if image_path is not None and image_path.is_file():
        try:
            image_filename = client.upload_image(image_path)
        except Exception as e:
            # Fallback: keep local filename if upload fails (e.g., mocked client)
            # Log but continue as T2V
            print(f"[render_video] warning: upload failed for {image_path}: {e}")
            image_filename = image_path.name
    else:
        if model == "ltx-2.5":
            print(f"[render_video] warning: no image found for {shot_id} in renders/images/ - falling back to T2V")

    workflow = prepare_workflow(
        model=model,
        prompt=prompt_text,
        image_filename=image_filename,
        duration=duration,
        fps=fps,
        shot_id=shot_id,
    )

    result = client.execute(workflow)

    output_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    result_file = output_dir / f"{shot_id}.yaml"

    result_file.write_text(
        yaml.safe_dump(
            result,
            sort_keys=False,
            allow_unicode=True,
        ),
        encoding="utf-8",
    )

    # Try to download generated video(s) to project videos folder
    try:
        # project_root derived as before
        try:
            project_root = prompt_file.parents[3]
        except IndexError:
            project_root = Path.cwd()
        # Prefer project_root / "videos" if user expects, but also ensure output_dir sibling?
        # Spec says images folder, so videos likely in renders/videos or project/videos?
        # Save to output_dir (renders/videos) plus optional project_root/videos
        video_dirs = [output_dir]
        # Also ensure legacy location project_root / "videos" if requested via issue
        # but keep main output in renders/videos as configured
        outputs = _extract_outputs(result)
        for node_id, node_out in outputs.items():
            if not isinstance(node_out, dict):
                continue
            # videos may be under "gifs", "videos", "images", "mp4s"
            for key in ("gifs", "videos", "images", "mp4s"):
                items = node_out.get(key)
                if not items:
                    continue
                for idx, item in enumerate(items):
                    if not isinstance(item, dict):
                        continue
                    filename = item.get("filename")
                    subfolder = item.get("subfolder", "")
                    filetype = item.get("type", "output")
                    if not filename:
                        continue
                    # Do not download temp previews
                    if filetype == "temp":
                        continue
                    params = {
                        "filename": filename,
                        "subfolder": subfolder,
                        "type": filetype,
                    }
                    try:
                        resp = requests.get(f"{COMFYUI_URL}/view", params=params, timeout=60)
                        resp.raise_for_status()
                        ext = Path(filename).suffix or ".mp4"
                        # name as shot_id.mp4
                        vname = f"{shot_id}{'_'+str(idx) if len(items)>1 else ''}{ext}"
                        for vdir in video_dirs:
                            vdir.mkdir(parents=True, exist_ok=True)
                            (vdir / vname).write_bytes(resp.content)
                        # also try to save to project_root/videos if exists as alternative
                        alt = project_root / "videos"
                        if alt != output_dir and alt.parent.exists():
                            pass
                    except Exception:
                        continue
    except Exception:
        pass

    return result
