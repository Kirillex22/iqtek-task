from shared.exceptions.UserServiceExceptions import UserAlreadyExistsException, UserNotExistsException


class UserServiceExceptionHandler:
    @staticmethod
    def handle(exc: Exception):
        if isinstance(exc, UserAlreadyExistsException):
            raise exc

        elif isinstance(exc, UserNotExistsException):
            raise exc
