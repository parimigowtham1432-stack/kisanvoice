import csv
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from app.api import app

BASE_DIR = Path(__file__).resolve().parent.parent
CSV_FILE = BASE_DIR / "tests" / "test_cases.csv"


def parse_expected_list(value: str):
    if not value:
        return []
    if ";" in value:
        return [item.strip() for item in value.split(";")]
    return [value.strip()]


def parse_amount_list(value: str):
    if not value:
        return []
    if ";" in value:
        return [float(item.strip()) for item in value.split(";")]
    return [float(value.strip())] if value.strip() else []


def normalize_result(payload):
    if isinstance(payload, list):
        return payload
    return [payload]


with CSV_FILE.open("r", encoding="utf-8", newline="") as source:
    CASES = list(csv.DictReader(source))


@pytest.mark.parametrize("row", CASES, ids=lambda row: row["test_case_id"])
def test_extract_transaction_endpoint(row):
    client = TestClient(app)
    response = client.post("/extract_transaction", json={"text": row["input_statement"]})

    if row["test_case_id"] == "TC029":
        assert response.status_code in {400, 404, 422}
        return

    assert response.status_code == 200, response.text

    payload = response.json()
    actual = normalize_result(payload)

    expected_subjects = parse_expected_list(row["expected_crop"])
    expected_verbs = parse_expected_list(row["expected_activity"])
    expected_amounts = parse_amount_list(row["expected_amount"])
    expected_dates = parse_expected_list(row["expected_date"])

    if expected_subjects:
        actual_subjects = [item.get("subject") for item in actual]
        assert all(subject in actual_subjects for subject in expected_subjects if subject)

    if expected_verbs:
        actual_verbs = [item.get("verb") for item in actual]
        assert all(verb in actual_verbs for verb in expected_verbs if verb)

    if expected_amounts:
        actual_amounts = [float(item.get("transaction_amount")) for item in actual if item.get("transaction_amount") is not None]
        assert sorted(expected_amounts) == sorted(actual_amounts)

    if expected_dates:
        actual_dates = [item.get("transaction_date") for item in actual if item.get("transaction_date") is not None]
        assert all(date in actual_dates for date in expected_dates if date)
