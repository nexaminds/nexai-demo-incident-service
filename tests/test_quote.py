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


def test_validate_valid_request() -> None:
    response = client.post(
        "/orders/validate",
        json={
            "subtotal": 100,
            "discount_percent": 10,
            "tax_percent": 5,
        },
    )

    assert response.status_code == 200
    assert response.json() == {"valid": True, "errors": []}


def test_validate_negative_subtotal() -> None:
    response = client.post(
        "/orders/validate",
        json={
            "subtotal": -10,
            "discount_percent": 10,
            "tax_percent": 5,
        },
    )

    assert response.status_code == 200
    data = response.json()
    assert data["valid"] is False
    assert "subtotal must be non-negative" in data["errors"]


def test_validate_invalid_discount() -> None:
    response = client.post(
        "/orders/validate",
        json={
            "subtotal": 100,
            "discount_percent": 150,
            "tax_percent": 5,
        },
    )

    assert response.status_code == 200
    data = response.json()
    assert data["valid"] is False
    assert "discount_percent must be between 0 and 100" in data["errors"]


def test_validate_negative_tax() -> None:
    response = client.post(
        "/orders/validate",
        json={
            "subtotal": 100,
            "discount_percent": 10,
            "tax_percent": -5,
        },
    )

    assert response.status_code == 200
    data = response.json()
    assert data["valid"] is False
    assert "tax_percent must be non-negative" in data["errors"]


def test_validate_multiple_errors() -> None:
    response = client.post(
        "/orders/validate",
        json={
            "subtotal": -10,
            "discount_percent": 150,
            "tax_percent": -5,
        },
    )

    assert response.status_code == 200
    data = response.json()
    assert data["valid"] is False
    assert len(data["errors"]) == 3
