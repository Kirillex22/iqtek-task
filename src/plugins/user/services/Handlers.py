import logging
import random
import time
from typing import Type, Dict, Callable, List
from src.plugins.user.entities.Commands import CreateUserCommand, BaseUserCommand, UpdateUserCommand, DeleteUserCommand
from src.plugins.user.entities.Events import UserCreatedEvent, BaseUserEvent, UserUpdatedEvent, UserDeletedEvent
from src.plugins.user.services.UserService import UserService

service = UserService()
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def create_user_command_handler(event, uow):
    return service.create_user(event, uow)

def update_user_command_handler(event, uow):
    return service.update_user(event.id, event, uow)

def delete_user_command_handler(event, uow):
    return service.delete_user(event.id, uow)

def user_created_event_handler(event, uow):
    logging.info(f'ПОЛЬЗОВАТЕЛЬ {event.id} СОЗДАН')

def user_updated_event_handler(event, uow):
    logging.info(f'ПОЛЬЗОВАТЕЛЬ {event.id} СМЕНИЛ ИМЯ С "{event.old_full_name}" НА "{event.full_name}"')

def user_deleted_event_handler(event, uow):
    logging.info(f'ПОЛЬЗОВАТЕЛЬ {event.id} УДАЛЕН')

def notify_email_handler(event, uow):
    print(f'// ОТПРАВКА EMAIL...')
    time.sleep(2)
    exception_proba = random.randint(0, 1)
    if exception_proba:
        raise Exception('// ОШИБКА ПРИ ОТПРАВКЕ EMAIL')
    print(f'// ОТПРАВЛЕНО УВЕДОМЛЕНИЕ НА EMAIL')


COMMAND_HANDLERS: Dict[Type[BaseUserCommand], List[Callable]] = {
    CreateUserCommand: [create_user_command_handler],
    UpdateUserCommand: [update_user_command_handler],
    DeleteUserCommand: [delete_user_command_handler],
}

EVENT_HANDLERS: Dict[Type[BaseUserEvent], List[Callable]] = {
    UserCreatedEvent: [user_created_event_handler, notify_email_handler],
    UserUpdatedEvent: [user_updated_event_handler],
    UserDeletedEvent: [user_deleted_event_handler, notify_email_handler]
}

