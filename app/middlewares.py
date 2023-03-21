from functools import wraps

from firebase_admin import auth
from flask import g, request


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
        except Exception:
            decoded_token = {}
        # now use the token to create a user object
        g.decoded_token = decoded_token
    else:
        g.decoded_token = {}


def authorized_roles(roles_list):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            user_role = g.get('decoded_token', {}).get('role')
            if user_role not in roles_list:
                return {'message': 'Unauthorized access.'}, 401
            return func(*args, **kwargs)
        return wrapper
    return decorator


def require_login(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not g.get('decoded_token', {}):
            return {'message': 'Unauthorized access.'}, 401
        return func(*args, **kwargs)
    return wrapper


