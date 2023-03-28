from dataclasses import asdict
from datetime import datetime, timezone
from typing import Any

from firebase_admin import auth
from firebase_admin.exceptions import NotFoundError

from app.exceptions import UserCreationFailedError
from app.models.user_model import User, UserRole
from app.services.service import Service


class UserService(Service):

    def __init__(self, operating_uid="", admin=False) -> None:
        super().__init__()

        self.operating_uid : str = operating_uid
        self.admin : bool = admin


    def _create(self, model: User) -> None:
        self.db.collection("users").document(model.uid).set(model.__dict__())


    def _read(self, id: str) -> User:
        doc_ref = self.db.collection("users").document(id)
        doc = doc_ref.get()
        if not doc.exists:
            raise NotFoundError("User not found")
        data = doc.to_dict()
        user = User(**data)
        if not user.active:
            raise NotFoundError("User not found")
        return user
    

    def _update(self, model: User) -> None:
        self.db.collection("users").document(model.uid).update(model.changes)
    

    def _delete(self, model: User) -> None:
        self.db.collection("users").document(model.uid).delete()

    

    def create_user(self, name: str, email: str, password: str, role: UserRole) -> User:
        
        firebase_user = auth.create_user(email=email, password=password)

        if not firebase_user:
            raise UserCreationFailedError()

        uid: str = firebase_user.uid

        auth.set_custom_user_claims(uid, {"role": role})
        user: User = User(
            uid=uid,
            name=name,
            email=email,
            role=role,
        )

        self._create(user)

        return user


    def get_user(self, uid: str) -> User:
        return self._read(uid)


    def update_user(self, uid: str, updates : dict[str, Any]) -> User:
        

        if uid != self.operating_uid and not self.admin:
            raise PermissionError("You do not have permission to perform this action.")
        
        user: User = self._read(uid)
        
        for key, value in updates:
            user.update_field(key, value)
        
        self._update(user)
        
        return user


    def delete_user(self, uid: str) -> None:
        
        if uid != self.operating_uid and not self.admin:
            raise PermissionError("You do not have permission to perform this action.")

        user: User = self._read(uid)
        
        user.delete(caller_uid=self.operating_uid, admin=self.admin)
        
        self._update(user)
        
        
        
        
