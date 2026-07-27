from fastapi import FastAPI
from pydantic import BaseModel, Field


app = FastAPI(title="nexai-demo-incident-service")


class QuoteRequest(BaseModel):
    subtotal: float
    discount_percent: float
    tax_percent: float


class QuoteResponse(BaseModel):
    subtotal: float
    discount_percent: float
    tax_percent: float
    total: float


class ValidationResponse(BaseModel):
    valid: bool
    errors: list[str] = []


@app.get("/healthz")
def healthz() -> dict[str, bool]:
    return {"ok": True}


@app.post("/orders/quote", response_model=QuoteResponse)
def create_quote(order: QuoteRequest) -> QuoteResponse:
    discounted_subtotal = order.subtotal * (1 - order.discount_percent / 100)
    total = discounted_subtotal * (1 + order.tax_percent / 100)

    return QuoteResponse(
        subtotal=order.subtotal,
        discount_percent=order.discount_percent,
        tax_percent=order.tax_percent,
        total=round(total, 2),
    )


@app.post("/orders/validate", response_model=ValidationResponse)
def validate_order(order: QuoteRequest) -> ValidationResponse:
    errors = []

    if order.subtotal < 0:
        errors.append("subtotal must be non-negative")
    if not (0 <= order.discount_percent <= 100):
        errors.append("discount_percent must be between 0 and 100")
    if order.tax_percent < 0:
        errors.append("tax_percent must be non-negative")

    return ValidationResponse(valid=len(errors) == 0, errors=errors)
