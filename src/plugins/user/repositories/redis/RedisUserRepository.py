from typing import Optional
from redis import Redis

from src.common.base.BaseUserRepository import BaseUserRepository
from src.common.exceptions.UserServiceExceptions import UserNotExistsException
from src.plugins.user.dto.UserDTO import UserDTO as User, UserDTO
from src.plugins.user.dto.CreateUserDTO import CreateUserDTO

class RedisUserRepository(BaseUserRepository):
    def __init__(self, redis: Redis, counter_key: str = "user:id:counter", prefix: str = "user:"):
        self.redis = redis
        self.prefix = prefix
        self.counter_key = counter_key  # ключ для счётчика в Redis

    # def _key(self, user_id: int) -> str:
    #     return f"{self.prefix}{user_id}"
    #
    # def create_user(self, user: CreateUserDTO) -> UserDTO:
    #     user_id = self.redis.incr(self.counter_key)
    #     user.id = user_id
    #
    #     key = self._key(user.id)
    #     self.redis.set(key, user.json())
    #
    #     saved_user = self.redis.get(key)
    #     return UserDTO(**saved_user)
    #
    # def update_user(self, user: User) -> UserDTO:
    #     key = self._key(user.id)
    #
    #     if not self._exists(key):
    #         raise UserNotExistsException(user.id)
    #
    #     self.redis.set(key, user.json())
    #     saved_user = self.redis.get(key)
    #     return UserDTO(**saved_user)
    #
    # def get_user(self, user_id: int) -> Optional[User]:
    #     key = self._key(user_id)
    #     user_data = self.redis.get(key)
    #
    #     if user_data is None:
    #         raise UserNotExistsException(user_id)
    #
    #     return UserDTO(**user_data)
    #
    # def delete_user(self, user_id: int) -> None:
    #     key = self._key(user_id)
    #
    #     if not self._exists(key):
    #         raise UserNotExistsException(user_id)
    #
    #     self.redis.delete(key)
    #
    # def _exists(self, key: str) -> bool:
    #     return self.redis.exists(key) == 1