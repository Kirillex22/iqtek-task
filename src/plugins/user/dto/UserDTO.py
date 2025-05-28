from dataclasses import dataclass


@dataclass
class UserDTO:
    id: int
    full_name: str