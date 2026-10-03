"""KisanVoice command-line interface."""

import json
from datetime import datetime
from app.nlp.expense_extractor import ExpenseExtractor


def main():
    print("=" * 65)
    print("KisanVoice - Agricultural Expense Extractor")
    print("=" * 65)

    text = input("Farmer statement: ").strip()

    extractor = ExpenseExtractor()
    results = extractor.extract(text)

    if not results:
        print("\nNo agricultural expense information detected.")
        return

    print("\nExtracted records:")
    print(json.dumps(results, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
