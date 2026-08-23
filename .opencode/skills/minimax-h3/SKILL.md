---
name: minimax-h3
description: MiniMax H3 structured prompt adapter for T2VA/I2VA/FL2VA/L2VA/Ref2VA.
---
MiniMax H3 Prompt Adapter
MiniMax H3 uses structured prompt formats associated with its Context-IR workflow.
The official public prompt-writing skill defines five modes:
T2VA
I2VA
FL2VA
L2VA
Ref2VA
For base text/keyframe modes use: references/base-en.txt and follow its final prompt structure.
---
integrated_multimodal_description
overall_soundscape
non_diegetic_music
---
For Ref2VA use: references/ref-en.txt and follow its six-section rewrite format.
---
subject_definitions
summary
retention_analysis
detailed_description
overall_soundscape
non_diegetic_music
---
Do not claim to reproduce the private H3-Context-IR implementation.
Mode selection
Use:
T2VA when no visual reference is required.
I2VA when a first frame is supplied.
FL2VA when first and last frames define the path.
L2VA when a last frame is supplied.
Ref2VA when multiple reference images/video/audio assets must be preserved.
Base prompt
`integrated_multimodal_description` must contain the complete visual/audio timeline.
Then:
`overall_soundscape`
Then:
`non_diegetic_music`
Ref2VA
Keep reference labels stable.
Example labels:
<Subject 1>
<Image 1>
<Video 1>
<Audio 1>
Never create an unresolved reference label.
Dialogue
Preserve exact dialogue text and language.
Use explicit speaker identity.
Timing
Use monotonically increasing timestamps when describing multiple cuts.
Output
Create:
project/prompts/<shot_id>.h3.yaml
The compiler validates required sections before writing the artifact.
