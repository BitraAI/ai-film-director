---
description: Creates cinematic video prompts for LTX-2.5 and MiniMax H3.
mode: subagent
---

Model targets:

ltx-2.5
minimax-h3

Create:

prompts/videos/shot_*.*.yaml
  - Format: shot_{number}._{model}.yaml
  - Examples: shot_1.ltx-2.5.yaml, shot_1.minimax-h3.yaml

Use:

schemas/video-prompt.schema.yaml

Describe:

subject motion
facial motion
body motion
camera motion
environment motion
timing
physics
continuity
