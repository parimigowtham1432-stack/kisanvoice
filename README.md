# KisanVoice – Agricultural Transaction Extraction API

KisanVoice is a rule-based NLP project that extracts agricultural transaction information from farmer statements. It can be run as a command-line utility or exposed as an HTTP API endpoint.

## API contract

Endpoint:

```http
POST http://localhost:8000/extract_transaction
```

Request body:

```json
{
  "text": "I paid 5000 rupees for pesticide spraying on my chilli crop today."
}
```

Successful response (single match):

```json
{
  "subject": "chilli",
  "verb": "pesticide spraying",
  "transaction_amount": 5000,
  "transaction_date": "02/10/2026"
}
```

Successful response (multiple matches):

```json
[
  {
    "subject": "chilli",
    "verb": "pesticide spraying",
    "transaction_amount": 5000,
    "transaction_date": "02/10/2026"
  },
  {
    "subject": "chilli",
    "verb": "deweeding",
    "transaction_amount": 10000,
    "transaction_date": "02/10/2026"
  }
]
```

If no transaction is found, the API responds with an HTTP 404 error.

## Project structure

```text
KisanVoice/
├── app/
│   ├── __init__.py
│   ├── api.py
│   ├── config.py
│   ├── nlp/
│   │   ├── preprocessing.py
│   │   ├── crop_extractor.py
│   │   ├── activity_extractor.py
│   │   ├── amount_extractor.py
│   │   ├── date_extractor.py
│   │   └── expense_extractor.py
│   └── utils/
│       └── normalizer.py
├── data/
│   ├── input/
│   └── output/
├── tests/
│   ├── test_api.py
│   ├── test_cases.csv
│   ├── test_expense_extractor.py
│   └── test_runner.py
├── main.py
├── README.md
├── requirements.txt
└── spec/
    └── api_spec.md
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

## Run the CLI locally

From the project root:

```bash
python main.py
```

Example input:

```text
Today I spent 5000 rupees for spraying pesticides and 10000 for labour for deweeding in my chilli crop.
```

## Run the API locally

Start the server:

```bash
uvicorn app.api:app --host 0.0.0.0 --port 8000 --reload
```

Then call the API:

```bash
curl -X POST http://localhost:8000/extract_transaction \
  -H "Content-Type: application/json" \
  -d '{"text":"I paid 5000 rupees for pesticide spraying on my chilli crop today."}'
```

Expected output:

```json
{
  "subject": "chilli",
  "verb": "pesticide spraying",
  "transaction_amount": 5000,
  "transaction_date": "02/10/2026"
}
```

## Deployment procedure

1. Ensure Python 3.11+ is installed.
2. Activate the virtual environment and install dependencies:

   ```bash
   python -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```

3. Start the application on a local machine:

   ```bash
   uvicorn app.api:app --host 0.0.0.0 --port 8000
   ```

4. For a production-style deployment, run the service behind a process manager such as `systemd`, Docker, or a reverse proxy such as Nginx.
5. Use the endpoint at `http://localhost:8000/extract_transaction` or the server IP address if deployed on a LAN.

## Run tests

### Rule-based extraction tests

```bash
python tests/test_runner.py
```

### API end-to-end tests

```bash
python -m pytest tests/test_api.py -q
```

The JSON test report is written to:

```text
data/output/test_report.json
```

## Important

This project is a rule-based baseline. It is intentionally structured so that individual extractors can be upgraded or replaced with spaCy/NER models without changing the public API contract.
