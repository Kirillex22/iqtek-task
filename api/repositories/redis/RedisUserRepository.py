from typing import Optional

from redis.asyncio import Redis

from domain.base.BaseUserRepository import BaseUserRepository
from domain.entities.User import User
from shared.exceptions.UserServiceExceptions import UserAlreadyExistsException, UserNotExistsException


class RedisUserRepository(BaseUserRepository):
    def __init__(self, redis: Redis, prefix: str = "user:"):
        self.redis = redis
        self.prefix = prefix

    async def _exists(self, key: str) -> bool:
        exists = bool(await self.redis.exists(key))
        return exists

    def _key(self, user_id: str) -> str:
        return f"{self.prefix}{user_id}"

    async def create_user(self, user: User) -> None:
        key = self._key(user.id)

        if self._exists(key):
            raise UserAlreadyExistsException(user)
        await self.redis.set(key, user.json())

    async def update_user(self, user: User) -> None:
        key = self._key(user.id)

        if not self._exists(key):
            raise UserNotExistsException(user.id)
        await self.redis.set(key, user.json())

    async def get_user(self, user_id: str) -> Optional[User]:
        key = self._key(user_id)
        data = await self.redis.get(key)
        if not data:
            return None
        return User.parse_raw(data)

    async def delete_user(self, user_id: str) -> None:
        key = self._key(user_id)

        if not self._exists(key):
            raise UserNotExistsException(user_id)
        await self.redis.delete(key)
