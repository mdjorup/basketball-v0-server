import json
import os

from dotenv import load_dotenv
from flask import Flask

app = Flask(__name__)

load_dotenv()

@app.route("/")
def index():
    return "Hello World"

@app.route("/project")
def project():
    env_variable : str = os.environ.get("FIREBASE_SERVICE_ACCOUNT_CONFIG_JSON", "")
    env_json = json.loads(env_variable)
    return env_json.get("project_id", "No project id found")

if __name__ == "__main__":
    app.run()


