from pathlib import Path

import requests
import yaml

from comfyui.adapters import prepare_workflow
from comfyui.client import ComfyUIClient
from config import COMFYUI_URL


def render_image(
    prompt_file: Path,
    output_dir: Path,
    client: ComfyUIClient,
    model_override: str | None = None,
):
    data = yaml.safe_load(
        prompt_file.read_text(encoding="utf-8")
    )

    model = model_override or data["model"]

    workflow = prepare_workflow(
        model=model,
        prompt=data["prompt"],
        negative_prompt=data.get("negative_prompt"),
        seed=data.get("seed"),
    )

    result = client.execute(workflow)

    output_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    # Save metadata YAML
    result_file = output_dir / f"{data['shot_id']}.yaml"
    result_file.write_text(
        yaml.safe_dump(
            result,
            sort_keys=False,
            allow_unicode=True,
        ),
        encoding="utf-8",
    )

    # Download final images to output_dir (renders/images), skip temp previews
    outputs = result.get("outputs", {}) if isinstance(result, dict) else {}
    if not outputs and isinstance(result, dict):
        for v in result.values():
            if isinstance(v, dict) and "outputs" in v:
                outputs = v.get("outputs", {})
                break
    for node_out in outputs.values():
        if not isinstance(node_out, dict):
            continue
        images = node_out.get("images")
        if not images:
            continue
        for idx, img in enumerate(images):
            if not isinstance(img, dict):
                continue
            filename = img.get("filename")
            subfolder = img.get("subfolder", "")
            img_type = img.get("type", "output")
            if not filename or img_type == "temp":
                continue
            params = {"filename": filename, "subfolder": subfolder, "type": img_type}
            try:
                resp = requests.get(f"{COMFYUI_URL}/view", params=params, timeout=30)
                resp.raise_for_status()
                ext = Path(filename).suffix or ".png"
                img_name = f"{data['shot_id']}{'_'+str(idx) if len(images) > 1 else ''}{ext}"
                (output_dir / img_name).write_bytes(resp.content)
            except Exception:
                continue

    return result
