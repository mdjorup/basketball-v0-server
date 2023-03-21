from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Literal

UserRole = Literal['admin', 'standard', 'coach']


# The user model is just there to define how the data is structured
# You can use this to validate the data, and also to serialize it
# Perhaps, you want to update the user, well you can just check that the field you're updating is in the dataclass
# Perhaps you want all data on the user, well you can get a User object and then serialize it to a dict

@dataclass
class User:
    uid : str
    name: str
    email: str
    password: str 
    role: UserRole
    active : bool
    created_at : datetime
    updated_at : datetime
    __updates : dict = field(default_factory=dict, init=False, repr=False, compare=False)

    def set_field(self, field : str, value : Any) -> None:
        if not hasattr(self, field):
            raise AttributeError(f"User object has no attribute {field}")
        
        setattr(self, field, value)
        self.__updates[field] = value
    
    def get_updates(self) -> dict:
        return self.__updates
    
    
    
    
        


    