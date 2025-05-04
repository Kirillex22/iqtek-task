from abc import ABC, abstractmethod
from typing import Optional

from domain.entities.User import User


class BaseUserRepository(ABC):
    @abstractmethod
    async def create_user(self, user: User) -> None:
        pass

    @abstractmethod
    async def update_user(self, user: User) -> None:
        pass

    @abstractmethod
    async def get_user(self, user_id: str) -> Optional[User]:
        pass

    @abstractmethod
    async def delete_user(self, user_id: str) -> None:
        pass
