"""Text preprocessing and sentence splitting."""

import re


def clean_text(text: str) -> str:
    if not isinstance(text, str):
        raise TypeError("Input must be a string.")

    text = text.replace("\u00a0", " ")
    text = re.sub(r"\s+", " ", text).strip()
    return text


def split_expense_clauses(text: str) -> list[str]:
    """Split common multi-expense constructions.

    This is deliberately conservative. It preserves clauses connected with
    'and' when they are likely to represent separate expenses.
    """
    text = clean_text(text)

    # Common separators used before a second expense.
    patterns = [
        r"\s+and\s+(?=\d+(?:\.\d+)?\s*(?:rupees?|rs\.?|₹)|[a-z])",
        r"\s*,\s*(?=\d+(?:\.\d+)?\s*(?:rupees?|rs\.?|₹))",
    ]

    clauses = [text]
    for pattern in patterns:
        next_clauses = []
        for clause in clauses:
            pieces = re.split(pattern, clause, flags=re.IGNORECASE)
            next_clauses.extend(pieces)
        clauses = next_clauses

    return [c.strip(" ,.") for c in clauses if c.strip(" ,.")]
