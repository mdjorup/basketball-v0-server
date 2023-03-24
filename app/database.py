from flask import current_app


def get_db():
    return current_app.config["FIRESTORE_DB"]
