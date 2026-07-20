from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_healthz_returns_ok() -> None:
    response = client.get("/healthz")

    assert response.status_code == 200
    assert response.json() == {"ok": True}


def test_quote_applies_discount_before_tax() -> None:
    response = client.post(
        "/orders/quote",
        json={
            "subtotal": 100,
            "discount_percent": 10,
            "tax_percent": 5,
        },
    )

    assert response.status_code == 200
    assert response.json()["total"] == 94.5
