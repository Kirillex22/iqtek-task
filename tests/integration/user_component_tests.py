import uuid
import pytest
import httpx

BASE_URL = "http://127.0.0.1:8000"

test_user_create = {
    "full_name": "Test User Name"
}

test_user_update = {
    "full_name": "Updated User Name"
}

@pytest.fixture(scope="function")
async def create_user():
    async with httpx.AsyncClient(base_url=BASE_URL) as client:
        response = await client.post("/users/", json=test_user_create)
        assert response.status_code == 200
        user = response.json()
        return user

@pytest.mark.asyncio
async def test_create_user_success():
    async with httpx.AsyncClient(base_url=BASE_URL) as client:
        response = await client.post("/users/", json=test_user_create)
        assert response.status_code == 200
        data = response.json()
        assert "id" in data
        await client.delete(f"/users/{data['id']}")

@pytest.mark.asyncio
async def test_get_user_success(create_user):
    user = await create_user
    user_id = user['id']
    async with httpx.AsyncClient(base_url=BASE_URL) as client:
        response = await client.get(f"/users/{user_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == user_id

@pytest.mark.asyncio
async def test_get_user_not_found():
    fake_id = str(uuid.uuid4())
    async with httpx.AsyncClient(base_url=BASE_URL) as client:
        response = await client.get(f"/users/{fake_id}")
        assert response.status_code == 404

@pytest.mark.asyncio
async def test_update_user_success(create_user):
    user = await create_user
    user_id = user['id']
    update_payload = test_user_update.copy()
    update_payload["id"] = user_id
    async with httpx.AsyncClient(base_url=BASE_URL) as client:
        response = await client.put(f"/users/?user_id={user_id}", json=update_payload)
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == user_id

@pytest.mark.asyncio
async def test_update_user_not_found():
    update_payload = test_user_update.copy()
    user_id = uuid.uuid4()
    async with httpx.AsyncClient(base_url=BASE_URL) as client:
        response = await client.put(f"/users/?user_id={user_id}", json=update_payload)
        assert response.status_code == 404

@pytest.mark.asyncio
async def test_delete_user_success(create_user):
    user = await create_user
    user_id = user['id']
    async with httpx.AsyncClient(base_url=BASE_URL) as client:
        response = await client.delete(f"/users/{user_id}")
        assert response.status_code == 201

        response = await client.get(f"/users/{user_id}")
        assert response.status_code == 404

@pytest.mark.asyncio
async def test_delete_user_not_found():
    fake_id = str(uuid.uuid4())
    async with httpx.AsyncClient(base_url=BASE_URL) as client:
        response = await client.delete(f"/users/{fake_id}")
        assert response.status_code == 404