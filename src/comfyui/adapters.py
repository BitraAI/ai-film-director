from pathlib import Path

from .workflow import load_workflow, set_node_input


WORKFLOW_ROOT = Path("workflows")


ADAPTERS = {
    "krea2": {
        "workflow": WORKFLOW_ROOT / "image" / "krea2.json",
        "prompt_node": None,
        "prompt_input": "text",
        "negative_node": None,
        "negative_input": "text",
        "seed_node": None,
        "seed_input": "seed",
    },
    "flux2-klein": {
        "workflow": WORKFLOW_ROOT / "image" / "flux2-klein.json",
        "prompt_node": None,
        "prompt_input": "text",
        "negative_node": None,
        "negative_input": "text",
        "seed_node": None,
        "seed_input": "seed",
    },
    "qwen-image": {
        "workflow": WORKFLOW_ROOT / "image" / "qwen-image.json",
        "prompt_node": None,
        "prompt_input": "prompt",
        "negative_node": None,
        "negative_input": "negative_prompt",
        "seed_node": None,
        "seed_input": "seed",
    },
    "ltx-2.5": {
        "workflow": WORKFLOW_ROOT / "video" / "ltx-2.5.json",
        "prompt_node": None,
        "prompt_input": "prompt",
        "seed_node": None,
        "seed_input": "seed",
    },
    "minimax-h3": {
        "workflow": WORKFLOW_ROOT / "video" / "minimax-h3.json",
        "prompt_node": None,
        "prompt_input": "prompt",
        "seed_node": None,
        "seed_input": "seed",
    },
    "qwen3-tts": {
        "workflow": WORKFLOW_ROOT / "audio" / "qwen3-tts.json",
        "prompt_node": None,
        "prompt_input": "text",
    },
}


def prepare_workflow(model: str, prompt: str, negative_prompt=None, seed=None):
    config = ADAPTERS[model]

    workflow = load_workflow(config["workflow"])

    if config.get("prompt_node") is not None:
        set_node_input(
            workflow,
            config["prompt_node"],
            config["prompt_input"],
            prompt,
        )

    if (
        negative_prompt is not None
        and config.get("negative_node") is not None
    ):
        set_node_input(
            workflow,
            config["negative_node"],
            config["negative_input"],
            negative_prompt,
        )

    if seed is not None and config.get("seed_node") is not None:
        set_node_input(
            workflow,
            config["seed_node"],
            config["seed_input"],
            seed,
        )

    return workflow
