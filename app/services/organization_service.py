from uuid import uuid4

from firebase_admin.exceptions import NotFoundError

from app.models.organization_model import Organization
from app.models.player_model import Player
from app.models.team_model import Team
from app.models.user_model import User
from app.services.service import Service
from app.services.user_service import UserService


class OrganizationService(Service):
    def __init__(self, operating_uid="", admin=False) -> None:
        super().__init__()

        self.operating_uid: str = operating_uid
        self.admin: bool = admin

    def _create(self, model: Organization) -> None:
        self.db.collection("organizations").document(model.organization_id).set(
            model.__dict__()
        )

    def _read(self, id: str, deep=False) -> Organization:
        organization_ref = self.db.collection("organizations").document(id)
        organization_doc = organization_ref.get()
        if not organization_doc.exists:
            raise NotFoundError("Organization not found")
        data = organization_doc.to_dict()
        organization = Organization(
            **data
        )  # may need to change this depending on response
        if not organization.active:
            raise NotFoundError("Organization not found")
        if not deep:
            return organization

        # TODO: May want to take advantage of the player and team services here

        # get all players
        players_ref = organization_ref.collection("players")
        players_docs = players_ref.stream()
        players: list[Player] = list(
            filter(
                lambda p: p.active,
                [Player(**player.to_dict()) for player in players_docs],
            )
        )

        organization.players = players

        # get all teams
        teams_ref = organization_ref.collection("teams")
        teams_docs = teams_ref.stream()
        teams: list[Team] = list(
            filter(lambda t: t.active, [Team(**team.to_dict()) for team in teams_docs])
        )

        organization.teams = teams

        return organization

    def _update(self, model: Organization) -> None:
        # How do we update an organization?
        # tricky cases are adding and removing teams and players
        # Theory is that teams and players updates aren't updates to the organization
        # but rather updates to the organization's teams and players
        # So adding a team or adding a player isn't reflected in the organization changes
        self.db.collection("organizations").document(model.organization_id).update(
            model.changes
        )

    def _delete(self, model: Organization) -> None:
        self.db.collection("organizations").document(model.organization_id).delete()

    def create_organization(self, name: str) -> Organization:
        owner = self.operating_uid
        coaches: list[str] = [owner]
        organization_id: str = str(uuid4())
        organization: Organization = Organization(
            organization_id=organization_id,
            name=name,
            owner=owner,
            coaches=coaches,
        )

        self._create(organization)
        return organization

    def get_organization(self, organization_id: str) -> Organization:
        return self._read(organization_id)

    def delete_organization(self, organization_id: str) -> None:
        organization = self._read(organization_id)

        if organization.owner != self.operating_uid and not self.admin:
            raise PermissionError(
                "You do not have permission to delete this organization"
            )
        elif organization.active == False:
            raise NotFoundError("Organization not found")

        organization.delete()

        self._update(organization)

    def get_organization_coaches(self, organization_id: str) -> list[User]:
        organization = self._read(organization_id)
        coach_ids: list[str] = organization.coaches

        user_service = UserService()
        coaches: list[User] = user_service.get_users_by_ids(coach_ids)
        return coaches

    def add_user_to_organization(self, organization_id: str, user_id: str) -> None:
        organization = self._read(organization_id)
        if organization.owner != self.operating_uid and not self.admin:
            raise PermissionError(
                "You do not have permission to add a user to this organization"
            )
        elif organization.active == False:
            raise NotFoundError("Organization not found")
        elif user_id in organization.coaches:
            raise ValueError("User is already a coach")

        user_service = UserService()
        user = user_service.get_user(user_id)
        if user.active == False:
            raise NotFoundError("User not found")
        elif user.role != "coach":
            raise ValueError("User is not a coach")

        organization.add_coach(user.uid)

        self._update(organization)

    def remove_user_from_organization(self, organization_id: str, user_id: str) -> None:
        organization = self._read(organization_id)

        if organization.owner != self.operating_uid and not self.admin:
            raise PermissionError(
                "You do not have permission to remove a user from this organization"
            )
        elif organization.active == False:
            raise NotFoundError("Organization not found")
        elif user_id not in organization.coaches:
            raise ValueError("User is not a coach")
        elif user_id == organization.owner:
            raise ValueError("You cannot remove the owner from the organization")

        organization.remove_coach(user_id)
        self._update(organization)

    def transfer_organization_ownership(
        self, organization_id: str, user_id: str
    ) -> None:
        organization = self._read(organization_id)

        if organization.owner != self.operating_uid and not self.admin:
            raise PermissionError(
                "You do not have permission to transfer ownership of this organization"
            )
        elif organization.active == False:
            raise NotFoundError("Organization not found")
        elif user_id not in organization.coaches:
            raise ValueError("User is not a coach")

        organization.update_field("owner", user_id)

        self._update(organization)
