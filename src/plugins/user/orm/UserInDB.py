from dataclasses import dataclass
from uuid import UUID


@dataclass
class UserInDB:
    id: UUID
    full_name: str