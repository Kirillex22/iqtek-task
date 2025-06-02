from functools import wraps
from typing import Callable, Optional

from src.common.exceptions.UserServiceExceptions import UserAlreadyExistsException, UserNotExistsException

def uow_wrapper(func) -> Callable:
    @wraps(func)
    def wrapper(self, *args, **kwargs) -> Optional:
        try:
            result = func(self, *args, **kwargs)
            return result
        except Exception as e:
            self.exception_handler.handle(e)
            return None

    return wrapper

class UserServiceExceptionHandler:
    @staticmethod
    def handle(exc: Exception):
        if isinstance(exc, UserAlreadyExistsException):
            raise exc

        elif isinstance(exc, UserNotExistsException):
            raise exc

        else:
            raise exc
