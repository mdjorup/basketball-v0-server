from dotenv import load_dotenv
from firebase_admin import auth, credentials, firestore, initialize_app
from firebase_admin.exceptions import NotFoundError, PermissionDeniedError
from flask import Flask
from flask_cors import CORS

from app.config import firebase_credentials, origins
from app.exception_handlers import (handle_bad_request,
                                    handle_email_already_exists,
                                    handle_exception, handle_not_found,
                                    handle_permission_denied,
                                    handle_server_error,
                                    handle_user_creation_failed)
from app.exceptions import (BadRequestError, ServerError,
                            UserCreationFailedError)
from app.middlewares import before_request
from app.routes.game_routes import game_blueprint
from app.routes.league_routes import league_blueprint
from app.routes.organization_routes import organization_blueprint
from app.routes.player_routes import player_blueprint
from app.routes.team_routes import team_blueprint
from app.routes.user_routes import user_blueprint

load_dotenv()

app = Flask(__name__)
CORS(app, origins=origins)

app.config["FIREBASE_ADMIN_SDK"] = firebase_credentials

cred = credentials.Certificate(app.config["FIREBASE_ADMIN_SDK"])
initialize_app(cred)

db = firestore.client()

app.config["FIRESTORE_DB"] = db



app.register_error_handler(auth.EmailAlreadyExistsError, handle_email_already_exists)
app.register_error_handler(UserCreationFailedError, handle_user_creation_failed)
app.register_error_handler(NotFoundError, handle_not_found)
app.register_error_handler(PermissionDeniedError, handle_permission_denied)
app.register_error_handler(ServerError, handle_server_error)
app.register_error_handler(BadRequestError, handle_bad_request)
app.register_error_handler(Exception, handle_exception)
app.register_error_handler(404, handle_not_found)
app.before_request(before_request)
app.register_blueprint(user_blueprint, url_prefix="/users")
app.register_blueprint(game_blueprint, url_prefix="/games")
app.register_blueprint(league_blueprint, url_prefix="/leagues")
app.register_blueprint(organization_blueprint, url_prefix="/organizations")
app.register_blueprint(player_blueprint, url_prefix="/players")
app.register_blueprint(team_blueprint, url_prefix="/teams")
