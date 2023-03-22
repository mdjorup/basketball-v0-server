from dataclasses import asdict
from datetime import datetime, timezone

from firebase_admin import auth
from firebase_admin.exceptions import NotFoundError

from app.database import get_db
from app.exceptions import UserCreationFailedError
from app.models.user_model import User, UserRole


class UserService:

    def __init__(self):
        self.db = get_db()

    
    def create_user(self, name : str, email : str, password : str, role : UserRole) -> User:
        firebase_user = auth.create_user(email=email, password=password)
        
        if not firebase_user:
            raise UserCreationFailedError()
        
        uid : str = firebase_user.uid
        
        auth.set_custom_user_claims(uid, {"role": role})
        current_time: datetime = datetime.now(timezone.utc)
        user : User = User(uid=uid, name=name, email=email, role=role, active=True, created_at=current_time, updated_at=current_time)
    
        self.db.collection("users").document(uid).set(asdict(user))
        
        return user
        

    def get_user(self, uid : str) -> User:
        doc_ref = self.db.collection("users").document(uid)
        doc = doc_ref.get()
        if not doc.exists:
            raise NotFoundError(f"User {uid} not found")
        data = doc.to_dict()
        user : User = User(**data)
        return user
            

    def update_user(self, user : User) -> None:
        # updating a user should involve first loading the user using the get_user method in order to pass a User object
        uid = user.uid
        doc_ref = self.db.collection("users").document(uid)
        doc = doc_ref.get()
        if not doc.exists:
            raise NotFoundError(f"User {uid} not found")
        
        doc_ref.set(asdict(user))
    def delete_user(self, uid : str) -> None:
        
        doc_ref = self.db.collection("users").document(uid)
        doc = doc_ref.get()

        if not doc.exists:
            raise NotFoundError(f"User {uid} not found")
        
        data = doc.to_dict()
        user : User = User(**data)
        user.update_field("active", False)
        doc_ref.set(asdict(user))



        
        

    # So we should be able to construct a user object from the data, but then also 
    