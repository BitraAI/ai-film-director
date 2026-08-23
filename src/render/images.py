from pathlib import Path

import yaml

from film_director.comfyui.adapters import prepare_workflow
from film_director.comfyui.client import ComfyUIClient


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

    result_file = output_dir / f"{data['shot_id']}.yaml"

    result_file.write_text(
        yaml.safe_dump(
            result,
            sort_keys=False,
            allow_unicode=True,
        ),
        encoding="utf-8",
    )

    return result
