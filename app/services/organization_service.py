
from app.services.service import Service


class OrganizationService(Service):
    
    def __init__(self, operating_uid="", admin=False) -> None:
        super().__init__()

        self.operating_uid : str = operating_uid
        self.admin : bool = admin
    
        

