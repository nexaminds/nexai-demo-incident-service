# nexai-demo-incident-service

A tiny FastAPI service for demonstrating an incident flow around an order quote calculation.

## What The Service Does

- `GET /healthz` returns a basic health check response.
- `POST /orders/quote` accepts an order subtotal, discount percentage, and tax percentage, then returns a calculated quote total.

Example request:

```json
{
  "subtotal": 100,
  "discount_percent": 10,
  "tax_percent": 5
}
```

## Known Intentional Bug

The quote calculation intentionally contains a bug for a Claude Managed Agents demo.

Correct behavior should apply the tax percentage to the discounted subtotal:

```text
discounted_subtotal = subtotal - (subtotal * discount_percent / 100)
total = discounted_subtotal + (discounted_subtotal * tax_percent / 100)
```

This service currently adds `tax_percent` as a flat amount instead of calculating percentage-based tax, which causes the included pytest to fail.

## Install

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

On Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## Run

```bash
uvicorn app.main:app --reload
```

## Test

```bash
pytest
```
