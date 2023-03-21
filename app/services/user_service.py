from app.database import get_db
from app.models.user_model import User, UserRole


class UserService:

    def __init__(self):
        self.db = get_db()

    
    def create_user(self, uid : str, name : str, email : str, password : str, role : UserRole) -> User:
        pass

    def get_user(self, uid : str) -> User:
        pass

    def update_user(self, uid : str, data : dict) -> None:
        pass

    def delete_user(self, uid : str) -> None:
        pass


        
        

    # So we should be able to construct a user object from the data, but then also 
    