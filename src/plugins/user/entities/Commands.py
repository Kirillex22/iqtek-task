from dataclasses import dataclass
from uuid import UUID

from src.plugins.user.dto.CreateUserDTO import CreateUserDTO


@dataclass
class BaseUserCommand:
    pass

@dataclass
class CreateUserCommand(CreateUserDTO, BaseUserCommand):
    pass

@dataclass
class SendMailNotificationCommand(BaseUserCommand):
    id: UUID
    text: str
