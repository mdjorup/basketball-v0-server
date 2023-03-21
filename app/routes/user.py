
from flask import Blueprint, g, request

from app.database import get_db

user_blueprint = Blueprint("user", __name__)

@user_blueprint.route("/", methods=["GET"])
def index():
    return "Hello World"


@user_blueprint.route("/", methods=["POST"])
def users():

    db = get_db()

    if request.method == "POST":
        data : dict = request.get_json()
        return {} #create_user(auth, db, data)
    return {}


@user_blueprint.route("/<user_id>", methods=["GET", "PUT", "DELETE"])
def user(user_id):
    return ""


@user_blueprint.route("/register", methods=["POST"])
def user_register():
    return ""


@user_blueprint.route("/me", methods=["GET"])
def user_me():
    return "sdklfaj"