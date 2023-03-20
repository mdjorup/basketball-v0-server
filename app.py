import json
import os

from dotenv import load_dotenv
from firebase_admin import auth, credentials, firestore, initialize_app
from flask import Flask, g, request
from flask_cors import CORS

from user.user_handler import create_user

app = Flask(__name__)
CORS(app, origins=["http://localhost:3000", "https://basketball-v0-906cb.web.app", "https://basketball-v0-906cb.firebaseapp.com"] )


load_dotenv()

firebase_credentials = json.loads(
    os.environ.get("FIREBASE_SERVICE_ACCOUNT_CONFIG_JSON", "")
)
app.config["FIREBASE_ADMIN_SDK"] = firebase_credentials

cred = credentials.Certificate(app.config["FIREBASE_ADMIN_SDK"])
initialize_app(cred)

db = firestore.client()

@app.before_request
def before_request():
    auth_header : str = request.headers.get("Authorization", "")

    if auth_header and auth_header.startswith("Bearer "):
        token : str = auth_header.split("Bearer ")[1]
        # this is where the token is validated and the user is retrieved
        try:
            decoded_token : dict = auth.verify_id_token(token)
            # user = auth.get_user(decoded_token["uid"])
        except auth.InvalidIdTokenError:
            decoded_token = {}
        # now use the token to create a user object
        g.user = decoded_token # will be changed later to user object
    else:
        g.user = None
        

# Users
@app.route("/")
def index():
    return "Hello World"


@app.route("/users", methods=["POST"])
def users():

    if request.method == "POST":
        data : dict = request.get_json()
        return create_user(auth, db, data)
    return {}


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
