import json as Json
from unittest.mock import MagicMock

import pytest
from fastapi.testclient import TestClient
from redis import Redis
from sqlalchemy.exc import IntegrityError
from sqlmodel import Session

from config.Config import Config
from dependencies import get_uow
from infrastructure.UnitOfWorkProvider import UnitOfWorkProvider
from main import app
from repositories.postgres.orm.UserORM import UserORM


def make_app_client(config, client) -> TestClient:
    uow_provider = UnitOfWorkProvider(config, client=client)
    app.dependency_overrides[get_uow] = lambda: uow_provider.get_uow()
    return TestClient(app)


@pytest.fixture(params=["redis", "postgresql"])
def input_data(request):
    client, config = None, None
    if request.param == "redis":
        client = MagicMock(spec=Redis)
        config = Config(db_type="redis")
    elif request.param == "postgresql":
        client = MagicMock(spec=Session)
        config = Config(db_type="postgresql")

    return make_app_client(config, client), client


def test_create_user_success(input_data):
    app_client, client = input_data

    if isinstance(client, Redis):
        client.set.return_value = None
        client.exists.return_value = False

    if isinstance(client, Session):
        client.add.return_value = None
        client.commit.return_value = None
        client.rollback.return_value = None

    response = app_client.post(
        "/users/",
        json={
            "id": "123",
            "full_name": "John Dow"
        }
    )

    assert response.status_code == 201


def test_create_already_created_user(input_data):
    app_client, client = input_data

    if isinstance(client, Redis):
        client.set.return_value = None
        client.exists.return_value = True

    if isinstance(client, Session):
        client.add.return_value = None
        client.commit.side_effect = IntegrityError(statement=None, params=None, orig=None)
        client.rollback.return_value = None

    response = app_client.post(
        "/users/",
        json={
            "id": "123",
            "full_name": "John Dow"
        }
    )

    assert response.status_code == 409


def test_get_user_success(input_data):
    response_json = {"id": "123", "full_name": "John Dow"}

    app_client, client = input_data

    if isinstance(client, Redis):
        client.get.return_value = Json.dumps(response_json)
        client.exists.return_value = False

    if isinstance(client, Session):
        mock_result = MagicMock()
        mock_result.first.return_value = UserORM(**response_json)
        client.exec.return_value = mock_result
        client.commit.return_value = None
        client.rollback.return_value = None

    response = app_client.get("/users/123")

    assert response.status_code == 200
    assert response.json() == response_json


def test_get_not_existing_user(input_data):
    app_client, client = input_data

    if isinstance(client, Redis):
        client.get.return_value = None
        client.exists.return_value = False

    if isinstance(client, Session):
        mock_result = MagicMock()
        mock_result.first.return_value = None
        client.exec.return_value = mock_result
        client.commit.return_value = None
        client.rollback.return_value = None

    response = app_client.get("/users/123")

    assert response.status_code == 404


def test_update_user_success(input_data):
    app_client, client = input_data

    existing_entity_json = {"id": "123", "full_name": "John Dow"}
    to_update_json = {"id": "123", "full_name": "Jane Dow"}

    if isinstance(client, Redis):
        client.get.return_value = Json.dumps(existing_entity_json)
        client.exists.return_value = True

    if isinstance(client, Session):
        mock_result = MagicMock()
        mock_result.first.return_value = UserORM(**existing_entity_json)
        client.exec.return_value = mock_result
        client.commit.return_value = None
        client.rollback.return_value = None

    response = app_client.put(
        "/users/",
        json=to_update_json
    )

    assert response.status_code == 200


def test_update_not_existing_user(input_data):
    app_client, client = input_data

    to_update_json = {"id": "123", "full_name": "Jane Dow"}

    if isinstance(client, Redis):
        client.get.return_value = None
        client.exists.return_value = False

    if isinstance(client, Session):
        mock_result = MagicMock()
        mock_result.first.return_value = None
        client.exec.return_value = mock_result
        client.commit.return_value = None
        client.rollback.return_value = None

    response = app_client.put(
        "/users/",
        json=to_update_json
    )

    assert response.status_code == 404


def test_delete_user_success(input_data):
    app_client, client = input_data
    example_user = {"id": "123", "full_name": "John Dow"}

    if isinstance(client, Redis):
        client.exists.return_value = True
        client.delete.return_value = 1

    if isinstance(client, Session):
        mock_result = MagicMock()
        mock_result.first.return_value = UserORM(**example_user)
        client.exec.return_value = mock_result
        client.commit.return_value = None
        client.rollback.return_value = None
        client.delete.return_value = None

    response = app_client.delete("/users/123")

    assert response.status_code == 204


def test_delete_not_existing_user(input_data):
    app_client, client = input_data
    example_user = {"id": "123", "full_name": "John Dow"}

    if isinstance(client, Redis):
        client.exists.return_value = False
        client.delete.return_value = 0

    if isinstance(client, Session):
        mock_result = MagicMock()
        mock_result.first.return_value = None
        client.exec.return_value = mock_result
        client.commit.return_value = None
        client.rollback.return_value = None
        client.delete.return_value = None

    response = app_client.delete("/users/123")

    assert response.status_code == 404
