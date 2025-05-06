from abc import ABC, abstractmethod

from domain.base.BaseUserRepository import BaseUserRepository


class BaseUnitOfWork(ABC):
    user_repository: BaseUserRepository

    def __enter__(self) -> "BaseUnitOfWork":
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            self.rollback()
        else:
            self.commit()

    @abstractmethod
    def commit(self):
        pass

    @abstractmethod
    def rollback(self):
        pass
