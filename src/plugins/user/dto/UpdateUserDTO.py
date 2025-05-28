from dataclasses import dataclass


@dataclass
class UpdateUserDTO:
    id: int
    full_name: str