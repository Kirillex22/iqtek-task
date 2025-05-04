from abc import ABC, abstractmethod

from domain.base.BaseUserRepository import BaseUserRepository


class BaseUnitOfWork(ABC):
    user_repository: BaseUserRepository

    async def __aenter__(self) -> "BaseUnitOfWork":
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            await self.rollback()
        else:
            await self.commit()

    @abstractmethod
    async def commit(self):
        pass

    @abstractmethod
    async def rollback(self):
        pass