from pathlib import Path
import subprocess

from film_director.config import FFMPEG_BIN


def create_concat_file(
    videos: list[Path],
    concat_file: Path,
):
    concat_file.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    lines = []

    for video in videos:
        path = video.resolve().as_posix()
        path = path.replace("'", r"'\''")
        lines.append(f"file '{path}'")

    concat_file.write_text(
        "\n".join(lines) + "\n",
        encoding="utf-8",
    )

    return concat_file


def render_final(
    project_root: Path,
    output_name: str = "film.mp4",
):
    video_dir = (
        project_root
        / "renders"
        / "videos"
    )

    final_dir = project_root / "final"
    final_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    output = final_dir / output_name

    videos = sorted(
        video_dir.glob("*.mp4")
    )

    if not videos:
        raise FileNotFoundError(
            f"No video clips found in {video_dir}"
        )

    concat_file = final_dir / "concat.txt"

    create_concat_file(
        videos,
        concat_file,
    )

    command = [
        FFMPEG_BIN,
        "-y",
        "-f",
        "concat",
        "-safe",
        "0",
        "-i",
        str(concat_file),
        "-c",
        "copy",
        str(output),
    ]

    subprocess.run(
        command,
        check=True,
    )

    return output
