from dataclasses import dataclass
from typing import Literal

from user.constants import UserRole


@dataclass
class User:
    token: dict
    email: str
    uid: str
    data: dict
    role: UserRole = "standard"

    def __init__(self, token: dict):
        self.token = token
        self.email = token.get("email", "")
        self.uid = token.get("uid", "")
        self.data = {}


    def __eq__(self, __o: object) -> bool:
        if isinstance(__o, User):
            return self.uid == __o.uid
        return False

    def load(self) -> None:
        # loads the user data from the database
        pass 

    def save(self) -> None:
        # saves the user data to the database
        pass

    
    

        
        