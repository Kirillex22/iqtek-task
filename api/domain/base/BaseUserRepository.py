from abc import ABC, abstractmethod

from domain.entities.User import User


class BaseUserRepository(ABC):
    @abstractmethod
    def create_user(self, user: User) -> None:
        pass

    @abstractmethod
    def update_user(self, user: User) -> None:
        pass

    @abstractmethod
    def get_user(self, user_id: str) -> User:
        pass

    @abstractmethod
    def delete_user(self, user_id: str) -> None:
        pass
