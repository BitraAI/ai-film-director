from pathlib import Path


STAGES = [
    "story",
    "screenplay",
    "characters",
    "world",
    "storyboard",
    "shots",
    "images",
    "videos",
    "audio",
    "final",
]


class FilmDirector:

    def __init__(self, project_root: Path):
        self.root = project_root

    def status(self):
        result = {}

        files = {
            "story": "story/story.yaml",
            "screenplay": "screenplay/screenplay.yaml",
            "characters": "characters/characters.yaml",
            "world": "world/locations.yaml",
            "storyboard": "storyboard/storyboard.yaml",
            "shots": "shots/shots.yaml",
            "images": "prompts/images",
            "videos": "prompts/videos",
            "audio": "prompts/audio",
            "final": "final/film.mp4",
        }

        for stage, path in files.items():
            result[stage] = (self.root / path).exists()

        return result

    def next_stage(self):
        status = self.status()

        for stage in STAGES:
            if not status.get(stage, False):
                return stage

        return "complete"
