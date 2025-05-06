from domain.entities.User import User
from repositories.postgres.orm.UserORM import UserORM


def map_user_model_to_orm(user: User) -> UserORM:
    return UserORM(**user.dict())


def map_user_orm_to_model(user_orm: UserORM) -> User:
    return User(**user_orm.dict())
