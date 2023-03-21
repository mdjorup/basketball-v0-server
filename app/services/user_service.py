from dataclasses import asdict
from datetime import datetime, timezone

from firebase_admin import auth

from app.database import get_db
from app.models.user_model import User, UserRole


class UserService:

    def __init__(self):
        self.db = get_db()

    
    def create_user(self, name : str, email : str, password : str, role : UserRole) -> User | None:
        firebase_user = auth.create_user(email=email, password=password)
        if not firebase_user:
            # should be raising errors
            return None
        uid : str = firebase_user.uid
        
        auth.set_custom_user_claims(uid, {"role": role})
        current_time: datetime = datetime.now(timezone.utc)
        user : User = User(uid=uid, name=name, email=email, password=password, role=role, active=True, created_at=current_time, updated_at=current_time)
        
        self.db.collection("users").document(uid).set(asdict(user))
        
        return user
        

    def get_user(self, uid : str) -> User | None:
        doc_ref = self.db.collection("users").document(uid)
        doc = doc_ref.get()
        if doc.exists:
            data = doc.to_dict()
            user : User = User(**data)
            return user
        else:
            return None
            

        pass

    def update_user(self, user : User) -> bool:
        # updating a user should involve first loading the user using the get_user method in order to pass a User object

        return True

    def delete_user(self, uid : str) -> None:
        pass


        
        

    # So we should be able to construct a user object from the data, but then also 
    