import csv
import json
from datetime import datetime
from pathlib import Path

from app.nlp.expense_extractor import ExpenseExtractor


BASE_DIR = Path(__file__).resolve().parent.parent
CSV_FILE = BASE_DIR / "tests" / "test_cases.csv"

extractor = ExpenseExtractor()


def parse_expected(value: str):
    if not value:
        return []
    if ";" in value:
        return [x.strip() for x in value.split(";")]
    return [value.strip()]


def parse_amounts(value: str):
    if not value:
        return []
    return [float(x.strip()) for x in value.split(";")]


def test_all_cases():
    failures = []

    with CSV_FILE.open("r", encoding="utf-8", newline="") as file:
        rows = list(csv.DictReader(file))

    for row in rows:
        actual = extractor.extract(row["input_statement"])

        expected_crop = parse_expected(row["expected_crop"])
        expected_activity = parse_expected(row["expected_activity"])
        expected_amount = parse_amounts(row["expected_amount"])
        expected_date = row["expected_date"]

        actual_crops = [r["crop"] for r in actual if r["crop"] is not None]
        actual_activities = [r["activity"] for r in actual if r["activity"] is not None]
        actual_amounts = [float(r["amount"]) for r in actual if r["amount"] is not None]
        actual_dates = [r["date"] for r in actual if r["date"] is not None]

        # Negative test case.
        if row["test_case_id"] == "TC029":
            if actual:
                failures.append({
                    "id": row["test_case_id"],
                    "expected": "No records",
                    "actual": actual,
                })
            continue

        # Compare expected values only where the test case defines them.
        if expected_crop and not all(c in actual_crops for c in expected_crop):
            failures.append({"id": row["test_case_id"], "field": "crop",
                             "expected": expected_crop, "actual": actual_crops})

        if expected_activity and not all(a in actual_activities for a in expected_activity):
            failures.append({"id": row["test_case_id"], "field": "activity",
                             "expected": expected_activity, "actual": actual_activities})

        if expected_amount:
            if sorted(expected_amount) != sorted(actual_amounts):
                failures.append({"id": row["test_case_id"], "field": "amount",
                                 "expected": expected_amount, "actual": actual_amounts})

        if expected_date:
            if expected_date not in actual_dates:
                failures.append({"id": row["test_case_id"], "field": "date",
                                 "expected": expected_date, "actual": actual_dates})

    result = {
        "total": len(rows),
        "passed": len(rows) - len(failures),
        "failed": len(failures),
        "failures": failures,
    }

    output = BASE_DIR / "data" / "output"
    output.mkdir(parents=True, exist_ok=True)
    (output / "test_report.json").write_text(
        json.dumps(result, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    assert not failures, json.dumps(failures, indent=2)


if __name__ == "__main__":
    test_all_cases()
    print("All test cases passed.")
