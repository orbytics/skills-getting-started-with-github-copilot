from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data

def test_signup_and_remove_participant():
    test_email = "testuser@mergington.edu"
    activity = "Chess Club"
    # Sign up
    response = client.post(f"/activities/{activity}/signup?email={test_email}")
    assert response.status_code == 200
    assert f"Signed up {test_email}" in response.json()["message"]
    # Duplicate signup
    response = client.post(f"/activities/{activity}/signup?email={test_email}")
    assert response.status_code == 400
    # Remove participant
    response = client.delete(f"/activities/{activity}/signup?email={test_email}")
    assert response.status_code == 200
    assert f"Removed {test_email}" in response.json()["message"]
    # Remove again (should fail)
    response = client.delete(f"/activities/{activity}/signup?email={test_email}")
    assert response.status_code == 404

def test_signup_nonexistent_activity():
    response = client.post("/activities/NonexistentActivity/signup?email=someone@mergington.edu")
    assert response.status_code == 404

def test_remove_nonexistent_participant():
    response = client.delete("/activities/Chess Club/signup?email=notfound@mergington.edu")
    assert response.status_code == 404
