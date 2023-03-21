
from dataclasses import asdict

from flask import Blueprint, g, request

from app.models.user_model import User
from app.services.user_service import UserService

user_blueprint = Blueprint("user", __name__)

@user_blueprint.post("/")
def users():

    user_service = UserService()

    new_user : User | None = user_service.create_user("Michael", "michael.djorup@gmail.com", "password", "standard")
    if new_user:   
        return asdict(new_user)
    else:
        return {}


@user_blueprint.get("/<user_id>")
def user(user_id : str):

    user_service = UserService()
    
    user : User | None = user_service.get_user(user_id)
    if user:
        return asdict(user)
    else:
        return {}
    


@user_blueprint.route("/register", methods=["POST"])
def user_register():
    return ""


@user_blueprint.route("/me", methods=["GET"])
def user_me():
    return "sdklfaj"