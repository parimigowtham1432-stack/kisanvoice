
"""Money extraction and normalization."""

import re

NUMBER_WORDS = {
    "zero": 0, "one": 1, "two": 2, "three": 3, "four": 4,
    "five": 5, "six": 6, "seven": 7, "eight": 8, "nine": 9,
    "ten": 10, "hundred": 100, "thousand": 1000, "lakh": 100000,
}


def _words_to_number(words: str) -> float | None:
    tokens = re.findall(r"[a-z]+", words.lower())
    total = 0
    current = 0

    for token in tokens:
        value = NUMBER_WORDS.get(token)
        if value is None:
            continue

        if token == "hundred":
            current = max(current, 1) * 100
        elif token in {"thousand", "lakh"}:
            total += max(current, 1) * value
            current = 0
        else:
            current += value

    result = total + current
    return float(result) if result else None


def _mask_dates(text: str) -> str:
    text = re.sub(r"\b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b", " ", text)

    months = (
        "January|February|March|April|May|June|July|August|"
        "September|October|November|December"
    )
    text = re.sub(
        rf"\b\d{{1,2}}\s+(?:{months})\s+\d{{4}}\b",
        " ",
        text,
        flags=re.IGNORECASE,
    )
    return text


def extract_amounts(text: str) -> list[float]:
    text = _mask_dates(text)
    amounts = []

    numeric_pattern = re.compile(
        r"(?<!\w)(?:₹|rs\.?|inr)?\s*(\d[\d,]*(?:\.\d+)?)(?!\w)",
        re.IGNORECASE,
    )

    for match in numeric_pattern.finditer(text):
        raw = match.group(1).replace(",", "")
        value = float(raw)
        amounts.append(int(value) if value.is_integer() else value)

    word_pattern = re.compile(
        r"\b((?:zero|one|two|three|four|five|six|seven|eight|nine|ten|"
        r"hundred|thousand|lakh)(?:\s+(?:zero|one|two|three|four|five|"
        r"six|seven|eight|nine|ten|hundred|thousand|lakh))*)"
        r"(?:\s+rupees?)?\b",
        re.IGNORECASE,
    )

    for match in word_pattern.finditer(text):
        value = _words_to_number(match.group(1))
        if value is not None:
            value = int(value) if value.is_integer() else value
            amounts.append(value)

    return amounts
