from typing import Dict, List, Callable, Type

from src.plugins.user.entities.Events import BaseUserEvent, SettingInvalidNameEvent

HANDLERS: Dict[Type[BaseUserEvent], List[Callable]] = {
    SettingInvalidNameEvent: [lambda x: print('--------------------- monkey moment ------------------------------')]
}

def handle(event: BaseUserEvent) -> None:
    handlers: List[Callable] | None = HANDLERS.get(type(event), None)
    if not handlers:
        raise Exception(f'Unknown event: {event}')

    for handler in handlers:
        handler(event)


