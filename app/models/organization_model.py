from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, List

from app.models.model import Model
from app.models.user_model import User


@dataclass
class Organization(Model):
    id: str
    name: str

    created_at: datetime
    updated_at: datetime
    # players : List[Player] = field(default_factory = list)
    # teams : List[Team] = field(default_factory = list)
    coaches : List[User] = field(default_factory = list)
    
    

    def update_field(self, key: str, value: Any) -> None:
        if key not in self.__annotations__.keys():
            raise AttributeError(f"Attribute {key} doesn't exist on {self.__class__.__name__}")
        
        object.__setattr__(self, key, value)

        
