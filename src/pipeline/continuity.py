def collect_ids(data, key):
    return {
        item[key]
        for item in data
        if isinstance(item, dict) and key in item
    }


def missing_ids(references, known):
    return sorted(set(references) - known)


def audit_character_ids(screenplay, characters):
    known = collect_ids(characters, "character_id")
    refs = []

    for scene in screenplay:
        refs.extend(scene.get("characters", []))

        for dialogue in scene.get("dialogue", []):
            refs.append(dialogue["character_id"])

    return missing_ids(refs, known)
