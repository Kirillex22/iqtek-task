from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from src.common.base.BaseSessionFactory import BaseSessionFactory


class SQLAlchemySessionFactory(BaseSessionFactory):
    def __init__(self, db_url: str):
        self._engine = create_engine(db_url)

    def get_engine(self):
        return self._engine

    def get_session(self):
        return Session(self._engine)
