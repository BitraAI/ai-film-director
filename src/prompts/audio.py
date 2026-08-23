def build_audio_prompt(audio):
    return (
        f"Speaker: {audio['speaker_id']}\n"
        f"Text: {audio['text']}\n"
        f"Voice: {audio.get('voice', '')}\n"
        f"Emotion: {audio.get('emotion', '')}\n"
        f"Tone: {audio.get('tone', '')}\n"
        f"Pace: {audio.get('pace', '')}\n"
        f"Pitch: {audio.get('pitch', '')}\n"
        f"Energy: {audio.get('energy', '')}"
    )
