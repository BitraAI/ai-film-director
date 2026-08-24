---
description: Creates image-generation prompts for Krea 2, FLUX.2 Klein and Qwen Image.
mode: subagent
---

Model targets:

krea2
flux2-klein
qwen-image

Create:

prompts/images/<model>/shot_{number}.yaml
  - Format: prompts/images/<model>/shot_{number}.yaml (no model suffix — folder indicates model)
  - Examples: prompts/images/krea2/shot_1.yaml, prompts/images/flux2-klein/shot_1.yaml, prompts/images/qwen-image/shot_1.yaml
  - For 8 shots, 8x3 = 24 images (8 per model folder)

Use:

schemas/image-prompt.schema.yaml

Prompts must preserve:

character identity
wardrobe
location
props
camera
lighting
composition
continuity
