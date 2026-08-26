from __future__ import annotations

import copy
from functools import lru_cache
from pathlib import Path

from .workflow import load_workflow, set_node_input
import json as _json


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
        "prompt_node": "75:171",
        "prompt_input": "prompt",
        "negative_node": "75:172",
        "negative_input": "text",
        "seed_node": "75:73",
        "seed_input": "noise_seed",
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


def _resolve_workflow_path(path: Path) -> Path:
    """Resolve workflow path with fallbacks for dot/underscore and case variants.

    Handles historical mismatches like ltx-2.5.json vs ltx-2_5.json and
    Flux.2_Klein.json vs flux2-klein.json.
    """
    if path.exists():
        return path
    # Try dot <-> underscore swaps in filename
    candidates = [
        path.with_name(path.name.replace(".", "_")),
        path.with_name(path.name.replace("_", ".")),
        path.with_name(path.name.replace(".", "_").lower()),
        path.with_name(path.name.replace("_", ".").lower()),
    ]
    # Specific known aliases
    aliases = {
        "ltx-2.5.json": ["ltx-2_5.json", "ltx-2_5.JSON"],
        "flux2-klein.json": ["Flux.2_Klein.json", "flux.2_klein.json"],
    }
    for alt in aliases.get(path.name, []):
        candidates.append(path.with_name(alt))
        candidates.append(path.with_name(alt.lower()))

    for cand in candidates:
        if cand.exists():
            return cand

    # Case-insensitive directory scan as last resort
    if path.parent.exists():
        lower_name = path.name.lower()
        for p in path.parent.iterdir():
            if p.name.lower() == lower_name:
                return p
            # also try normalized (dots/underscores equivalent)
            if p.name.lower().replace(".", "_") == lower_name.replace(".", "_"):
                return p
    return path  # let load_workflow raise proper FileNotFoundError


@lru_cache(maxsize=None)
def _load_cached_workflow(path_str: str) -> dict:
    """Cache raw workflow JSON by path to avoid repeated disk I/O."""
    resolved = _resolve_workflow_path(Path(path_str))
    return load_workflow(resolved)


