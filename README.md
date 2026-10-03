# KisanVoice – Red Chilli Expense Extraction

A modular NLP prototype for extracting agricultural expense information from
farmer voice-to-text statements.

## Extracted fields

- Crop
- Activity
- Amount
- Date

## Project structure

```text
KisanVoice/
├── app/
│   ├── config.py
│   ├── nlp/
│   │   ├── preprocessing.py
│   │   ├── crop_extractor.py
│   │   ├── activity_extractor.py
│   │   ├── amount_extractor.py
│   │   └── date_extractor.py
│   └── utils/
│       └── normalizer.py
├── tests/
│   ├── test_cases.csv
│   ├── test_expense_extractor.py
│   └── test_runner.py
├── data/
│   ├── input/
│   └── output/
├── models/
├── main.py
└── requirements.txt
```

## Setup

```bash
python -m venv .venv
```

### macOS/Linux

```bash
source .venv/bin/activate
```

### Windows

```bash
.venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## Run the application

From the KisanVoice directory:

```bash
python main.py
```

Example:

```text
Farmer statement:
Today I spent 5000 for spraying pesticides and 10000 for labour for deweeding in my chilli crop.
```

Expected structure:

```json
[
  {
    "crop": "chilli",
    "activity": "pesticide spraying",
    "amount": 5000,
    "date": "01/10/2026"
  },
  {
    "crop": "chilli",
    "activity": "deweeding",
    "amount": 10000,
    "date": "01/10/2026"
  }
]
```

## Run tests

```bash
python tests/test_runner.py
```

The JSON test report is written to:

```text
data/output/test_report.json
```

## Important

This is a rule-based baseline. It is intentionally modular so that a
spaCy/NER model can later replace individual extractors without changing
the application interface.
