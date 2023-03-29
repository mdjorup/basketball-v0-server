from dataclasses import dataclass, field
from enum import Enum
from typing import Any

from app.models.model import Model


class Position(Enum):
    """
    Enum representing the possible positions a basketball player can play.
    """

    POINT_GUARD = "PG"
    SHOOTING_GUARD = "SG"
    SMALL_FORWARD = "SF"
    POWER_FORWARD = "PF"
    CENTER = "C"
    NA = "N/A"


@dataclass
class Player(Model):
    """
    Dataclass representing a basketball player.

    Attributes:
        player_id (str): The unique identifier of the player.
        first_name (str): The first name of the player.
        last_name (str): The last name of the player.
        team_ids (list[str], optional): A list of team IDs the player is associated with. Defaults to an empty list.
        height (float, optional): The height of the player in inches. Defaults to None.
        weight (float, optional): The weight of the player in pounds. Defaults to None.
        position (Position): The position of the player. Defaults to Position.NA.

    Methods:
        update_field(key: str, value: Any) -> None:
            Updates the value of an attribute in the class with the specified key.
            If the key is not found in the class' annotations, an AttributeError is raised.
    """

    player_id: str
    first_name: str
    last_name: str
    active: bool = True
    team_ids: list[str] = field(default_factory=list)
    height: float | None = None
    weight: float | None = None
    position: Position = Position.NA

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        

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
            raise AttributeError(
                f"Attribute {key} doesn't exist on {self.__class__.__name__}"
            )

        object.__setattr__(self, key, value)
