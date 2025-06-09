from dataclasses import dataclass
from uuid import UUID

from src.plugins.user.dto.CreateUserDTO import CreateUserDTO
from src.plugins.user.dto.UpdateUserDTO import UpdateUserDTO


@dataclass
class BaseUserCommand:
    pass

@dataclass
class CreateUserCommand(CreateUserDTO, BaseUserCommand):
    pass

@dataclass
class UpdateUserCommand(UpdateUserDTO, BaseUserCommand):
    pass

@dataclass
class DeleteUserCommand(BaseUserCommand):
    id: UUID
