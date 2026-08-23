def build_video_prompt(shot, image_prompt):
    return (
        f"Use the supplied reference image as the visual continuity anchor.\n\n"
        f"SUBJECT: {shot['subject']}\n"
        f"ACTION: {shot['action']}\n"
        f"SUBJECT MOTION: Natural physical movement matching the action.\n"
        f"CAMERA MOTION: {shot.get('camera_movement', 'static')}\n"
        f"FRAMING: {shot.get('framing', '')}\n"
        f"LIGHTING: {shot.get('lighting', '')}\n"
        f"DURATION: {shot['duration']} seconds.\n"
        f"CONTINUITY: Preserve identity, wardrobe, props, location and "
        f"screen direction.\n\n"
        f"REFERENCE IMAGE DESCRIPTION:\n{image_prompt}"
    )
