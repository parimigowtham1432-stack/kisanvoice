
"""Crop extraction and normalization."""

import re
from app.config import CROP_ALIASES


def extract_crops(text: str) -> list[str]:
    text_lower = text.lower()
    matches = []

    aliases = sorted(CROP_ALIASES.items(), key=lambda x: len(x[0]), reverse=True)

    for alias, canonical in aliases:
        for match in re.finditer(rf"\b{re.escape(alias)}\b", text_lower):
            matches.append((match.start(), canonical))

    matches.sort(key=lambda x: x[0])

    result = []
    for _, crop in matches:
        if crop not in result:
            result.append(crop)

    return result


def extract_crop(text: str) -> str | None:
    crops = extract_crops(text)
    return crops[0] if crops else None
