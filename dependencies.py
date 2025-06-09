from src.common.base.BaseUnitOfWork import BaseUnitOfWork
from src.config.Config import Config
from src.plugins.user.services.Handlers import EVENT_HANDLERS, COMMAND_HANDLERS
from src.plugins.user.services.MessageBus import MessageBus
from src.plugins.user.services.UserService import UserService
from src.infrastructure.UnitOfWorkProvider import UnitOfWorkProvider
from src.common.exceptions.InfrastructureExceptions import ConfigurationException

try:
    config = Config.from_yaml("config.yaml")
    uow_provider = UnitOfWorkProvider(config)
    uow = uow_provider.get_uow()
    message_bus = MessageBus(uow, EVENT_HANDLERS, COMMAND_HANDLERS)
except:
    raise ConfigurationException()

def get_uow() -> BaseUnitOfWork:
    return uow

def get_user_service() -> UserService:
    return UserService()

def get_message_bus() -> MessageBus:
    return message_bus