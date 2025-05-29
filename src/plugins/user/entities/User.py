from uuid import UUID

class User:
    def __init__(self, id: UUID, full_name: str):
        self.id: UUID = id
        words_count = len(full_name.split())
        if words_count != 3:
            raise AttributeError(f'Words count in {full_name} should be 3')
        self.full_name = full_name

    # @property
    # def full_name(self):
    #     return self._full_name
    #
    # @full_name.setter
    # def full_name(self, value):
    #     words_count = len(value.split())
    #     if words_count != 3:
    #         raise AttributeError(f'Words count in {value} should be 3')
    #     self._full_name = value