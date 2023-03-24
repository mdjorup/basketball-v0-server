from dataclasses import MISSING, dataclass, field, fields
from datetime import datetime, timezone
from typing import Any, List, Literal

from app.models.model import Model

UserRole = Literal["admin", "standard", "coach"]


# The user model is just there to define how the data is structured
# You can use this to validate the data, and also to serialize it
# Perhaps, you want to update the user, well you can just check that the field you're updating is in the dataclass
# Perhaps you want all data on the user, well you can get a User object and then serialize it to a dict


@dataclass
class User(Model):
    uid: str
    name: str
    email: str
    role: UserRole
    active: bool
    created_at: datetime  # unix timestamp
    updated_at: datetime  # unix timestamp
    organization_ids: List[str] = field(default_factory = list)

    def update_field(self, key: str, value: Any) -> None:
        if key not in self.__annotations__.keys():
            raise AttributeError("Attribute doesn't exist")
        elif (
            key == "uid" or key == "email" or key == "created_at" or key == "updated_at"
        ):
            raise AttributeError(f"Unable to edit attribute {key}")
        object.__setattr__(self, key, value)
        self.updated_at = datetime.now(timezone.utc)
