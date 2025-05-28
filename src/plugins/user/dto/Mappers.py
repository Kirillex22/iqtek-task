from src.plugins.user.dto.CreateUserDTO import CreateUserDTO
from src.plugins.user.dto.UserDTO import UserDTO
from src.plugins.user.entities.User import User


def map_create_user_dto_to_user(user_to_create: CreateUserDTO) -> User:
    return User(id=None, full_name=user_to_create.full_name)

def map_user_to_user_dto(user: User) -> UserDTO:
    return UserDTO(id=user.id, full_name=user.full_name)

def map_user_dto_to_user(user: UserDTO) -> User:
    return User(id=user.id, full_name=user.full_name)