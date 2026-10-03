"""Output normalization utilities."""

from decimal import Decimal


def normalize_amount(value):
    if value is None or value == "":
        return None

    if isinstance(value, str):
        value = value.replace(",", "").replace("₹", "").strip()

    number = Decimal(str(value))
    return int(number) if number == number.to_integral() else float(number)


def normalize_crop(crop: str | None) -> str | None:
    if not crop:
        return None
    return crop.strip().lower()


def normalize_activity(activity: str | None) -> str | None:
    if not activity:
        return None
    return activity.strip().lower()
