from pathlib import Path

from film_director.pipeline.director import FilmDirector


def test_pipeline_status(tmp_path):
    director = FilmDirector(tmp_path)
    status = director.status()

    assert "story" in status
    assert "screenplay" in status
    assert "shots" in status
