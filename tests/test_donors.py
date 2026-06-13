import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_create_donor():

    response = client.post("/donors/", params={
        "blood_type": "O+",
        "location": "Nairobi",
        "user_id": 1
    })

    assert response.status_code == 200
    data = response.json()
    assert data["blood_type"] == "O+"
    assert data["location"] == "Nairobi"
    assert "id" in data


def test_get_donors():

    response = client.get("/donors/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

    response_filtered = client.get("/donors/", params={"blood_type": "O+"})
    assert response_filtered.status_code == 200
