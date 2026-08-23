# AI Film Director

AI Film Director is an OpenCode project that transforms:

→ Story
→ Screenplay
→ Characters
→ Character Sheets
→ Locations
→ Props
→ Storyboard
→ Shot List
→ Image Prompts
→ Krea 2 / FLUX.2 Klein / Qwen Image
→ Video Prompts
→ LTX-2.5 / MiniMax H3
→ Audio Prompts
→ Qwen3-TTS
→ Final Video

## Requirements

- OpenCode
- Python 3.11+
- ComfyUI
- FFmpeg
- ComfyUI workflows for:
  - Krea 2
  - FLUX.2 Klein
  - Qwen Image
  - LTX-2.5
  - MiniMax H3
  - Qwen3-TTS

## Directory Structure

ai-film-director/
├── README.md
├── opencode.json
├── pyproject.toml
├── .env.example
│
├── .opencode/
│   ├── agents/
│   │   ├── film-director.md
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
│   │
│   ├── commands/
│   │   ├── film.md
│   │   ├── story.md
│   │   ├── screenplay.md
│   │   ├── characters.md
│   │   ├── locations.md
|   |   ├── props.md
│   │   ├── storyboard.md
│   │   ├── shots.md
│   │   ├── images.md
│   │   ├── videos.md
│   │   ├── audio.md
│   │   ├── render.md
│   │   ├── validate.md
│   │   └── status.md
│   │
│   └── skills/
│       ├── story-development/
│       │   ├── SKILL.md
│       │   └── references/
│       │       └── story-rules.md
│       ├── screenplay/
│       │   └── SKILL.md
│       ├── character-design/
│       │   └── SKILL.md
│       ├── storyboard/
│       │   └── SKILL.md
│       ├── shot-design/
│       │   └── SKILL.md
│       ├── flux-2-klein/
│       │   ├── SKILL.md
│       │   └── references/
│       ├── krea-2/
│       │   ├── SKILL.md
│       │   └── references/
│       ├── qwen-image/
│       │   ├── SKILL.md
│       │   └── references/
│       ├── ltx-2.5/
│       │   ├── SKILL.md
│       │   └── references/
│       │       ├── creative-examples.md
│       │       └── ltx-vocabulary.md
│       │       └── multishot-format.md
│       │       └── screenplay-format.md
│       │       └── single-shot-format.md
│       ├── minimax-h3/
│       │   ├── SKILL.md
│       │   └── references/
│       │       └── -base-en.txt
│       │       └── ref-en.txt
│       ├── qwen3-tts/
│       │   └── SKILL.md
│       ├── continuity/
│       │   └── SKILL.md
│       ├── comfyui/
│       │   └── SKILL.md
│       └── final-edit/
│           └── SKILL.md
│
├── schemas/
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
├── workflows/
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
├── projects/
│   └── .gitkeep
│
├── src/
│   └── film_director/
│       ├── __init__.py
│       ├── cli.py
│       ├── config.py
│       ├── ids.py
│       ├── paths.py
│       ├── validation.py
│       ├── manifest.py
│       │
│       ├── pipeline/
│       │   ├── __init__.py
│       │   ├── director.py
│       │   ├── stage.py
│       │   └── continuity.py
│       │
│       ├── prompts/
│       │   ├── __init__.py
│       │   ├── image.py
│       │   ├── video.py
│       │   └── audio.py
│       │
│       ├── comfyui/
│       │   ├── __init__.py
│       │   ├── client.py
│       │   ├── workflow.py
│       │   └── adapters.py
│       │
│       ├── render/
│       │   ├── __init__.py
│       │   ├── images.py
│       │   ├── videos.py
│       │   ├── audio.py
│       │   └── final.py
│       │
│       └── utils/
│           ├── __init__.py
│           ├── files.py
│           └── jsonx.py
│
├── scripts/
│   ├── init_project.py
│   ├── validate_project.py
│   ├── run_workflow.py
│   ├── generate_images.py
│   ├── generate_videos.py
│   ├── generate_audio.py
│   ├── render_final.py
│   └── build_manifest.py
│
└── tests/
    ├── test_validation.py
    ├── test_workflow.py
    └── test_pipeline.py

## Install

git clone https://github.com/BitraAI/ai-film-director.git
cd ai-film-director

python -m venv film-env

source film-env/bin/activate
python -m pip install -U pip
python -m pip install -U uv
uv pip install -e .

Copy:

cp .env.example .env

Configure:

COMFYUI_URL=http://127.0.0.1:8188
OUTPUT_ROOT=projects
Install Workflows

Put the user's ComfyUI JSON workflows here:

workflows/image/krea2.json
workflows/image/flux2-klein.json
workflows/image/qwen-image.json

workflows/video/ltx-2.5.json
workflows/video/minimax-h3.json

workflows/audio/qwen3-tts.json

The workflow adapter modifies only the configured prompt/input nodes and preserves the remainder of the workflow.

Create a Film
python scripts/init_project.py my-film

This creates:

projects/my-film/
├── project.yaml
├── story/
├── screenplay/
├── characters/
├── locations/
├── props/
├── storyboard/
├── shots/
├── prompts/
├── renders/
├── audio/
├── final/
└── manifest.yaml

### OpenCode

curl -fsSL https://opencode.ai/install | bash
Start OpenCode from the repository:

opencode

Primary director:

@film-director
Full Pipeline
/film my-film

Or execute stages independently:

/story my-film
/screenplay my-film
/characters my-film
/locations my-film
/props my-film
/storyboard my-film
/shots my-film
/images my-film
/videos my-film
/audio my-film
/render my-film
Validate
/validate my-film

or:

python scripts/validate_project.py projects/my-film

Generate Images
python scripts/generate_images.py projects/my-film

Select an image backend:

python scripts/generate_images.py projects/my-film --model krea2
python scripts/generate_images.py projects/my-film --model flux2-klein
python scripts/generate_images.py projects/my-film --model qwen-image

Generate Videos
python scripts/generate_videos.py projects/my-film

Select an video backend:

python scripts/generate_videos.py projects/my-film --model ltx-2.5
python scripts/generate_videos.py projects/my-film --model minimax-h3

Generate Audio
python scripts/generate_audio.py projects/my-film

Final Render
python scripts/render_final.py projects/my-film

Output:

projects/my-film/final/film.mp4
Project State
/status my-film

or:

python scripts/build_manifest.py projects/my-film
Pipeline Stages

1. Story

Input:

User story idea

Output:

story/story.yaml

2. Screenplay

Output:

screenplay/screenplay.yaml

3. Characters

Output:

characters/characters.yaml
characters/sheets/*.yaml

4. Locations / Props

Output:

locations/locations.yaml
props/props.yaml

5. Storyboard

Output:

storyboard/storyboard.yaml

6. Shot List

Output:

shots/shots.yaml

7. Image Prompts

Output:

prompts/images/*.yaml

8. Image Generation

Generated assets:

renders/images/

9. Video Prompts

Output:

prompts/videos/*.yaml

10. Video Generation

Generated assets:

renders/videos/

11. Audio

Output:

prompts/audio/*.yaml
audio/

12. Final

Output:

final/film.mp4


