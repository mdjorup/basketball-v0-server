from firebase_admin.auth import EmailAlreadyExistsError
from firebase_admin.exceptions import NotFoundError, PermissionDeniedError
from flask import Blueprint

from app.exceptions import (BadRequestError, ServerError,
                            UserCreationFailedError)


def handle_email_already_exists(error):
    return str(error), 409

def handle_user_creation_failed(error):
    return str(error), 500

def handle_not_found(error):
    return str(error), 404

def handle_permission_denied(error):
    print("getting to permission denied error")
    return str(error), 401

def handle_server_error(error):
    return str(error), 500

def handle_bad_request(error):
    return str(error), 400

def handle_exception(error):
    return str(error), 500