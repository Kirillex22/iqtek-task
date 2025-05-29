import uuid

import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

userid = None

test_user_create = {
    "username": "testuser",
    "full_name": "Test User"
}

test_user_update = {
    "id": userid,
    "full_name": "Updated User"
}

@pytest.fixture(scope="module")
def create_user():
    global userid
    response = client.post("/users/", json=test_user_create)
    assert response.status_code == 200
    json = response.json()
    userid = json["id"]
    return json

def test_create_user_success():
    response = client.post("/users/", json=test_user_create)
    assert response.status_code == 200
    data = response.json()
    assert "id" in data

def test_get_user_success(create_user):
    user_id = create_user["id"]
    response = client.get(f"/users/{user_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == user_id

def test_get_user_not_found():
    response = client.get("/users/999999")
    assert response.status_code == 404

def test_update_user_success(create_user):
    user_id = create_user["id"]
    update_payload = test_user_update.copy()
    update_payload["id"] = user_id
    response = client.put("/users/", json=update_payload)
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == user_id

def test_update_user_not_found():
    update_payload = test_user_update.copy()
    update_payload["id"] = str(uuid.uuid4())
    response = client.put("/users/", json=update_payload)
    assert response.status_code == 404

def test_delete_user_success(create_user):
    user_id = create_user["id"]
    response = client.delete(f"/users/{user_id}")
    assert response.status_code == 201

    response = client.get(f"/users/{user_id}")
    assert response.status_code == 404

def test_delete_user_not_found():
    response = client.delete("/users/999999")
    assert response.status_code == 404