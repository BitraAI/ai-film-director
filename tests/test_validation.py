from pathlib import Path
from film_director.validation import validate_file


def test_story_schema():
    data = Path("projects/example/story/story.yaml")
    schema = Path("schemas/story.schema.yaml")

    if data.exists():
        assert validate_file(data, schema)
