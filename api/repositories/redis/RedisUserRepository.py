from typing import Optional

from redis import Redis

from domain.base.BaseUserRepository import BaseUserRepository
from domain.entities.User import User
from shared.exceptions.UserServiceExceptions import UserAlreadyExistsException, UserNotExistsException


class RedisUserRepository(BaseUserRepository):
    def __init__(self, redis: Redis, prefix: str = "user:"):
        self.redis = redis
        self.prefix = prefix

    def _exists(self, key: str) -> bool:
        return bool(self.redis.exists(key))

    def _key(self, user_id: str) -> str:
        return f"{self.prefix}{user_id}"

    def create_user(self, user: User) -> None:
        key = self._key(user.id)

        if self._exists(key):
            raise UserAlreadyExistsException()
        self.redis.set(key, user.json())

    def update_user(self, user: User) -> None:
        key = self._key(user.id)

        if not self._exists(key):
            raise UserNotExistsException(user.id)
        self.redis.set(key, user.json())

    def get_user(self, user_id: str) -> Optional[User]:
        key = self._key(user_id)
        user = self.redis.get(key)

        if user is None:
            raise UserNotExistsException(user_id)

        return User.parse_raw(user)

    def delete_user(self, user_id: str) -> None:
        key = self._key(user_id)

        if not self._exists(key):
            raise UserNotExistsException(user_id)
        self.redis.delete(key)