def _patch_ltx_workflow(
    workflow: dict,
    prompt: str | None = None,
    image_filename: str | None = None,
    duration: float | None = None,
    fps: int | float | None = None,
    shot_id: str | None = None,
) -> None:
    """Patch LTX-2.5 workflow for I2V + prompt/duration.

    - Injects prompt into LTXDirectorCS25 timeline_data.global_prompt and
      local_prompts.
    - Creates/updates LoadImage node for image-to-video.
    - Syncs duration/fps/frames (LTX requires frames %8==1).
    - Leaves workflow valid if no patch needed.
    """
    # Node 220 is the canonical LTXDirectorCS25 in this export.
    director_id = "220" if "220" in workflow else None
    if director_id is None:
        # fallback: find node by class_type
        for nid, n in workflow.items():
            if n.get("class_type") == "LTXDirectorCS25":
                director_id = nid
                break
    if director_id is None:
        return
    node = workflow[director_id]
    inputs = node.setdefault("inputs", {})

    # --- prompt ---
    if prompt is not None:
        # Prefer timeline_data JSON global_prompt
        td_raw = inputs.get("timeline_data")
        if isinstance(td_raw, str) and td_raw.strip().startswith("{"):
            try:
                td = _json.loads(td_raw)
                td["global_prompt"] = prompt
                # also update first segment if exists else create
                # ensure prompt is reflected in local_prompts for backward compat
                inputs["timeline_data"] = _json.dumps(td, ensure_ascii=False)
            except Exception:
                # fallback to local_prompts
                inputs["local_prompts"] = prompt
        else:
            inputs["local_prompts"] = prompt
            # also try timeline_data
            if isinstance(td_raw, str):
                try:
                    td = _json.loads(td_raw)
                    td["global_prompt"] = prompt
                    inputs["timeline_data"] = _json.dumps(td, ensure_ascii=False)
                except Exception:
                    pass
        # also ensure local_prompts reflects prompt (some exports read it)
        if not inputs.get("local_prompts"):
            inputs["local_prompts"] = prompt

    # --- duration / fps / frames ---
    if duration is not None or fps is not None:
        try:
            cur_duration = float(inputs.get("duration_seconds", duration or 5.0))
            cur_fps = int(inputs.get("frame_rate", fps or 24))
            if duration is not None:
                cur_duration = float(duration)
            if fps is not None:
                cur_fps = int(fps)
            # LTX constraint: frames %8==1
            frames = int(round(cur_duration * cur_fps))
            # adjust to satisfy %8==1
            remainder = frames % 8
            if remainder != 1:
                # prefer rounding up to next %8==1
                delta = (1 - remainder) % 8
                frames += delta
                # keep duration consistent if needed, but preserve fps
                cur_duration = frames / cur_fps
            inputs["duration_seconds"] = cur_duration
            inputs["duration_frames"] = frames
            inputs["duration_frames"] = frames
            inputs["end_frame"] = max(0, frames - 1)
            inputs["end_second"] = cur_duration
            inputs["frame_rate"] = cur_fps
            # also patch timeline_data mirrored fields
            td_raw = inputs.get("timeline_data")
            if isinstance(td_raw, str) and td_raw.strip().startswith("{"):
                try:
                    td = _json.loads(td_raw)
                    td["normalDurationFrames"] = frames
                    # if segments empty, leave global
                    inputs["timeline_data"] = _json.dumps(td, ensure_ascii=False)
                except Exception:
                    pass
        except Exception:
            pass
        # patch frame_rate outputs used elsewhere (nodes 5,240)
        # Node 5 and 240 reference 220:7 for frame_rate
        if fps is not None:
            # also ensure VHS_VideoCombine frame_rate via link will be correct
            pass

    # --- image (I2V) ---
    if image_filename is not None:
        # 1) Ensure LoadImage node exists (id 1000, avoid collision)
        load_id = None
        for nid, n in workflow.items():
            if n.get("class_type") == "LoadImage" and n.get("inputs", {}).get("image") == image_filename:
                load_id = nid
                break
        if load_id is None:
            # pick unused numeric id
            base = 1000
            while str(base) in workflow:
                base += 1
            load_id = str(base)
            workflow[load_id] = {
                "inputs": {"image": image_filename},
                "class_type": "LoadImage",
                "_meta": {"title": "Load Image (I2V)"},
            }
        # 2) Patch timeline_data to reference image for Director
        td_raw = inputs.get("timeline_data")
        if isinstance(td_raw, str) and td_raw.strip().startswith("{"):
            try:
                td = _json.loads(td_raw)
                # Set reference_mode to image if possible and embed image
                # Keep existing characters but ensure first character has image if needed
                # For simplest I2V, set retakeVideo.imageFile and reference_mode
                if "reference_mode" in td:
                    # Single image I2V: use reference image mode
                    # Common values: "OFF", "image", "video"
                    if td.get("reference_mode") == "OFF":
                        # Do not forcibly enable if model expects OFF, but embed image anyway
                        pass
                # Embed image reference in multiple plausible places
                # a) retakeVideo.imageFile
                if "retakeVideo" in td and isinstance(td["retakeVideo"], dict):
                    td["retakeVideo"]["imageFile"] = image_filename
                    td["retakeVideo"]["fileName"] = image_filename
                # b) characters[0].images
                if "characters" in td and isinstance(td["characters"], list) and td["characters"]:
                    # ensure first character carries image for reference
                    if isinstance(td["characters"][0], dict):
                        td["characters"][0].setdefault("images", [])
                        if image_filename not in td["characters"][0]["images"]:
                            # keep list short
                            td["characters"][0]["images"] = [image_filename]
                # c) also set a top-level imageFile if workflow expects
                td["imageFile"] = image_filename
                inputs["timeline_data"] = _json.dumps(td, ensure_ascii=False)
            except Exception:
                pass
        # 3) If workflow has an obvious image-accepting node, wire it
        # Search for nodes with "image" input usage (e.g., LTXDirectorGuide)
        # Try to find LTXDirectorGuideCS25 image-related wiring - if it has image input, set it
        # We also create a fallback VAEEncode path if VAEEncode exists
        # For generic case, try to locate VAEEncode or ImageToLatent
        for nid, n in workflow.items():
            if n.get("class_type") in ("VAEEncode", "VAEEncodeForInpaint"):
                inp = n.setdefault("inputs", {})
                if "pixels" in inp and isinstance(inp["pixels"], list):
                    # already wired to LoadImage?
                    if inp["pixels"][0] != load_id:
                        inp["pixels"] = [load_id, 0]
        # If no VAEEncode, leave LoadImage isolated but uploaded - Director will still see image via timeline_data


def prepare_workflow(
    model: str,
    prompt: str,
    negative_prompt=None,
    seed=None,
    *,
    image_filename: str | None = None,
    duration: float | None = None,
    fps: int | float | None = None,
    shot_id: str | None = None,
) -> dict:
    if model not in ADAPTERS:
        raise ValueError(f"Unknown model: {model}. Available: {sorted(ADAPTERS)}")
    config = ADAPTERS[model]

    # Deep-copy cached workflow so mutations don't pollute cache
    cached = _load_cached_workflow(str(config["workflow"]))
    workflow = copy.deepcopy(cached)

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

    # LTX-2.5 specific patching for I2V + timing
    if model == "ltx-2.5":
        _patch_ltx_workflow(
            workflow,
            prompt=prompt,
            image_filename=image_filename,
            duration=duration,
            fps=fps,
            shot_id=shot_id,
        )
    elif model == "minimax-h3" and image_filename is not None:
        # Generic: ensure LoadImage exists for minimax if needed
        load_id = None
        for nid, n in workflow.items():
            if n.get("class_type") == "LoadImage":
                load_id = nid
                n["inputs"]["image"] = image_filename
                break
        if load_id is None:
            base = 1000
            while str(base) in workflow:
                base += 1
            workflow[str(base)] = {
                "inputs": {"image": image_filename},
                "class_type": "LoadImage",
                "_meta": {"title": "Load Image (I2V)"},
            }

    return workflow
