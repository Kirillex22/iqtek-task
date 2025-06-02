from abc import abstractmethod, ABC


class BaseSessionFactory(ABC):
    @abstractmethod
    def get_session(self):
        pass