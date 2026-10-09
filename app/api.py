from __future__ import annotations

import json
from typing import Any

from fastapi import FastAPI, HTTPException, Request

from app.nlp.expense_extractor import ExpenseExtractor

app = FastAPI(
    title="KisanVoice API",
    version="1.0.0",
    description="Extract transaction details from farmer statements.",
)

extractor = ExpenseExtractor()


def serialize_transaction(record: dict[str, Any]) -> dict[str, Any]:
    return {
        "subject": record.get("crop"),
        "verb": record.get("activity"),
        "transaction_amount": record.get("amount"),
        "transaction_date": record.get("date"),
    }


@app.get("/health")
def healthcheck() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/extract_transaction")
async def extract_transaction(request: Request):
    raw_body = await request.body()

    if not raw_body:
        raise HTTPException(status_code=400, detail="A non-empty input string is required.")

    try:
        payload = json.loads(raw_body.decode("utf-8"))
    except (TypeError, ValueError):
        payload = raw_body.decode("utf-8")

    if isinstance(payload, str):
        text = payload
    elif isinstance(payload, dict):
        text = payload.get("text") or payload.get("input") or payload.get("statement")
    else:
        text = None

    if not isinstance(text, str) or not text.strip():
        raise HTTPException(status_code=400, detail="A non-empty input string is required.")

    records = extractor.extract(text)
    if not records:
        raise HTTPException(status_code=404, detail="No transaction found for the supplied statement.")

    transactions = [serialize_transaction(record) for record in records]

    if len(transactions) == 1:
        return transactions[0]
    return transactions
