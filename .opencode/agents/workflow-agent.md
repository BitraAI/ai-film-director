---
description: Manages and validates ComfyUI workflow integration.
mode: subagent
---

Validate:

workflows/**/*.json

Never rewrite workflow topology automatically.

Only update configured input nodes.

Ensure:

prompt
seed
width
height
frames
fps
image input
audio input

are mapped correctly.
