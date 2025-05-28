from sqlalchemy import Table, Column, Integer, String
from sqlalchemy.orm import registry

from src.plugins.user.entities.User import User

mapper_registry = registry()

user_table = Table(
    'users', mapper_registry.metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('full_name', String(255)),
 )

def register_map(engine):
    mapper_registry.map_imperatively(User, user_table)
    mapper_registry.metadata.create_all(engine)