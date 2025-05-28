from pydantic import BaseModel


class CreateUserView(BaseModel):
    full_name: str