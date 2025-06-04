from uuid import UUID

from src.common.exceptions.UserServiceExceptions import InvalidUserFullNameException
from src.plugins.user.entities.Events import UserCreatedEvent


class User:
    def __init__(self, id: UUID, full_name: str, already_registered: bool = True):
        self.events = []
        self.already_registered = already_registered
        self.id: UUID = id
        self.full_name = full_name

    @property
    def id(self) -> UUID:
        return self._id

    @id.setter
    def id(self, id: UUID):
        if not self.already_registered:
            self.events.append(UserCreatedEvent(id=id))
        self._id = id

    @property
    def full_name(self) -> str:
        return self._full_name

    @full_name.setter
    def full_name(self, value):
        words_count = len(value.split())
        if words_count != 3:
           raise InvalidUserFullNameException(f'Слов в полном имении должно быть 3.')
        else:
            self._full_name = value

