from typing import Optional

from sqlmodel import SQLModel, Field


class UserORM(SQLModel, table=True):
    __tablename__ = "user"

    id: int | None = Field(default=None, primary_key=True)
    full_name: Optional[str] = Field(default=None, nullable=True)
