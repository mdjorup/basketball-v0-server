from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Literal

from app.models.model import Model

# TODO: Turn this into an ENUM Class
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
    created_at: datetime = datetime.now(tz=timezone.utc)
    updated_at: datetime = datetime.now(tz=timezone.utc)
    active: bool = True

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def update_field(self, key: str, value: Any) -> None:
        if key == "uid" or key == "email" or key == "created_at" or key == "updated_at":
            raise AttributeError(f"Unable to edit attribute {key}")
        super().update_field(key, value)
        self.updated_at = datetime.now(timezone.utc)

    def delete(self):
        self.update_field("active", False)
