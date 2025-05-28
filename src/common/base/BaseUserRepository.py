from abc import ABC, abstractmethod

from src.plugins.user.dto.CreateUserDTO import CreateUserDTO
from src.plugins.user.dto.UserDTO import UserDTO
from src.plugins.user.entities.User import User


class BaseUserRepository(ABC):
    @abstractmethod
    def create_user(self, user: CreateUserDTO) -> UserDTO:
        raise NotImplementedError()

    @abstractmethod
    def update_user(self, user: User) -> UserDTO:
        raise NotImplementedError()

    @abstractmethod
    def get_user(self, user_id: int) -> UserDTO:
        raise NotImplementedError()

    @abstractmethod
    def delete_user(self, user: User) -> None:
        raise NotImplementedError()
