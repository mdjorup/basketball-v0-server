from dataclasses import asdict
from datetime import datetime, timezone
from uuid import uuid4

from firebase_admin.exceptions import NotFoundError

from app.models.organization_model import Organization
from app.services.service import Service


class OrganizationService(Service):
    
    def create_organization(self, name : str, owner_uid : str) -> Organization:


        coaches = [owner_uid]
        organization_id = str(uuid4())
        organization : Organization = Organization(organization_id=organization_id, name=name, owner=owner_uid, coaches=coaches)

        self.db.collection("organizations").document(organization_id).set(asdict(organization))

        return organization
    
    def get_organization_metadata(self, organization_id : str) -> Organization:
        organization_doc = self.db.collection("organizations").document(organization_id).get()
        if not organization_doc.exists:
            raise NotFoundError(f"Organization with ID {organization_id} not found.")
        organization = Organization(**organization_doc.to_dict())
        return organization
    
    def get_organization_deep(self, organization_id : str) -> Organization:
        organization = self.get_organization_metadata(organization_id)
        # organization.teams = self.team_service.get_teams_by_organization(organization_id)
        # organization.players = self.player_service.get_players_by_organization(organization_id)
        return organization
    
    def update_organization(self, organization : Organization) -> Organization:
        organization_id = organization.organization_id
        self.db.collection("organizations").document(organization_id).set(asdict(organization))
        return organization
    
    def delete_organization(self, organization_id : str) -> None:
        self.db.collection("organizations").document(organization_id).set({"active": False})

    
        

