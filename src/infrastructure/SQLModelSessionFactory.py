from sqlalchemy import create_engine
from sqlmodel import SQLModel, Session

from src.common.base.BaseSessionFactory import BaseSessionFactory


class SQLModelSessionFactory(BaseSessionFactory):
    def __init__(self, db_url: str):
        self._engine = create_engine(db_url)
        SQLModel.metadata.create_all(self._engine)

    def get_session(self):
        return Session(self._engine)
