
"""Main KisanVoice agricultural expense extraction pipeline."""

from datetime import datetime

from app.config import DEFAULT_REFERENCE_DATE
from app.nlp.preprocessing import clean_text
from app.nlp.crop_extractor import extract_crops
from app.nlp.activity_extractor import extract_activities
from app.nlp.amount_extractor import extract_amounts
from app.nlp.date_extractor import extract_date


class ExpenseExtractor:
    def __init__(self, reference_date: datetime | None = None):
        self.reference_date = reference_date or DEFAULT_REFERENCE_DATE

    def extract(self, text: str) -> list[dict]:
        text = clean_text(text)

        crops = extract_crops(text)
        activities = extract_activities(text)
        amounts = extract_amounts(text)
        date = extract_date(text, self.reference_date)

        # Clearly irrelevant input.
        if not crops and not activities and not amounts:
            return []

        # Generic field expense: preserve amount but do not invent an activity.
        if not activities and not crops and amounts:
            if "field" in text.lower():
                return [{
                    "crop": None,
                    "activity": None,
                    "amount": amounts[0],
                    "date": date,
                }]
            return []

        records = []

        # Multiple crops + matching number of amounts:
        # create one record per crop/amount pair.
        if len(crops) > 1 and len(crops) == len(amounts):
            for crop, amount in zip(crops, amounts):
                activity = activities[0] if activities else None
                records.append({
                    "crop": crop,
                    "activity": activity,
                    "amount": amount,
                    "date": date,
                })
            return records

        crop = crops[0] if crops else None

        # No recognized activity: preserve crop and/or amount.
        if not activities:
            for amount in amounts or [None]:
                records.append({
                    "crop": crop,
                    "activity": None,
                    "amount": amount,
                    "date": date,
                })
            return records

        # One activity and multiple amounts.
        if len(activities) == 1:
            for amount in amounts or [None]:
                records.append({
                    "crop": crop,
                    "activity": activities[0],
                    "amount": amount,
                    "date": date,
                })
            return records

        # Multiple activities and matching amounts.
        if len(activities) == len(amounts):
            for activity, amount in zip(activities, amounts):
                records.append({
                    "crop": crop,
                    "activity": activity,
                    "amount": amount,
                    "date": date,
                })
            return records

        # Best-effort alignment without inventing extra records.
        for index, activity in enumerate(activities):
            amount = amounts[index] if index < len(amounts) else None
            records.append({
                "crop": crop,
                "activity": activity,
                "amount": amount,
                "date": date,
            })

        return records
