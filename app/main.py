from fastapi import FastAPI
from pydantic import BaseModel, Field


app = FastAPI(title="nexai-demo-incident-service")


class QuoteRequest(BaseModel):
    subtotal: float = Field(ge=0)
    discount_percent: float = Field(ge=0, le=100)
    tax_percent: float = Field(ge=0)


class QuoteResponse(BaseModel):
    subtotal: float
    discount_percent: float
    tax_percent: float
    total: float


@app.get("/healthz")
def healthz() -> dict[str, bool]:
    return {"ok": True}


@app.post("/orders/quote", response_model=QuoteResponse)
def create_quote(order: QuoteRequest) -> QuoteResponse:
    taxed_subtotal = order.subtotal + (order.subtotal * order.tax_percent / 100)
    discount_amount = order.subtotal * order.discount_percent / 100
    total = taxed_subtotal - discount_amount

    return QuoteResponse(
        subtotal=order.subtotal,
        discount_percent=order.discount_percent,
        tax_percent=order.tax_percent,
        total=round(total, 2),
    )
