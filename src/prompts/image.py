def build_image_prompt(shot, character_anchors, location_anchors, props):
    return (
        f"SUBJECT: {shot['subject']}\n"
        f"CHARACTERS: {', '.join(character_anchors)}\n"
        f"LOCATION: {', '.join(location_anchors)}\n"
        f"PROPS: {', '.join(props)}\n"
        f"ACTION: {shot['action']}\n"
        f"SHOT: {shot['shot_size']}\n"
        f"ANGLE: {shot.get('angle', '')}\n"
        f"LENS: {shot.get('lens', '')}\n"
        f"CAMERA: {shot.get('camera_movement', '')}\n"
        f"COMPOSITION: {shot.get('composition', '')}\n"
        f"LIGHTING: {shot.get('lighting', '')}\n"
        f"Create a cinematic production frame with strict character and "
        f"location continuity."
    )
