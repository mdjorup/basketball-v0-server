from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any

from google.cloud import firestore

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
        owner (str): The uid of the user that owns the organization
        players (list[Player], optional): A list of players in the organization. Defaults to an empty list.
        active (bool, optional): Whether the organization is active. Defaults to True.
        teams (list[Team], optional): A list of teams in the organization. Defaults to an empty list.
        coaches (list[str]], optional): A list of coaches in the organization. Defaults to an empty list.

    Methods:
        update_field(key: str, value: Any) -> None:
            Updates the value of an attribute in the class with the specified key.
            If the key is not found in the class' annotations, an AttributeError is raised.

    """

    organization_id: str
    name: str
    owner: str  # uid of person who owns it
    created_at: datetime = datetime.now(tz=timezone.utc)
    updated_at: datetime = datetime.now(tz=timezone.utc)
    active: bool = True
    players: list[Player] = field(default_factory=list)  # subcollection
    teams: list[Team] = field(default_factory=list)  # subcollection
    coaches: list[str] = field(default_factory=list)  # list of uids

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def __dict__(self) -> dict[str, Any]:
        super_dict = super().__dict__()
        super_dict.pop("players")
        super_dict.pop("teams")
        return super_dict

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
        super().update_field(key, value)
        super().update_field("updated_at", datetime.now(timezone.utc))

    def delete(self):
        """
        Deletes the organization.
        """
        self.update_field("active", False)
    
    def add_coach(self, coach_uid: str) -> None:
        """
        Adds a coach to the organization.

        Args:
            coach_uid (str): The uid of the coach to be added.
        """
        if coach_uid in self.coaches:
            return
        
        self.coaches.append(coach_uid)
        self.changes["coaches"] = firestore.ArrayUnion([coach_uid])
        super().update_field("updated_at", datetime.now(timezone.utc))

    def remove_coach(self, coach_uid: str) -> None:
        
        if coach_uid not in self.coaches:
            return
        
        self.coaches.remove(coach_uid)
        self.changes["coaches"] = firestore.ArrayRemove([coach_uid])
        super().update_field("updated_at", datetime.now(timezone.utc))
        
        