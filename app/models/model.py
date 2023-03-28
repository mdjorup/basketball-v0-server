from abc import ABC
from dataclasses import MISSING, asdict, dataclass, fields
from typing import Any


@dataclass
class Model:
    
    changes: dict[str, Any]

    def __init__(self, **kwargs) -> None:
        defaults = {
            f.name: f.default_factory()
            for f in fields(self)
            if f.default_factory is not MISSING
        }

        filtered_kwargs = {
            k: v for k, v in kwargs.items() if k in self.__annotations__.keys()
        }

        merged_kwargs = {**defaults, **filtered_kwargs}

        for k, v in merged_kwargs.items():
            object.__setattr__(self, k, v)
        self.changes = {}

    def __dict__(self) -> dict[str, Any]:
        dict_self = asdict(self)
        dict_self.pop("changes")
        return dict_self


    def update_field(self, key: str, value: Any) -> None:
        if key not in self.__annotations__.keys():
            raise AttributeError("Attribute doesn't exist")
        self.changes[key] = value
        object.__setattr__(self, key, value)
