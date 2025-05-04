from config.Config import Config
from domain.base.BaseUnitOfWork import BaseUnitOfWork
from infrastructure.UnitOfWorkProvider import UnitOfWorkProvider

config = Config.from_yaml("config.yaml")
uow_provider = UnitOfWorkProvider(config)


def get_uow() -> BaseUnitOfWork:
    return uow_provider.get_uow()
