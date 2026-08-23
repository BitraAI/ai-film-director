from pathlib import Path
from film_director.utils.files import load_yaml


class Stage:

    def __init__(self, project_root: Path):
        self.root = project_root

    def exists(self, relative: str) -> bool:
        return (self.root / relative).exists()

    def load(self, relative: str):
        return load_yaml(self.root / relative)
