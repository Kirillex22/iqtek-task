from pydantic import BaseModel


class UpdateUserView(BaseModel):
    id: int
    full_name: str