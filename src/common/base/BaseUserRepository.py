from abc import ABC, abstractmethod
from typing import Set
from uuid import UUID
from src.plugins.user.entities.User import User


class BaseUserRepository(ABC):
    def __init__(self):
        self.seen: Set[User] = set()

    @abstractmethod
    def create_user(self, user: User) -> User:
        raise NotImplementedError()

    @abstractmethod
    def update_user(self, user: User) -> User:
        raise NotImplementedError()

    @abstractmethod
    def get_user(self, user_id: UUID) -> User:
        raise NotImplementedError()

    @abstractmethod
    def delete_user(self, user: User) -> None:
        raise NotImplementedError()
