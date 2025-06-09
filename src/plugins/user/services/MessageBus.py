import logging
from typing import List, Union
from tenacity import Retrying, RetryError, stop_after_attempt, wait_exponential

from src.common.base.BaseUnitOfWork import BaseUnitOfWork
from src.plugins.user.entities.Commands import BaseUserCommand
from src.plugins.user.entities.Events import BaseUserEvent
from src.plugins.user.services.Handlers import EVENT_HANDLERS, COMMAND_HANDLERS


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

def handle_event(event: BaseUserEvent, queue: List[Message], uow: BaseUnitOfWork):
    for handler in EVENT_HANDLERS[type(event)]:
        try:
            for attempt in Retrying(
                stop=stop_after_attempt(3),
                wait=wait_exponential(),
                after=lambda retry_state: logging.warning(retry_state.outcome.exception())
            ):
                with attempt:
                    logging.debug('Обработка события %s обработчиком %s', event, handler)
                    handler(event, uow=uow)
                    queue.extend(uow.collect_new_events())
        except RetryError as retry_failure:
            logging.error(
                f'Не удалось обработать событие после {retry_failure.last_attempt.attempt_number} попыток: {event}'
            )
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