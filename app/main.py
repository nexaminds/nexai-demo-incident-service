from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, ValidationError
from fastapi.exceptions import RequestValidationError


app = FastAPI(title="nexai-demo-incident-service")


@app.exception_handler(RequestValidationError)
async def validation_error_handler(request: Request, exc: RequestValidationError):
    """Handle Pydantic validation errors with structured JSON response."""
    details = {}
    for error in exc.errors():
        field = ".".join(str(loc) for loc in error["loc"] if loc != "body")
        details[field] = {
            "message": error["msg"],
            "type": error["type"],
        }
    
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "error": "Invalid input",
            "details": details,
        },
    )


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """Handle general exceptions with a safe error message."""
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": "Internal server error",
            "details": {
                "message": "An unexpected error occurred",
            },
        },
    )


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
    discounted_subtotal = order.subtotal * (1 - order.discount_percent / 100)
    total = discounted_subtotal + order.tax_percent

    return QuoteResponse(
        subtotal=order.subtotal,
        discount_percent=order.discount_percent,
        tax_percent=order.tax_percent,
        total=round(total, 2),
    )
