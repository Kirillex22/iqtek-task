from typing import Optional

from pydantic import BaseModel


class User(BaseModel):
    id: str
    full_name: Optional[str]
