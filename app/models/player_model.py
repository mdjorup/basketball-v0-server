

from dataclasses import dataclass, field
from enum import Enum
from typing import Any

from app.models.model import Model


class Position(Enum):
    POINT_GUARD = "PG"
    SHOOTING_GUARD = "SG"
    SMALL_FORWARD = "SF"
    POWER_FORWARD = "PF"
    CENTER = "C"
    NA = "N/A"


@dataclass
class Player(Model):
    player_id: str
    organization_id: str
    first_name: str
    last_name: str
    team_ids: list[str] = field(default_factory=list)
    height: int | None = None
    weight: int | None = None
    position: Position = Position.NA

    def update_field(self, key: str, value: Any) -> None:
        if key not in self.__annotations__.keys():
            raise AttributeError(f"Attribute {key} doesn't exist on {self.__class__.__name__}")
        
        object.__setattr__(self, key, value)
        