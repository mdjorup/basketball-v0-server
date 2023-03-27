from dataclasses import dataclass, field
from typing import Any, List

from app.models.model import Model


@dataclass
class League(Model):
    """
    Dataclass representing a basketball league.

    Attributes:
        league_id (str): The unique identifier of the league.
        name (str): The name of the league.
        description (str, optional): The description of the league. Defaults to "".
        teams (List[str], optional): The unique identifiers of the teams in the league. Defaults to an empty list.

    Methods:
        update_field(key: str, value: Any) -> None:
            Updates the value of an attribute in the class with the specified key.
            If the key is not found in the class' annotations, an AttributeError is raised.
    """
    league_id: str
    name: str
    description: str = ""
    teams: list[str] = field(default_factory=list)

    

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