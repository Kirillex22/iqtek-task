from typing import Dict, List, Callable, Type, Union

from src.common.base.BaseUnitOfWork import BaseUnitOfWork
from src.plugins.user.entities.Commands import BaseUserCommand, CreateUserCommand
from src.plugins.user.entities.Events import BaseUserEvent, UserCreatedEvent
from src.plugins.user.services.UserService import UserService

COMMAND_HANDLERS: Dict[Type[BaseUserCommand], List[Callable]] = {
    CreateUserCommand: [lambda event, uow: UserService().create_user(event, uow)]
}

EVENT_HANDLERS: Dict[Type[BaseUserEvent], List[Callable]] = {
    UserCreatedEvent: [lambda event, uow: print(f'ПОЛЬЗОВАТЕЛЬ {event.id} СОЗДАН АХАХАХАХАХАХАХХА')]
}

Message = Union[BaseUserEvent, BaseUserCommand]

def handle(message: Message, uow: BaseUnitOfWork) -> List | None:
    queue = [message]
    results = []
    while queue:
        message = queue.pop(0)

        if isinstance(message, BaseUserEvent):
            handle_event(message, queue, uow)

        elif isinstance(message, BaseUserCommand):
            results.append(
                handle_command(message, queue, uow)
            )

        else:
            raise Exception(f"Unknown event type: {type(message)}")

    return results

def handle_event(
    event: BaseUserEvent,
    queue: List[Message],
    uow: BaseUnitOfWork,
):
    for handler in EVENT_HANDLERS[type(event)]:
        try:
            handler(event, uow=uow)
            queue.extend(uow.collect_new_events())
        except Exception:
            print(f"Exception while handling event: {event}")
            continue


def handle_command(
    command: BaseUserCommand,
    queue: List[Message],
    uow: BaseUnitOfWork,
):
    try:
        handler = COMMAND_HANDLERS[type(command)][0]
        result = handler(command, uow=uow)
        queue.extend(uow.collect_new_events())
        return result
    except Exception:
        print(f"Exception while handling command: {command}")
        raise