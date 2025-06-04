from dataclasses import dataclass
from uuid import UUID


@dataclass
class BaseUserEvent:
    pass

@dataclass
class UserCreatedEvent(BaseUserEvent):
    id: UUID

