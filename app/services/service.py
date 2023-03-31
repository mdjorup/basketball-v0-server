from abc import ABC, abstractmethod

from app.database import get_db
from app.models.model import Model


class Service(ABC):
    def __init__(self):
        self.db = get_db()

    # abstract methods don't do any validation. They just do what they are told
    #
    @abstractmethod
    def _create(self, model: Model, *args, **kwargs) -> None:
        pass

    @abstractmethod
    def _read(self, id: str, *args, **kwargs) -> Model:
        pass

    @abstractmethod
    def _update(self, model: Model, *args, **kwargs) -> None:
        pass

    @abstractmethod
    def _delete(self, model: Model, *args, **kwargs) -> None:
        pass
