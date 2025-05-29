from dataclasses import dataclass
from uuid import UUID


@dataclass
class UserDTO:
    id: UUID
    full_name: str