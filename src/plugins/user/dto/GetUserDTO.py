from pydantic import BaseModel

class GetUserDTO(BaseModel):
    id: int