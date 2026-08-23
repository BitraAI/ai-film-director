---
name: qwen3-tts
description: Qwen3-TTS dialogue prompt adapter
---

# Qwen3-TTS

Generate dialogue specifications from the canonical audio plan.

Each dialogue item should define:

- speaker
- text
- emotion
- intensity
- pace
- pause
- voice identity
- pronunciation requirements

Character voice identity must remain stable.

Do not rewrite dialogue text unless explicitly instructed.

Output structured audio prompt YAML.
