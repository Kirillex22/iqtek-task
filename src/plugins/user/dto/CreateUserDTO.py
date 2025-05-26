from pydantic import BaseModel

class CreateUserDTO(BaseModel):
    full_name: str