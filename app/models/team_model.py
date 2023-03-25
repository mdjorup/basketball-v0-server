
from dataclasses import dataclass, field
from typing import Any

from app.models.model import Model


@dataclass
class Team(Model):
    team_id: str
    organization_id: str
    name: str
    wins: int = 0
    losses: int = 0
    ties: int = 0
    league_id: str = ""
    player_ids: list[str] = field(default_factory=list)
    game_ids: list[str] = field(default_factory=list)

    def update_field(self, key: str, value: Any) -> None:
        if key not in self.__annotations__.keys():
            raise AttributeError(f"Attribute {key} doesn't exist on {self.__class__.__name__}")
        
        object.__setattr__(self, key, value)