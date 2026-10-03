
"""Agricultural activity extraction."""

import re
from app.config import ACTIVITY_ALIASES


def extract_activities(text: str) -> list[str]:
    text_lower = text.lower()
    matches = []

    for canonical, phrases in ACTIVITY_ALIASES.items():
        for phrase in sorted(phrases, key=len, reverse=True):
            match = re.search(rf"\b{re.escape(phrase)}\b", text_lower)
            if match:
                matches.append((match.start(), canonical, phrase))
                break

    matches.sort(key=lambda x: x[0])

    filtered = []
    for start, canonical, phrase in matches:
        if canonical == "field maintenance" and any(item[1] == "labour" for item in matches):
            continue
        if canonical == "fertilizer" and any(item[1] == "fertilizer purchase" for item in matches):
            continue
        if canonical == "pesticide spraying" and "fungicide" in text_lower and any(item[1] == "fungicide spraying" for item in matches):
            continue
        if canonical == "labour" and re.search(
            r"\b(?:labour|labor|workers?)\b.*\bfor\b.*\b(?:pesticide|fungicide|deweeding|weeding|harvesting|sorting|drying|packing|transportation|transplanting|seed|planting|fertilizer|irrigation|selling)\b",
            text_lower,
        ):
            continue
        filtered.append((start, canonical))

    # Remove duplicates while preserving order.
    result = []
    for _, activity in filtered:
        if activity not in result:
            result.append(activity)

    return result
