"""Detailed terminal test runner for KisanVoice expense extraction."""

import csv
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from app.config import DEFAULT_REFERENCE_DATE
from app.nlp.expense_extractor import ExpenseExtractor

CSV_FILE = ROOT / "tests" / "test_cases.csv"
REFERENCE_DATE = DEFAULT_REFERENCE_DATE
extractor = ExpenseExtractor(reference_date=REFERENCE_DATE)


def fmt(value):
    if value is None or value == "":
        return "NULL"
    return str(value)


def main():
    with CSV_FILE.open("r", encoding="utf-8", newline="") as file:
        rows = list(csv.DictReader(file))

    total = len(rows)
    passed = 0
    failed = 0

    print("=" * 100)
    print("KISANVOICE - DETAILED TEST CASE REPORT")
    print("=" * 100)
    print(f"Total Test Cases : {total}")
    print(f"Reference Date   : {REFERENCE_DATE.strftime('%d/%m/%Y')}")
    print("=" * 100)

    for index, row in enumerate(rows, start=1):
        test_id = row["test_case_id"]
        actual = extractor.extract(row["input_statement"])

        expected_crop = row["expected_crop"] or "NULL"
        expected_activity = row["expected_activity"] or "NULL"
        expected_amount = row["expected_amount"] or "NULL"
        expected_date = row["expected_date"] or "NULL"

        actual_records = []
        for record in actual:
            actual_records.append(
                f"crop={fmt(record.get('crop'))}, "
                f"activity={fmt(record.get('activity'))}, "
                f"amount={fmt(record.get('amount'))}, "
                f"date={fmt(record.get('date'))}"
            )

        # Run the authoritative pytest-style validation for this case by
        # reproducing the same field comparisons used by test_expense_extractor.
        case_pass = True

        if test_id == "TC029":
            case_pass = len(actual) == 0
        else:
            expected_crops = [x.strip() for x in expected_crop.split(";") if x.strip() and x != "NULL"]
            expected_activities = [x.strip() for x in expected_activity.split(";") if x.strip() and x != "NULL"]
            expected_amounts = [float(x.strip()) for x in expected_amount.split(";") if x.strip() and x != "NULL"]

            actual_crops = [r["crop"] for r in actual if r.get("crop") is not None]
            actual_activities = [r["activity"] for r in actual if r.get("activity") is not None]
            actual_amounts = [float(r["amount"]) for r in actual if r.get("amount") is not None]
            actual_dates = [r["date"] for r in actual if r.get("date") is not None]

            if expected_crops and not all(c in actual_crops for c in expected_crops):
                case_pass = False
            if expected_activities and not all(a in actual_activities for a in expected_activities):
                case_pass = False
            if expected_amounts and sorted(expected_amounts) != sorted(actual_amounts):
                case_pass = False
            if expected_date != "NULL" and expected_date not in actual_dates:
                case_pass = False

        if case_pass:
            passed += 1
            result = "PASS"
        else:
            failed += 1
            result = "FAIL"

        print(f"\n[{index:02d}/{total:02d}] {test_id} | {row['test_type']} | {row['crop_stage']}")
        print(f"INPUT              : {row['input_statement']}")
        print(f"EXPECTED CROP      : {expected_crop}")
        print(f"EXPECTED ACTIVITY  : {expected_activity}")
        print(f"EXPECTED AMOUNT    : {expected_amount}")
        print(f"EXPECTED DATE      : {expected_date}")

        if actual_records:
            print("ACTUAL RECORDS     :")
            for record_no, record in enumerate(actual_records, start=1):
                print(f"  {record_no}. {record}")
        else:
            print("ACTUAL RECORDS     : No records")

        print(f"RESULT             : {result}")

    pass_rate = (passed / total * 100) if total else 0

    print("\n" + "=" * 100)
    print("TEST SUMMARY")
    print("=" * 100)
    print(f"Total Test Cases   : {total}")
    print(f"Passed             : {passed}")
    print(f"Failed             : {failed}")
    print(f"Pass Rate          : {pass_rate:.2f}%")
    print("=" * 100)

    if failed:
        print("TEST RESULT: FAIL")
        return 1

    print("TEST RESULT: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
