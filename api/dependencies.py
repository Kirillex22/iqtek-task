from config.Config import Config
from domain.base.BaseUnitOfWork import BaseUnitOfWork
from domain.services.UserService import UserService
from infrastructure.UnitOfWorkProvider import UnitOfWorkProvider
from shared.exceptions.InfrastructureExceptions import ConfigurationException

try:
    config = Config.from_yaml("config.yaml")
    uow_provider = UnitOfWorkProvider(config)
except:
    raise ConfigurationException()


def get_uow() -> BaseUnitOfWork:
    return uow_provider.get_uow()


def get_user_service() -> UserService:
    return UserService()
