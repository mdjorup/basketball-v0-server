from abc import ABC, abstractmethod

from app.database import get_db
from app.models.model import Model


class Service(ABC):
    def __init__(self):
        self.db = get_db()

    # abstract methods don't do any validation. They just do what they are told
    # 
    @abstractmethod
    def __create(self, model : Model) -> None:
        pass

    @abstractmethod
    def __read(self, id : str) -> Model:
        pass

    @abstractmethod
    def __update(self, model : Model) -> None:
        pass

    @abstractmethod
    def __delete(self, model : Model) -> None:
        pass
