from uuid import UUID

from src.common.exceptions.UserServiceExceptions import EntityValidationException


class User:
    def __init__(self, id: UUID, full_name: str):
        self.id: UUID = id
        self.full_name = full_name

    @property
    def id(self) -> UUID:
        return self._id

    @id.setter
    def id(self, id: UUID):
        self._id = id

    @property
    def full_name(self) -> str:
        return self._full_name

    @full_name.setter
    def full_name(self, value):
        words_count = len(value.split())
        if words_count != 3:
            raise EntityValidationException(f'Words count in /{value}/ should be 3')
        self._full_name = value

