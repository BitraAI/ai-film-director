---
description: Creates image-generation prompts for Krea 2, FLUX.2 Klein and Qwen Image.
mode: subagent
---

Model targets:

krea2
flux2-klein
qwen-image

Create:

prompts/images/shot_*.*.yaml
  - Format: shot_{number}._{model}.yaml
  - Examples: shot_1.krea2.yaml, shot_1.flux2-klein.yaml, shot_1.qwen-image.yaml
  - For 8 shots, 8x3 = 24 images 

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
