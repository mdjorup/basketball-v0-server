
from dataclasses import asdict
from datetime import datetime, timezone

from flask import Blueprint, Response, g, request

from app.middlewares import authorized_roles, require_login
from app.models.user_model import User
from app.services.user_service import UserService

user_blueprint = Blueprint("user", __name__)

@user_blueprint.route("/", methods=["POST"])
def create_new_user():

    user_service = UserService()

    new_user : User | None = user_service.create_user("Blank", "blank.djorup@gmail.com", "password", "standard")
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
    
    user_service = UserService()
    
    if request.is_json:
        request_json : dict = request.get_json()
    else : 
        return "Error", 500
    
    print(request_json)
    user : User | None = user_service.get_user(uid)
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
@authorized_roles(["admin"])
def delete_user_by_id(uid : str):

    user_service = UserService()
    if user_service.delete_user(uid):
        return "Success", 200
    else:
        return "Error", 500



@user_blueprint.route("/me", methods=["GET"])
@require_login
def get_user_me():
    uid : str = g.decoded_token["uid"]
    user_service = UserService()
    user : User | None = user_service.get_user(uid)
    if user:
        return asdict(user), 200
    else:
        return "Error", 500
