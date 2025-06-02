from pydantic import BaseModel


class UpdateUserView(BaseModel):
    full_name: str