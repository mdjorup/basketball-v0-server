from dataclasses import dataclass
from datetime import datetime
from enum import Enum, auto
from typing import Any

from app.models.model import Model


class GameStatus(Enum):
    """
    Enum representing the status of a game.
    """
    UPCOMING = 0
    IN_PROGRESS = 1
    FINAL = 2


@dataclass
class Game(Model):
    """
    Dataclass representing a basketball game.

    Attributes:
        game_id (str): The unique identifier of the game.
        home_team_id (str): The unique identifier of the home team.
        away_team_id (str): The unique identifier of the away team.
        home_team_score (int): The score of the home team.
        away_team_score (int): The score of the away team.
        game_time (datetime): The time of the game.
        status (GameStatus, optional): The status of the game. Defaults to GameStatus.UPCOMING.
        league_id (str, optional): The identifier of the league the game belongs to. Defaults to "".

    Methods:
        update_field(key: str, value: Any) -> None:
            Updates the value of an attribute in the class with the specified key.
            If the key is not found in the class' annotations, an AttributeError is raised.
    """
    game_id: str
    home_team_id: str
    away_team_id: str
    home_team_score: int
    away_team_score: int
    game_time: datetime
    status: GameStatus = GameStatus.UPCOMING
    league_id: str = "" # this is if this is a league game



    def update_field(self, key: str, value: Any) -> None:
        """
        Updates the value of an attribute in the class with the specified key.

        Args:
            key (str): The name of the attribute to be updated.
            value (Any): The new value for the attribute.

        Raises:
            AttributeError: If the key is not found in the class' annotations.
        """
        if key not in self.__annotations__.keys():
            raise AttributeError(f"Attribute {key} doesn't exist on {self.__class__.__name__}")
        
        object.__setattr__(self, key, value)