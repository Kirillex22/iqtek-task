import uuid
import json
import pytest

from src.common.exceptions.UserServiceExceptions import InvalidUserIdException, InvalidUserFullNameException
from src.plugins.user.entities.User import User


def test_user_creation():
    id = uuid.uuid4()
    full_name = 'name name name'
    user = User(id=id, full_name=full_name)

def test_user_creation_wrong_id():
    id = 1
    full_name = 'name name name'
    with pytest.raises(InvalidUserIdException) as e:
        User(id=id, full_name=full_name)

def test_user_creation_wrong_full_name():
    id = uuid.uuid4()
    full_name = 'name name'
    with pytest.raises(InvalidUserFullNameException) as e:
        User(id=id, full_name=full_name)

def test_user_creation_from_json():
    id = uuid.uuid4()
    full_name = 'name name name'
    _json = {'id': str(id), 'full_name': full_name}
    user = User.from_json(_json)

def test_user_parse_to_json():
    id = uuid.uuid4()
    full_name = 'name name name'
    _json = {'id': str(id), 'full_name': full_name}

    user = User(id, full_name)
    parsed = user.json()

    assert parsed == _json