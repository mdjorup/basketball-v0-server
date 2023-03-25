from dataclasses import dataclass
from datetime import datetime
from typing import Any

from app.models.model import Model


@dataclass
class Player(Model):
    game_id: str
    home_team_id: str
    away_team_id: str
    home_team_score: int
    away_team_score: int
    game_time: datetime
    league_id: str = "" # this is if this is a league game



    def update_field(self, key: str, value: Any) -> None:
        if key not in self.__annotations__.keys():
            raise AttributeError(f"Attribute {key} doesn't exist on {self.__class__.__name__}")
        
        object.__setattr__(self, key, value)