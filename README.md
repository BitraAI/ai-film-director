# AI Film Director

OpenCode-native pipeline that turns a story idea into a finished film:

```
Story → Screenplay → Characters + Sheets → Locations → Props → Storyboard → Shot List → Image Prompts → Krea 2 / FLUX.2 Klein / Qwen Image → Video Prompts → LTX-2.5 / MiniMax H3 → Audio Prompts → Qwen3-TTS → Final Edit (FFmpeg)
```

Continuity, IDs, and schemas are validated at every stage. ComfyUI workflows are executed through adapters that only touch configured prompt/input nodes.

## Requirements

- [OpenCode](https://opencode.ai) >= 1.18
- Python 3.11+
- [ComfyUI](https://github.com/comfyanonymous/ComfyUI) (local or remote)
- FFmpeg (`ffmpeg` on PATH or via `FFMPEG_BIN`)
- ComfyUI workflow JSONs for the backends you use

## Directory Structure

```
ai-film-director/
├── README.md
├── opencode.json
├── pyproject.toml
├── .env.example
│
├── .opencode/
│   ├── agents/                  # 14 sub-agents delegated by @film-director
│   │   ├── film-director.md     # primary orchestrator
│   │   ├── story-agent.md
│   │   ├── screenplay-agent.md
│   │   ├── character-agent.md
│   │   ├── location-agent.md
│   │   ├── prop-agent.md
│   │   ├── storyboard-agent.md
│   │   ├── shot-agent.md
│   │   ├── image-prompt-agent.md
│   │   ├── video-prompt-agent.md
│   │   ├── audio-agent.md
│   │   ├── workflow-agent.md
│   │   ├── continuity-agent.md
│   │   └── final-editor-agent.md
│   ├── commands/                # 14 slash commands
│   │   ├── film.md              # full pipeline
│   │   ├── story.md
│   │   ├── screenplay.md
│   │   ├── characters.md
│   │   ├── locations.md
│   │   ├── props.md
│   │   ├── storyboard.md
│   │   ├── shots.md
│   │   ├── images.md
│   │   ├── videos.md
│   │   ├── audio.md
│   │   ├── render.md
│   │   ├── validate.md
│   │   └── status.md
│   └── skills/                  # 14 skills (see SKILL.md in each)
│       ├── story-development/
│       ├── screenplay/
│       ├── character-design/
│       ├── storyboard/
│       ├── shot-design/
│       ├── flux-2-klein/
│       ├── krea-2/
│       ├── qwen-image/
│       ├── ltx-2.5/             # references/: creative-examples.md, ltx-vocabulary.md, multishot-format.md, etc.
│       ├── minimax-h3/          # references/: base-en.txt, ref-en.txt
│       ├── qwen3-tts/
│       ├── continuity/
│       ├── comfyui/
│       └── final-edit/
│
├── schemas/                     # JSON Schema (YAML) for every artifact
│   ├── project.schema.yaml
│   ├── story.schema.yaml
│   ├── screenplay.schema.yaml
│   ├── character.schema.yaml
│   ├── character-sheet.schema.yaml
│   ├── location.schema.yaml
│   ├── prop.schema.yaml
│   ├── storyboard.schema.yaml
│   ├── shot.schema.yaml
│   ├── image-prompt.schema.yaml
│   ├── video-prompt.schema.yaml
│   ├── audio-prompt.schema.yaml
│   ├── workflow.schema.yaml
│   ├── render.schema.yaml
│   └── manifest.schema.yaml
│
├── workflows/                   # User-supplied ComfyUI graphs (gitignored content)
│   ├── image/
│   │   ├── krea2.json
│   │   ├── flux2-klein.json
│   │   └── qwen-image.json
│   ├── video/
│   │   ├── ltx-2.5.json
│   │   └── minimax-h3.json
│   └── audio/
│       └── qwen3-tts.json
│
├── projects/                    # Generated films (gitignored)
│   └── <film>/
│       ├── project.yaml
│       ├── story/story.yaml
│       ├── screenplay/screenplay.yaml
│       ├── characters/characters.yaml
│       ├── characters/sheets/*.yaml
│       ├── locations/locations.yaml
│       ├── props/props.yaml
│       ├── storyboard/storyboard.yaml
│       ├── shots/shots.yaml
│       ├── prompts/images/*.yaml
│       ├── prompts/videos/*.yaml
│       ├── prompts/audio/*.yaml
│       ├── renders/images/
│       ├── renders/videos/
│       ├── audio/
│       ├── final/film.mp4
│       └── manifest.yaml
│
├── src/                         # Flat package (pip install -e ., PYTHONPATH=src)
│   ├── cli.py                   # film-director status|manifest
│   ├── config.py                # env: COMFYUI_URL, OUTPUT_ROOT, etc.
│   ├── paths.py                 # project_paths() / create_project_tree()
│   ├── validation.py            # validate_file() (cached schemas)
│   ├── manifest.py              # build_manifest() / save_manifest()
│   ├── comfyui/
│   │   ├── client.py            # ComfyUIClient (Session + retry + backoff)
│   │   ├── workflow.py          # load_workflow() / set_node_input()
│   │   └── adapters.py          # prepare_workflow() (cached)
│   ├── pipeline/
│   │   └── director.py          # FilmDirector.status() / next_stage()
│   ├── render/
│   │   ├── images.py            # render_image()
│   │   ├── videos.py            # render_video()
│   │   ├── audio.py             # render_audio()
│   │   └── final.py             # render_final() → final/film.mp4
│   └── utils/
│       ├── files.py             # atomic load/save JSON/YAML
│       └── jsonx.py             # load_json / save_json
│
├── scripts/                     # Standalone entry points
│   ├── init_project.py
│   ├── validate_project.py
│   ├── generate_images.py
│   ├── generate_videos.py
│   ├── generate_audio.py
│   ├── render_final.py
│   ├── build_manifest.py
│   └── run_workflow.py
│
└── tests/
    ├── test_validation.py
    ├── test_workflow.py
    └── test_pipeline.py
```

## Install

```bash
git clone https://github.com/BitraAI/ai-film-director.git
cd ai-film-director

python -m venv film-env
source film-env/bin/activate
python -m pip install -U pip uv
uv pip install -e .
```

Verify:

```bash
film-director --help
python -m pytest -q
```

## Configure

```bash
cp .env.example .env
```

`.env.example` (`src/config.py:1`):

```
COMFYUI_URL=http://127.0.0.1:8188
OUTPUT_ROOT=projects
COMFYUI_TIMEOUT=600
POLL_INTERVAL=1
FFMPEG_BIN=ffmpeg
PYTHONUNBUFFERED=1
```

| Var | Default | Description |
|-----|---------|-------------|
| `COMFYUI_URL` | `http://127.0.0.1:8188` | ComfyUI API endpoint |
| `OUTPUT_ROOT` | `projects` | Root for `init_project.py` |
| `COMFYUI_TIMEOUT` | `600` | Seconds to wait for a workflow |
| `POLL_INTERVAL` | `1` | Poll interval (seconds) |
| `FFMPEG_BIN` | `ffmpeg` | FFmpeg binary |

### ComfyUI Workflows

Place your exported ComfyUI API graphs here (adapters only mutate configured prompt/input nodes):

```
workflows/image/krea2.json
workflows/image/flux2-klein.json
workflows/image/qwen-image.json
workflows/video/ltx-2.5.json
workflows/video/minimax-h3.json
workflows/audio/qwen3-tts.json
```

Validate they load:

```bash
python -m pytest tests/test_workflow.py -v
```

## Create a Film

```bash
python scripts/init_project.py my-film
# → projects/my-film/
```

This creates `project.yaml` (`project_id`, `title`, `genre`, `aspect_ratio`, `fps`, `duration_seconds` validated by `schemas/project.schema.yaml:1`) and the tree from `src/paths.py:4`:

```
story/  screenplay/  characters/sheets/  locations/  props/  storyboard/  shots/
prompts/images/  prompts/videos/  prompts/audio/
renders/images/  renders/videos/  audio/  final/
```

## Usage — OpenCode

Install OpenCode, then start it from the repo root:

```bash
curl -fsSL https://opencode.ai/install | bash
opencode
```

Primary orchestrator (`opencode.json:4`, `.opencode/agents/film-director.md:1`):

```
@film-director
```

Full pipeline (story → screenplay → characters → locations → props → storyboard → shots → images → videos → audio → continuity → render):

```
/film my-film
```

Run stages independently:

```
/story my-film        # → story/story.yaml
/screenplay my-film   # → screenplay/screenplay.yaml
/characters my-film   # → characters/characters.yaml + characters/sheets/*.yaml
/locations my-film    # → locations/locations.yaml
/props my-film        # → props/props.yaml
/storyboard my-film   # → storyboard/storyboard.yaml
/shots my-film        # → shots/shots.yaml
/images my-film       # → prompts/images/*.yaml + renders/images/
/videos my-film       # → prompts/videos/*.yaml + renders/videos/
/audio my-film        # → prompts/audio/*.yaml + audio/
/render my-film       # → final/film.mp4
/validate my-film     # schema + continuity checks
/status my-film       # manifest status
```

Each command delegates to its agent (e.g. `/story` → `@story-agent`, `/images` → `@image-prompt-agent`). See `.opencode/commands/*.md` and `.opencode/agents/*.md`.

## Usage — Scripts & CLI

All scripts accept a project path (`projects/<name>` or absolute).

```bash
# Validate schemas (story, screenplay, characters, locations, props, storyboard, shots)
python scripts/validate_project.py projects/my-film
# src/validation.py:6 — jsonschema against schemas/*.schema.yaml

# Project status / manifest
python scripts/build_manifest.py projects/my-film  # preferred — writes manifest.yaml via src/manifest.py:29
film-director status projects/my-film   # src/cli.py:15 — prints READY/MISSING per stage + next_stage()
film-director manifest projects/my-film # same as build_manifest.py

# Images — iterate prompts/images/*.yaml → renders/images/
python scripts/generate_images.py projects/my-film
python scripts/generate_images.py projects/my-film --model krea2
python scripts/generate_images.py projects/my-film --model flux2-klein
python scripts/generate_images.py projects/my-film --model qwen-image
# src/render/images.py:render_image() + src/comfyui/client.py:ComfyUIClient

# Videos — iterate prompts/videos/*.yaml → renders/videos/
python scripts/generate_videos.py projects/my-film
python scripts/generate_videos.py projects/my-film --model ltx-2.5
python scripts/generate_videos.py projects/my-film --model minimax-h3

# Audio — iterate prompts/audio/*.yaml → audio/
python scripts/generate_audio.py projects/my-film
# src/render/audio.py:render_audio()

# Final edit — FFmpeg concat of renders → final/film.mp4
python scripts/render_final.py projects/my-film
# src/render/final.py:render_final()

# Ad-hoc ComfyUI execution
python scripts/run_workflow.py <model> "<prompt>" [--negative "..."] [--seed 42] [--output out.yaml]
# src/comfyui/adapters.py:prepare_workflow() + src/comfyui/client.py:ComfyUIClient.execute()
```

## Pipeline Stages

| # | Stage | Command | Input | Output | Schema |
|---|-------|---------|-------|--------|--------|
| 1 | Story | `/story` | user idea | `story/story.yaml` | `story.schema.yaml` |
| 2 | Screenplay | `/screenplay` | story | `screenplay/screenplay.yaml` | `screenplay.schema.yaml` |
| 3 | Characters | `/characters` | story + screenplay | `characters/characters.yaml`, `characters/sheets/*.yaml` | `character.schema.yaml`, `character-sheet.schema.yaml` |
| 4 | Locations | `/locations` | story + screenplay | `locations/locations.yaml` | `location.schema.yaml` |
| 5 | Props | `/props` | story + screenplay | `props/props.yaml` | `prop.schema.yaml` |
| 6 | Storyboard | `/storyboard` | screenplay + characters + locations | `storyboard/storyboard.yaml` | `storyboard.schema.yaml` |
| 7 | Shot List | `/shots` | storyboard | `shots/shots.yaml` | `shot.schema.yaml` |
| 8 | Image Prompts | `/images` (prompt phase) | shots + sheets + locations | `prompts/images/*.yaml` | `image-prompt.schema.yaml` |
| 9 | Image Generation | `/images` (render) / `generate_images.py` | image prompts + `workflows/image/*.json` | `renders/images/` | `workflow.schema.yaml` |
| 10 | Video Prompts | `/videos` (prompt phase) | shots + images | `prompts/videos/*.yaml` | `video-prompt.schema.yaml` |
| 11 | Video Generation | `/videos` (render) / `generate_videos.py` | video prompts + `workflows/video/*.json` | `renders/videos/` | `workflow.schema.yaml` |
| 12 | Audio | `/audio` / `generate_audio.py` | screenplay dialogue | `prompts/audio/*.yaml`, `audio/` | `audio-prompt.schema.yaml` |
| 13 | Final | `/render` / `render_final.py` | renders + audio | `final/film.mp4` | `render.schema.yaml` |

Continuity is enforced at every stage by `@continuity-agent` (`.opencode/skills/continuity/SKILL.md`). Director rules (`.opencode/agents/film-director.md:26`): stable IDs, every scene → shots, every shot → image prompt, every motion shot → video prompt, every dialogue → audio prompt, preserve appearance/state/chronology.

`FilmDirector.next_stage()` order (`src/pipeline/director.py:4`): `story → screenplay → characters → locations → props → storyboard → shots → images → videos → audio → final`.

## Schemas & Validation

All artifacts are YAML validated with `jsonschema` (`src/validation.py:6`):

```bash
python scripts/validate_project.py projects/my-film
python -m pytest tests/test_validation.py -v
```

Schemas live in `schemas/` and are referenced by each skill's `SKILL.md`.

## Development

```bash
# All tests
python -m pytest -v

# Specific
python -m pytest tests/test_pipeline.py -v  # FilmDirector.status/next_stage
python -m pytest tests/test_workflow.py -v  # workflows/*.json loadable
python -m pytest tests/test_validation.py -v
```

Project config: `pyproject.toml:1` (`setuptools`, `requires-python >=3.11`, deps `PyYAML`, `jsonschema`, `requests`).

## License

No `LICENSE` file is currently committed. All rights reserved unless a license is added.
