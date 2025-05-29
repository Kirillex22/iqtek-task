from abc import ABC, abstractmethod
from uuid import UUID
from src.plugins.user.dto.UserDTO import UserDTO
from src.plugins.user.entities.User import User


class BaseUserRepository(ABC):
    @abstractmethod
    def create_user(self, user: User) -> UserDTO:
        raise NotImplementedError()

    @abstractmethod
    def update_user(self, user: User) -> UserDTO:
        raise NotImplementedError()

    @abstractmethod
    def get_user(self, user_id: UUID) -> UserDTO:
        raise NotImplementedError()

    @abstractmethod
    def delete_user(self, user: User) -> None:
        raise NotImplementedError()
