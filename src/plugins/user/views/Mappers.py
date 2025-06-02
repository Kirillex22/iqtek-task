from uuid import UUID

from src.plugins.user.dto.CreateUserDTO import CreateUserDTO
from src.plugins.user.dto.UpdateUserDTO import UpdateUserDTO
from src.plugins.user.dto.UserDTO import UserDTO
from src.plugins.user.entities.User import User
from src.plugins.user.views.UpdateUserView import UpdateUserView
from src.plugins.user.views.CreateUserView import CreateUserView
from src.plugins.user.views.UserView import UserView


def map_user_model_to_user_view(user: User):
    return UserView(id=user.id, full_name=user.full_name)

def map_user_dto_to_user_view(user_dto: UserDTO):
    return UserView(id=user_dto.id, full_name=user_dto.full_name)

def map_create_user_view_to_dto(user: CreateUserView):
    return CreateUserDTO(full_name=user.full_name)

def map_update_user_view_to_dto(user_id: UUID, user: UpdateUserView):
    return UpdateUserDTO(id=user_id, full_name=user.full_name)