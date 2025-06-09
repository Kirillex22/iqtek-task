from uuid import UUID

from sqlalchemy.testing.pickleable import User

from src.common.exceptions.UserServiceExceptions import InvalidUserFullNameException, InvalidUserIdException
from src.plugins.user.entities.Events import UserCreatedEvent, UserUpdatedEvent, UserDeletedEvent


class User:
    def __init__(self, id: UUID, full_name: str):
        self.events = []
        self.id: UUID = id
        self.full_name = full_name

    @property
    def id(self) -> UUID:
        return self._id

    @id.setter
    def id(self, id: UUID):
        if type(id) is not UUID:
            raise InvalidUserIdException
        self._id = id

    @property
    def full_name(self) -> str:
        return self._full_name


    @full_name.setter
    def full_name(self, value):
        words_count = len(value.split())
        if words_count != 3:
           raise InvalidUserFullNameException(f'Слов в полном имени должно быть 3.')
        else:
            self._full_name = value

    def commit_register(self):
        self.events.append(UserCreatedEvent(id=self.id))

    def commit_delete(self):
        self.events.append(UserDeletedEvent(id=self.id, full_name=self.full_name))

    def commit_full_name_change(self, old_full_name: str):
        self.events.append(UserUpdatedEvent(id=self._id, full_name=self._full_name, old_full_name=old_full_name))

    def json(self):
        return {
            'id': str(self.id),
            'full_name': self.full_name
        }

    @staticmethod
    def from_json(json: dict) -> User:
        id = UUID(json['id'])
        full_name = json['full_name']
        return User(id, full_name)