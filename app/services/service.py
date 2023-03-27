from abc import ABC

from app.database import get_db


class Service(ABC):
    def __init__(self):
        self.db = get_db()
