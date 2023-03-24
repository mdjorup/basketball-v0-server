from firebase_admin.auth import EmailAlreadyExistsError
from firebase_admin.exceptions import NotFoundError, PermissionDeniedError
from flask import Blueprint

from app.exceptions import BadRequestError, ServerError, UserCreationFailedError
from app.routes.responses import build_response


def build_error_response(status_code: int, error: Exception) -> tuple[dict, int]:
    return build_response({}, status_code, str(error), type(error).__name__)


def handle_email_already_exists(error: EmailAlreadyExistsError):
    return build_error_response(409, error)


def handle_user_creation_failed(error: UserCreationFailedError):
    return build_error_response(500, error)


def handle_not_found(error: NotFoundError):
    return build_error_response(404, error)


def handle_permission_denied(error: PermissionDeniedError):
    return build_error_response(401, error)


def handle_server_error(error: ServerError):
    return build_error_response(500, error)


def handle_bad_request(error: BadRequestError):
    return build_error_response(400, error)


def handle_exception(error: Exception):
    return build_error_response(500, error)
