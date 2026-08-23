import json
import time
import uuid
import requests


class ComfyUIClient:

    def __init__(self, base_url: str, timeout: int = 600, poll_interval: float = 1):
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.poll_interval = poll_interval
        self.client_id = str(uuid.uuid4())

    def queue(self, workflow: dict):
        response = requests.post(
            f"{self.base_url}/prompt",
            json={
                "prompt": workflow,
                "client_id": self.client_id,
            },
            timeout=30,
        )
        response.raise_for_status()
        return response.json()

    def history(self, prompt_id: str):
        response = requests.get(
            f"{self.base_url}/history/{prompt_id}",
            timeout=30,
        )
        response.raise_for_status()
        return response.json()

    def wait(self, prompt_id: str):
        start = time.time()

        while time.time() - start < self.timeout:
            history = self.history(prompt_id)

            if prompt_id in history:
                result = history[prompt_id]

                if result.get("status", {}).get("completed"):
                    return result

                if result.get("status", {}).get("status_str") == "error":
                    raise RuntimeError(json.dumps(result, indent=2))

            time.sleep(self.poll_interval)

        raise TimeoutError(f"ComfyUI timeout: {prompt_id}")

    def execute(self, workflow: dict):
        queued = self.queue(workflow)
        prompt_id = queued["prompt_id"]
        return self.wait(prompt_id)
