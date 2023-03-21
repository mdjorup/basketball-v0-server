from dotenv import load_dotenv
from firebase_admin import credentials, firestore, initialize_app
from flask import Flask
from flask_cors import CORS

from app.config import firebase_credentials, origins
from app.middlewares import before_request
from app.routes.user import user_blueprint

load_dotenv()

app = Flask(__name__)
CORS(app, origins=origins)

app.config["FIREBASE_ADMIN_SDK"] = firebase_credentials

cred = credentials.Certificate(app.config["FIREBASE_ADMIN_SDK"])
initialize_app(cred)

db = firestore.client()

app.before_request(before_request)
app.register_blueprint(user_blueprint, url_prefix="/user")

