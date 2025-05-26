from typing import Optional

from redis import Redis

from src.common.base.BaseSessionFactory import BaseSessionFactory


class RedisSessionFactory(BaseSessionFactory):
    def __init__(self, db_url: str, password: Optional[str] = None):
        self.client = Redis.from_url(db_url, password=password)