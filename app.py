import json
import os

from dotenv import load_dotenv
from firebase_admin import credentials, firestore, initialize_app
from flask import Flask

app = Flask(__name__)

load_dotenv()

firebase_credentials = json.loads(
    os.environ.get("FIREBASE_SERVICE_ACCOUNT_CONFIG_JSON", "")
)
app.config["FIREBASE_ADMIN_SDK"] = firebase_credentials

cred = credentials.Certificate(app.config["FIREBASE_ADMIN_SDK"])
initialize_app(cred)

db = firestore.client()


# Users
@app.route("/")
def index():
    return "Hello World"


@app.route("/users", methods=["GET", "POST"])
def users():
    return ""


@app.route("/users/<user_id>", methods=["GET", "PUT", "DELETE"])
def user(user_id):
    return ""


@app.route("/users/register", methods=["POST"])
def user_register():
    return ""


@app.route("/users/me", methods=["GET"])
def user_me():
    return ""


if __name__ == "__main__":
    app.run()
