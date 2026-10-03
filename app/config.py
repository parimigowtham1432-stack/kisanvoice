"""Application configuration for KisanVoice."""

from datetime import datetime
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
INPUT_DIR = DATA_DIR / "input"
OUTPUT_DIR = DATA_DIR / "output"
MODEL_DIR = BASE_DIR / "models"

DEFAULT_DATE_FORMAT = "%d/%m/%Y"
DEFAULT_REFERENCE_DATE = datetime(2026, 10, 2)

# Common crop aliases. Extend this dictionary as your project grows.
CROP_ALIASES = {
    "mirchi": "chilli",
    "mirapakay": "chilli",
    "mirapakayalu": "chilli",
    "red chilli": "red chilli",
    "red chillies": "red chilli",
    "chilli": "chilli",
    "chillies": "chilli",
    "cotton": "cotton",
}

# Ordered from more specific to more general phrases.
ACTIVITY_ALIASES = {
    "pesticide spraying": [
        "pesticide spraying", "spraying pesticides", "pesticide spray",
        "spray pesticide", "spraying pesticide", "sprayed pesticide",
        "pesticides", "spraying"
    ],
    "fungicide spraying": [
        "fungicide spraying", "spraying fungicide", "fungicide spray"
    ],
    "deweeding": [
        "deweeding", "weeding", "removing weeds", "weed removal"
    ],
    "ploughing": ["ploughing", "plowing"],
    "land leveling": ["land leveling", "land levelling"],
    "seed purchase": ["seed purchase", "purchased seeds", "purchased chilli seeds", "purchased red chilli seeds", "bought seeds", "bought chilli seeds"],
    "seed treatment": ["seed treatment", "treating seeds", "treating chilli seeds"],
    "nursery preparation": ["nursery preparation", "prepare the nursery", "preparing the nursery", "prepare the chilli nursery"],
    "transplanting": ["transplanting", "transplanting seedlings", "planting seedlings"],
    "fertilizer": ["fertilizer", "fertiliser"],
    "fertilizer purchase": ["fertilizer purchase", "bought fertilizer", "bought fertiliser"],
    "irrigation": ["irrigation", "irrigating", "watering"],
    "labour": ["labour", "labor", "workers", "paid workers", "to workers"],
    "harvesting": ["harvesting", "harvest", "harvesting red chillies"],
    "sorting": ["sorting", "sort the harvested chillies"],
    "drying": ["drying", "dry the chillies"],
    "packing": ["packing", "pack the chillies"],
    "transportation": ["transportation", "transport", "transporting"],
    "selling": ["selling", "sold", "sale"],
    "field maintenance": ["field maintenance", "field work"],
}

RELATIVE_DATES = {
    "today": 0,
    "ee roju": 0,
    "yesterday": -1,
}
