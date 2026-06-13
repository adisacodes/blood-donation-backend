from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to Blood Donation API 🩸"}

def test_get_dashboard_stats():
    response = client.get("/admin/dashboard")
    assert response.status_code == 200
    data = response.json()
    assert "totalDonors" in data
    assert "totalRequests" in data
    assert "pendingRequests" in data
    assert "approvedRequests" in data

def test_get_all_donors():
    response = client.get("/admin/donors")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_all_requests():
    response = client.get("/admin/requests")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_delete_donor_not_found():
    response = client.delete("/admin/donors/999")
    assert response.status_code == 404
