from pathlib import Path

import yaml

from film_director.comfyui.adapters import prepare_workflow
from film_director.comfyui.client import ComfyUIClient


def render_audio(
    prompt_file: Path,
    output_dir: Path,
    client: ComfyUIClient,
):
    data = yaml.safe_load(
        prompt_file.read_text(encoding="utf-8")
    )

    prompt = (
        f"Speaker: {data['speaker_id']}\n"
        f"Text: {data['text']}\n"
        f"Voice: {data.get('voice', '')}\n"
        f"Emotion: {data.get('emotion', '')}\n"
        f"Tone: {data.get('tone', '')}\n"
        f"Pace: {data.get('pace', '')}\n"
        f"Pitch: {data.get('pitch', '')}\n"
        f"Energy: {data.get('energy', '')}"
    )

    workflow = prepare_workflow(
        model="qwen3-tts",
        prompt=prompt,
    )

    result = client.execute(workflow)

    output_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    result_file = output_dir / f"{data['prompt_id']}.yaml"

    result_file.write_text(
        yaml.safe_dump(
            result,
            sort_keys=False,
            allow_unicode=True,
        ),
        encoding="utf-8",
    )

    return result
