from dataclasses import dataclass
from uuid import UUID


@dataclass
class UpdateUserDTO:
    id: UUID
    full_name: str