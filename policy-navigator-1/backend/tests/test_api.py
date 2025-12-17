from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_interpret_policy():
    response = client.post("/api/policies/interpret", json={"policy_text": "Sample policy text"})
    assert response.status_code == 200
    assert "structured_rules" in response.json()

def test_check_eligibility():
    response = client.post("/api/eligibility/check", json={"credentials": {"income": 50000, "state": "CA"}})
    assert response.status_code == 200
    assert "eligible" in response.json()

def test_match_benefits():
    response = client.post("/api/benefits/match", json={"credentials": {"income": 50000, "state": "CA"}})
    assert response.status_code == 200
    assert "benefits" in response.json()