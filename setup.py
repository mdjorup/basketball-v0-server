import json
import os

from dotenv import load_dotenv
from firebase_admin import credentials, firestore, initialize_app
from flask import Flask
from flask_cors import CORS

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