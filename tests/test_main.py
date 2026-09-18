from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_home():
    response = client.get("/")

    assert response.status_code == 200
    assert response.json()["status"] == "running"


def test_liveness():
    response = client.get("/health/live")

    assert response.status_code == 200
    assert response.json() == {"status": "alive"}


def test_readiness():
    response = client.get("/health/ready")

    assert response.status_code == 200
    assert response.json() == {"status": "ready"}


def test_create_order():
    response = client.post(
        "/orders",
        json={
            "product": "Laptop",
            "quantity": 2
        }
    )

    assert response.status_code == 201
    assert response.json()["product"] == "Laptop"
    assert response.json()["quantity"] == 2


def test_invalid_order():
    response = client.post(
        "/orders",
        json={
            "product": "L",
            "quantity": -1
        }
    )

    assert response.status_code == 422
