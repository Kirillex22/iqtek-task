from domain.entities.User import User


class UserAlreadyExistsException(Exception):
    code = "ALREADY_EXISTS"

    def __init__(self, user: User):
        super().__init__(f"Пользователь {user} уже существует в БД.")


class UserNotExistsException(Exception):
    code = "NOT_EXISTS"

    def __init__(self, user_id: str):
        super().__init__(f"Пользователь {user_id} не найден в БД.")


class UnknownUserException(Exception):
    code = "UNKNOWN"

    def __init__(self):
        super().__init__(f"Неизвестная ошибка при операции с пользователем.")
