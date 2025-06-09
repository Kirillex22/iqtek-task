import logging
from typing import List, Union
from tenacity import Retrying, RetryError, stop_after_attempt, wait_exponential

from src.common.base.BaseUnitOfWork import BaseUnitOfWork
from src.plugins.user.entities.Commands import BaseUserCommand
from src.plugins.user.entities.Events import BaseUserEvent
from src.plugins.user.services.Handlers import EVENT_HANDLERS, COMMAND_HANDLERS


Message = Union[BaseUserEvent, BaseUserCommand]

class MessageBus:
    def __init__(self, uow: BaseUnitOfWork, event_handlers, command_handlers):
        self._uow = uow
        self._event_handlers = event_handlers
        self._command_handlers = command_handlers

    def handle(self, message: Message) -> List | None:
        queue = [message]
        results = []
        while queue:
            message = queue.pop(0)

            if isinstance(message, BaseUserEvent):
                self.handle_event(message, queue)

            elif isinstance(message, BaseUserCommand):
                results.append(
                    self.handle_command(message, queue)
                )

            else:
                raise Exception(f"Unknown event type: {type(message)}")

        return results

    def handle_event(
            self,
            event: BaseUserEvent,
            queue: List[Message]
    ):
        for handler in self._event_handlers[type(event)]:
            try:
                for attempt in Retrying(
                    stop=stop_after_attempt(3),
                    wait=wait_exponential(),
                    after=lambda retry_state: logging.warning(retry_state.outcome.exception())
                ):
                    with attempt:
                        logging.debug('Обработка события %s обработчиком %s', event, handler)
                        handler(event, uow=self._uow)
                        queue.extend(self._uow.collect_new_events())
            except RetryError as retry_failure:
                logging.error(
                    f'Не удалось обработать событие после {retry_failure.last_attempt.attempt_number} попыток: {event}'
                )
                continue


    def handle_command(
        self,
        command: BaseUserCommand,
        queue: List[Message],
    ):
        try:
            handler = self._command_handlers[type(command)][0]
            result = handler(command, uow=self._uow)
            queue.extend(self._uow.collect_new_events())
            return result
        except Exception:
            print(f"Exception while handling command: {command}")
            raise