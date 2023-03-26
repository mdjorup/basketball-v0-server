
from dataclasses import dataclass, field
from typing import Any

from app.models.model import Model


@dataclass
class Team(Model):
    """
    Dataclass representing a basketball team.

    Attributes:
        team_id (str): The unique identifier of the team.
        name (str): The name of the team.
        wins (int, optional): The number of wins the team has. Defaults to 0.
        losses (int, optional): The number of losses the team has. Defaults to 0.
        ties (int, optional): The number of ties the team has. Defaults to 0.
        league_id (str, optional): The identifier of the league the team belongs to. Defaults to "".
        player_ids (list[str], optional): A list of player IDs the team has. Defaults to an empty list.
        game_ids (list[str], optional): A list of game IDs the team has played. Defaults to an empty list.

    Methods:
        update_field(key: str, value: Any) -> None:
            Updates the value of an attribute in the class with the specified key.
            If the key is not found in the class' annotations, an AttributeError is raised.
    """
    team_id: str
    name: str
    wins: int = 0
    losses: int = 0
    ties: int = 0
    league_id: str = ""
    player_ids: list[str] = field(default_factory=list)
    game_ids: list[str] = field(default_factory=list)

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