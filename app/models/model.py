from abc import ABC, abstractmethod
from dataclasses import MISSING, dataclass, fields
from typing import Any


@dataclass
class Model(ABC):
    def __init__(self, **kwargs):
        defaults = {
            f.name: f.default_factory() for f in fields(self) if f.default_factory is not MISSING
        }

        filtered_kwargs = {
            k: v for k, v in kwargs.items() if k in self.__annotations__.keys()
        }

        merged_kwargs = {**defaults, **filtered_kwargs}

        for k, v in merged_kwargs.items():
            object.__setattr__(self, k, v)
    
    @abstractmethod
    def update_field(self, key: str, value: Any) -> None:
        pass
        

        

