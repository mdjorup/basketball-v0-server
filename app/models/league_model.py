from dataclasses import dataclass, field
from typing import Any, List

from app.models.model import Model


@dataclass
class Player(Model):
    league_id: str
    name: str
    description: str = ""
    teams: list[str] = field(default_factory=list)

    

    def update_field(self, key: str, value: Any) -> None:
        if key not in self.__annotations__.keys():
            raise AttributeError(f"Attribute {key} doesn't exist on {self.__class__.__name__}")
        
        object.__setattr__(self, key, value)