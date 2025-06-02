from enum import Enum
from typing import Optional

import yaml
from pydantic_settings import BaseSettings


class DBType(str, Enum):
    POSTGRESQL = "postgresql"
    REDIS = "redis"


class PostgresData(BaseSettings):
    username: str
    password: str
    host: str
    db_name: str

    def generate_url(self):
        return f"{DBType.POSTGRESQL}://{self.username}:{self.password}@{self.host}/{self.db_name}"


class RedisData(BaseSettings):
    host: str
    port: int
    db_idx: int
    password: Optional[str] = None

    def generate_url(self):
        return f"{DBType.REDIS}://{self.host}:{self.port}/{self.db_idx}"


class Config(BaseSettings):
    db_type: DBType
    postgres_data: Optional[PostgresData] = None
    redis_data: Optional[RedisData] = None

    @classmethod
    def from_yaml(cls, path: str) -> "Config":
        with open(path, "r") as file:
            config_data = yaml.safe_load(file)
            return cls(**config_data)
