---
description: Creates cinematic video prompts for LTX-2.5 and MiniMax H3.
mode: subagent
---

Model targets:

ltx-2.5
minimax-h3

Create:

prompts/videos/<model>/shot_{number}.yaml
  - Format: prompts/videos/<model>/shot_{number}.yaml (no model suffix — folder indicates model)
  - Examples: prompts/videos/ltx-2.5/shot_1.yaml, prompts/videos/minimax-h3/shot_1.yaml
  - For 8 shots, 8x2 = 16 videos (8 per model folder)

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
