from typing import Optional

from pydantic import BaseModel


class User(BaseModel):
    id: int | None = None
    full_name: Optional[str]
