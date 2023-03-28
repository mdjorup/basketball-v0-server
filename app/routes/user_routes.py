from dataclasses import asdict

from firebase_admin.exceptions import PermissionDeniedError
from flask import Blueprint, g, request

from app.exceptions import BadRequestError
from app.middlewares import require_login
from app.models.user_model import User, UserRole
from app.routes.responses import build_response
from app.services.user_service import UserService

user_blueprint = Blueprint("users", __name__)


@user_blueprint.route("/", methods=["POST"])
def create_new_user():
    if not request.is_json:
        raise BadRequestError("Request body must be JSON")

    request_json: dict = request.get_json()
    name: str = request_json["name"]
    email: str = request_json["email"]
    password: str = request_json["password"]
    role: UserRole = request_json["role"]

    if role == "admin":  # can't create admin users
        raise PermissionDeniedError("Can't create admin users")

    user_service = UserService()


    new_user: User = user_service.create_user(
        name=name, email=email, password=password, role=role
    )

    return build_response(
        {"user": new_user.__dict__}, 201, f"User {new_user.uid} created successfully"
    )


@user_blueprint.route("/<uid>", methods=["GET"])
def get_user_by_id(uid: str):
    user_service = UserService()

    user: User = user_service.get_user(uid)

    return build_response(
        {"user": user.__dict__}, 200, f"User {user.uid} retrieved successfully"
    )


@user_blueprint.route("/<uid>", methods=["PUT"])
@require_login
def update_user_by_id(uid: str):
    # Vadidate that the user being updated is the same as the one in the token
    user_token_uid: str = g.decoded_token.get("uid")
    user_role : UserRole = g.decoded_token.get("role")
    admin = user_role == "admin"
    
    user_service = UserService(operating_uid=user_token_uid, admin=admin)

    if not request.is_json:
        raise BadRequestError("Request body must be JSON")

    request_json: dict = request.get_json()

    user: User = user_service.update_user(uid, request_json)
    
    return build_response(
        {"user": user.__dict__}, 200, f"User {user.uid} updated successfully"
    )


@user_blueprint.route("/<uid>", methods=["DELETE"])
@require_login
def delete_user_by_id(uid: str):
    # Validate access
    user_token_uid: str = g.decoded_token.get("uid")
    user_role : UserRole = g.decoded_token.get("role")
    admin = user_role == "admin"
    
    user_service = UserService(operating_uid=user_token_uid, admin=admin)

    user_service.delete_user(uid)
    return build_response({}, 204, f"User {uid} successfully deleted")


@user_blueprint.route("/me", methods=["GET"])
@require_login
def get_user_me():
    uid: str = g.decoded_token.get("uid")

    if not uid:
        raise PermissionDeniedError("Error getting user id from token")
    
    user_service = UserService(operating_uid=uid)
    
    user: User = user_service.get_user(uid)

    return build_response(
        {"user": user.__dict__}, 200, f"User {user.uid} retrieved successfully"
    )
