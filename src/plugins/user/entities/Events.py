from dataclasses import dataclass
from uuid import UUID


@dataclass
class BaseUserEvent:
    pass

@dataclass
class UserCreatedEvent(BaseUserEvent):
    id: UUID

@dataclass
class UserUpdatedEvent(BaseUserEvent):
    id: UUID
    full_name: str
    old_full_name: str

@dataclass
class UserDeletedEvent(BaseUserEvent):
    id: UUID
    full_name: str

