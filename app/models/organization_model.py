from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, List

from app.models.model import Model
from app.models.player_model import Player
from app.models.team_model import Team
from app.models.user_model import User


@dataclass
class Organization(Model):
    """
    Dataclass representing an organization.

    Attributes:
        organization_id (str): The unique identifier of the organization.
        name (str): The name of the organization.
        created_at (datetime): The date and time the organization was created.
        updated_at (datetime): The date and time the organization was last updated.
        players (list[Player], optional): A list of players in the organization. Defaults to an empty list.
        teams (list[Team], optional): A list of teams in the organization. Defaults to an empty list.
        coaches (list[User], optional): A list of coaches in the organization. Defaults to an empty list.
    
    Methods:
        update_field(key: str, value: Any) -> None:
            Updates the value of an attribute in the class with the specified key.
            If the key is not found in the class' annotations, an AttributeError is raised.

    """
    organization_id: str
    name: str
    created_at: datetime
    updated_at: datetime
    players : List[Player] = field(default_factory = list)
    teams : List[Team] = field(default_factory = list)
    coaches : List[User] = field(default_factory = list)
    
    

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

        
