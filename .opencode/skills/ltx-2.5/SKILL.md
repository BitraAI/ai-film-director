---
name: ltx-2.5
description: LTX-2.5 prompt adapter for cinematic video generation.
---
LTX-2.5 Prompt Adapter

Use When

Use only for LTX 2.5 video generation.

Do not use for H3, Kling, Veo, Sora, Runway, Seedance, or image-generation prompts.

Mode

Classify input:

Input	Mode	Reference
Text/shot specification	T2V	references/single-shot-format.md
First-frame image	I2V	references/single-shot-format.md
Reference images	T2V + visual refs	references/single-shot-format.md
Source video	V2V	references/single-shot-format.md
Audio-driven generation	A2V	references/single-shot-format.md
Multiple connected cuts	Multishot	references/multishot-format.md
Dialogue-heavy scene	Screenplay	references/screenplay-format.md

Default to single-shot when uncertain.

Prompt Structure

Build every prompt in this order:

Shot — scale, angle, visual/cinematic style
Scene — location, lighting, color, texture, atmosphere
Action — one dominant physical action, present tense
Character — appearance, wardrobe, physical emotion, continuity
Camera — framing, movement, focus, camera behavior
Audio — ambience, action sounds, music, dialogue, voice

Load references/ltx-vocabulary.md when additional cinematic vocabulary is needed.

Core Rules
Use concrete visual descriptions.
Use present tense.
One dominant action per shot.
Describe emotion through physical behavior.
Specify camera behavior for every shot.
Describe audio for every shot.
Keep lighting internally consistent.
Maintain character identity across shots.
Use natural-language camera movement.
Avoid unnecessary numerical specifications.
Avoid contradictory descriptions.
Dialogue must be in quotation marks.
Keep important on-screen text short.
Avoid named celebrities, trademarked characters, and third-party IP.
Single-Shot

Load:

references/single-shot-format.md

Output:

One flowing cinematic paragraph.
Normally 4–8 descriptive sentences.
Present tense.
Integrate all six prompt elements.
No field labels.
No JSON.
No shot-list formatting.

Structure:

SHOT → SCENE → ACTION → CHARACTER → CAMERA → AUDIO

Multishot

Load:

references/multishot-format.md

LTX 2.5 native multishot should be written as one chronological prose sequence.

Rules:

2–4 connected shots.
Never output Shot 1, Shot 2, etc.
Introduce cuts naturally:
A hard cut transitions to...
A match cut connects...
The image dissolves into...
Re-establish framing at each cut.
Re-identify recurring characters.
Maintain audio continuity.
Give each shot one dominant action.
Maintain the six-part structure within each shot.

Typical progression:

ESTABLISH → DETAIL → REACTION

or

WIDE → MEDIUM → CLOSE-UP

Screenplay

Load:

references/screenplay-format.md

Use:

INT./EXT. LOCATION – TIME

Then:

VISUAL ACTION

CHARACTER

(physical acting direction)

"Dialogue"

Integrate camera and audio naturally.

LTX 2.5 Technical Constraints
num_frames % 8 == 1
Width and height divisible by 32
Distilled model: 8 steps
Distilled CFG: 1
Auto-duration may be used by omitting frame count
LTX 2.5 supports native synchronized audio
LTX 2.5 supports native multishot

Validation

Before returning:

Multishot maintains audio continuity

Dialogue quoted

Correct mode selected

Correct format reference loaded

Shot specified

Scene/lighting specified

Character specified

One dominant action per shot

Camera specified

Audio specified

Present tense

Character continuity maintained

No contradictory directions

No unnecessary numerical specifications

Multishot has explicit transitions

Output

Return the final LTX 2.5 prompt only.

Do not return analysis, JSON, field labels, or explanations unless the calling agent explicitly requests metadata.

Create:
project/prompts/<shot_id>.ltx-2.5.yaml
with:
shot_id
model
prompt
duration
source
