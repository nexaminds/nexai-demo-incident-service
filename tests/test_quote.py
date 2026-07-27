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


def test_quote_validation_error_discount_too_high() -> None:
    response = client.post(
        "/orders/quote",
        json={
            "subtotal": 100,
            "discount_percent": 150,
            "tax_percent": 5,
        },
    )

    assert response.status_code == 422
    data = response.json()
    assert data["error"] == "Invalid input"
    assert "discount_percent" in data["details"]


def test_quote_validation_error_negative_subtotal() -> None:
    response = client.post(
        "/orders/quote",
        json={
            "subtotal": -10,
            "discount_percent": 10,
            "tax_percent": 5,
        },
    )

    assert response.status_code == 422
    data = response.json()
    assert data["error"] == "Invalid input"
    assert "subtotal" in data["details"]


def test_quote_validation_error_missing_field() -> None:
    response = client.post(
        "/orders/quote",
        json={
            "subtotal": 100,
            "discount_percent": 10,
        },
    )

    assert response.status_code == 422
    data = response.json()
    assert data["error"] == "Invalid input"
    assert "tax_percent" in data["details"]
