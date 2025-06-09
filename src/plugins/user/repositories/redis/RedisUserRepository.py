from typing import Optional
from uuid import UUID
from redis import Redis
import json

from src.common.base.BaseUserRepository import BaseUserRepository
from src.common.exceptions.UserServiceExceptions import UserNotExistsException, UnknownUserException, \
    UserAlreadyExistsException
from src.plugins.user.entities.User import User

def to_json(user: User) -> dict:
    return {
        'id': str(user.id),
        'full_name': user.full_name
    }

def from_json(json: dict) -> User:
    id = UUID(json['id'])
    full_name = json['full_name']
    return User(id, full_name)

class RedisUserRepository(BaseUserRepository):
    def __init__(self, redis: Redis, prefix: str = "user:"):
        super().__init__()
        self.redis = redis
        self.prefix = prefix

    def _key(self, user_id: UUID) -> str:
        return f"{self.prefix}{user_id}"

    def create_user(self, user: User) -> User:
        key = self._key(user.id)
        try:
            if self.redis.exists(key):
                raise UserAlreadyExistsException()

            self.redis.set(key, json.dumps(to_json(user)))
            saved_user_raw = self.redis.get(key)
            if saved_user_raw is None:
                raise UnknownUserException()

            saved_user = from_json(json.loads(saved_user_raw))
            self.seen.add(saved_user)
            return saved_user
        except Exception as e:
            raise UnknownUserException() from e

    def update_user(self, user: User) -> User:
        key = self._key(user.id)
        if not self._exists(key):
            raise UserNotExistsException(user.id)

        try:
            self.redis.set(key, json.dumps(to_json(user)))
            saved_user_raw = self.redis.get(key)
            if saved_user_raw is None:
                raise UnknownUserException()

            saved_user = from_json(json.loads(saved_user_raw))
            self.seen.add(saved_user)
            return saved_user
        except Exception as e:
            raise UnknownUserException() from e

    def get_user(self, user_id: UUID) -> Optional[User]:
        key = self._key(user_id)
        user_data_raw = self.redis.get(key)
        if user_data_raw is None:
            return None

        user = from_json(json.loads(user_data_raw))
        self.seen.add(user)
        return user

    def delete_user(self, user: User) -> None:
        key = self._key(user.id)
        if not self._exists(key):
            raise UserNotExistsException(user.id)

        self.redis.delete(key)
        self.seen.add(user)

    def _exists(self, key: str) -> bool:
        return self.redis.exists(key) == 1