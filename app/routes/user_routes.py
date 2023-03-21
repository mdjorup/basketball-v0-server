
from dataclasses import asdict

from firebase_admin.auth import EmailAlreadyExistsError
from firebase_admin.exceptions import NotFoundError
from flask import Blueprint, g, request

from app.middlewares import authorized_roles, require_login
from app.models.user_model import User, UserRole
from app.services.exceptions import UserCreationFailedError
from app.services.user_service import UserService

user_blueprint = Blueprint("user", __name__)

@user_blueprint.route("/", methods=["POST"])
def create_new_user():

    if not request.is_json:
        return "Error", 400
    
    request_json : dict = request.get_json()
    name : str = request_json["name"]
    email : str = request_json["email"]
    password : str = request_json["password"]
    role : UserRole = request_json["role"]

    if role == "admin": # can't create admin users
        return "Error", 400
    
    user_service = UserService()

    new_user : User | None = user_service.create_user(name=name, email=email, password=password, role=role)
    if new_user:   
        return asdict(new_user), 201
    else:
        return "Error", 500


@user_blueprint.route("/<uid>", methods=["GET"])
def get_user_by_id(uid : str):

    user_service = UserService()

    user : User | None = user_service.get_user(uid)
    if user:
        return asdict(user), 200
    else:
        return "Error", 500


@user_blueprint.route("/<uid>", methods=["PUT"])
@require_login
def update_user_by_id(uid : str):
    
    
    # Vadidate that the user being updated is the same as the one in the token
    user_token_uid : str = g.decoded_token.get("uid")
    if g.decoded_token.get("role") == "admin":
        pass
    elif not user_token_uid:
        return "Error", 500
    elif user_token_uid != uid: 
        return "Error", 400
    
    user_service = UserService()
    
    if request.is_json:
        request_json : dict = request.get_json()
    else : 
        return "Error", 500
    
    user : User = user_service.get_user(uid)
    if not user:
        return "Error", 500
    
    for key, value in request_json.items():
        user.update_field(key, value)

    success = user_service.update_user(user)
    if success:
        return asdict(user), 200
    else:
        return "Error", 500


@user_blueprint.route("/<uid>", methods=["DELETE"])
@require_login
def delete_user_by_id(uid : str):

    # Validate access
    user_token_uid : str = g.decoded_token.get("uid")
    if g.decoded_token.get("role") == "admin":
        pass
    elif not user_token_uid:
        return "Error", 500
    elif user_token_uid != uid: # can't delete other users
        return "Error", 400
    
    user_service = UserService()

    if user_service.delete_user(uid):
        return "Success", 200
    else:
        return "Error", 500



@user_blueprint.route("/me", methods=["GET"])
@require_login
def get_user_me():
    uid : str = g.decoded_token.get("uid")
    if not uid:
        return "Error", 500
    
    user_service = UserService()

    user : User = user_service.get_user(uid)
    if user:
        return asdict(user), 200
    else:
        return "Error", 500
    
    
@user_blueprint.errorhandler(EmailAlreadyExistsError)
def handle_email_already_exists(error):
    return error, 409

@user_blueprint.errorhandler(UserCreationFailedError)
def handle_user_creation_failed(error):
    return error, 500

@user_blueprint.errorhandler(NotFoundError)
def handle_not_found(error):
    return error, 404

@user_blueprint.errorhandler(Exception)
def handle_exception(error):
    return error, 500
