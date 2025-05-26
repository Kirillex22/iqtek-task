from src.config.Config import Config
from src.common.base.BaseUnitOfWork import BaseUnitOfWork
from src.plugins.user.services.UserService import UserService
from src.infrastructure.UnitOfWorkProvider import UnitOfWorkProvider
from src.common.exceptions.InfrastructureExceptions import ConfigurationException

try:
    config = Config.from_yaml("config.yaml")
    uow_provider = UnitOfWorkProvider(config)
except:
    raise ConfigurationException()


def get_uow() -> BaseUnitOfWork:
    return uow_provider.get_uow()


def get_user_service() -> UserService:
    return UserService()
