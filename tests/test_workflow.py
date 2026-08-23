from pathlib import Path

from film_director.comfyui.workflow import load_workflow


def test_workflow_json():
    for path in Path("workflows").rglob("*.json"):
        if path.stat().st_size:
            workflow = load_workflow(path)
            assert isinstance(workflow, dict)
