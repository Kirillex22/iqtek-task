from abc import ABC, abstractmethod

from src.plugins.user.dto.GetUserDTO import GetUserDTO
from src.plugins.user.entities.User import User


class BaseUserRepository(ABC):
    @abstractmethod
    def create_user(self, user: User) -> User:
        pass

    @abstractmethod
    def update_user(self, user: User) -> User:
        pass

    @abstractmethod
    def get_user(self, get_model: GetUserDTO) -> User:
        pass

    @abstractmethod
    def delete_user(self, get_model: GetUserDTO) -> None:
        pass
