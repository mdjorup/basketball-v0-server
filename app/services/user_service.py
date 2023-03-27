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

    def create_user(self, name: str, email: str, password: str, role: UserRole) -> User:
        """
        Creates a new user in Firebase Authentication and saves their details to the database.

        Args:
            name (str): The name of the user.
            email (str): The email address of the user.
            password (str): The password for the user's account.
            role (UserRole): The role of the user.

        Raises:
            UserCreationFailedError: If the user creation process fails.

        Returns:
            User: The user object representing the created user.
        """
        firebase_user = auth.create_user(email=email, password=password)

        if not firebase_user:
            raise UserCreationFailedError()

        uid: str = firebase_user.uid

        auth.set_custom_user_claims(uid, {"role": role})
        current_time: datetime = datetime.now(timezone.utc)
        user: User = User(
            uid=uid,
            name=name,
            email=email,
            role=role,
            active=True,
            created_at=current_time,
            updated_at=current_time,
        )

        self.db.collection("users").document(uid).set(asdict(user))

        return user

    def get_user(self, uid: str) -> User:
        """
        Retrieves a user from the database using their unique identifier.

        Args:
            uid (str): The unique identifier of the user.

        Raises:
            NotFoundError: If a user with the specified identifier cannot be found in the database.

        Returns:
            User: The user object representing the retrieved user.
        """
        doc_ref = self.db.collection("users").document(uid)
        doc = doc_ref.get()
        if not doc.exists:
            raise NotFoundError(f"User {uid} not found")
        data = doc.to_dict()
        user: User = User(**data)
        return user

    def update_user(self, user: User) -> None:
        """
        Updates the details of an existing user in the database.

        Args:
            user (User): The user object representing the updated user.

        Raises:
            NotFoundError: If the user with the specified identifier cannot be found in the database.

        Returns:
            None.
        """
        uid = user.uid
        doc_ref = self.db.collection("users").document(uid)
        doc = doc_ref.get()
        if not doc.exists:
            raise NotFoundError(f"User {uid} not found")

        doc_ref.set(asdict(user))

    def delete_user(self, uid: str) -> None:
        """
        Soft-deletes an existing user in the database by setting their 'active' field to False.

        Args:
            uid (str): The unique identifier of the user to be deleted.

        Raises:
            NotFoundError: If the user with the specified identifier cannot be found in the database.

        Returns:
            None.
        """
        doc_ref = self.db.collection("users").document(uid)
        doc = doc_ref.get()

        if not doc.exists:
            raise NotFoundError(f"User {uid} not found")

        data = doc.to_dict()
        user: User = User(**data)
        user.update_field("active", False)
        doc_ref.set(asdict(user))

