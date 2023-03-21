from app.database import get_db
from app.models.user_model import User, UserRole


class UserService:

    def __init__(self):
        self.db = get_db()

    
    def create_user(self, uid : str, name : str, email : str, password : str, role : UserRole) -> User | None:
        pass

    def get_user(self, uid : str) -> User | None:

        pass

    def update_user(self, user : User) -> bool:
        # updating a user should involve first loading the user using the get_user method in order to pass a User object

        pass

    def delete_user(self, uid : str) -> None:
        pass


        
        

    # So we should be able to construct a user object from the data, but then also 
    