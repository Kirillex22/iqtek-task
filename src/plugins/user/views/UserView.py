from uuid import UUID

from pydantic import BaseModel


class UserView(BaseModel):
    id: UUID
    full_name: str