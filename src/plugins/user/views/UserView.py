from pydantic import BaseModel


class UserView(BaseModel):
    id: int
    full_name: str