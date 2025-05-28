from typing import Optional

from redis import Redis

from src.common.base.BaseUserRepository import BaseUserRepository
from src.plugins.user.entities.User import User
from src.common.exceptions.UserServiceExceptions import UserAlreadyExistsException, UserNotExistsException


class RedisUserRepository(BaseUserRepository):
    def __init__(self, redis: Redis, prefix: str = "user:"):
        self.redis = redis
        self.prefix = prefix

    # def _exists(self, key: str) -> bool:
    #     return bool(self.redis.exists(key))
    #
    # def _key(self, user_id: int) -> str:
    #     return f"{self.prefix}{user_id}"
    #
    # def create_user(self, user: User) -> User:
    #     key = self._key(user.id)
    #
    #     if self._exists(key):
    #         raise UserAlreadyExistsException()
    #     self.redis.set(key, user.json())
    #     return User.parse_raw(self.redis.get(self._key(user.id)))
    #
    # def update_user(self, user: User) -> User:
    #     key = self._key(user.id)
    #
    #     if not self._exists(key):
    #         raise UserNotExistsException(user.id)
    #     self.redis.set(key, user.json())
    #     return User.parse_raw(self.redis.get(self._key(user.id)))
    #
    # def get_user(self, get_model: GetUserDTO) -> Optional[User]:
    #     user_id = get_model.id
    #     key = self._key(user_id)
    #     user = self.redis.get(key)
    #
    #     if user is None:
    #         raise UserNotExistsException(user_id)
    #
    #     return User.parse_raw(user)
    #
    # def delete_user(self, get_model: GetUserDTO) -> None:
    #     user_id = get_model.id
    #     key = self._key(user_id)
    #
    #     if not self._exists(key):
    #         raise UserNotExistsException(user_id)
    #     self.redis.delete(key)
