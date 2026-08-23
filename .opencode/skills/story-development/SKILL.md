---
name: story-development
description: Develop production-ready film stories with stable IDs and visual continuity.
compatibility: opencode
---

Create:

story/story.yaml

Required:

- premise
- logline
- genre
- tone
- theme
- characters
- conflict
- stakes
- acts
- beats
- ending

Rules:

1. Stable IDs.
2. Every beat belongs to an act.
3. Every character referenced by ID.
4. Every visual element must be concrete enough for later image generation.
5. Avoid continuity contradictions.

Validate with:

schemas/story.schema.yaml
