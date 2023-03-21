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
        g.token = decoded_token
    else:
        g.token = {}
