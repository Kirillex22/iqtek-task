from typing import Optional

from sqlmodel import SQLModel, Field


class UserORM(SQLModel, table=True):
    __tablename__ = "user"

    id: str = Field(primary_key=True)
    full_name: Optional[str] = Field(default=None, nullable=True)
