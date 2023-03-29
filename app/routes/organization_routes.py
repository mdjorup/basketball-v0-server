from dataclasses import asdict

from flask import Blueprint, g, request

from app.exceptions import BadRequestError
from app.middlewares import authorized_roles
from app.models.organization_model import Organization
from app.models.user_model import User
from app.routes.responses import build_response
from app.services.organization_service import OrganizationService

organization_blueprint = Blueprint("organizations", __name__)

# create organization -> need name, owner uid
# delete an organization -> soft delete
# add a coach -> owner must make the request, adds an existing uid to the
# delete a coach -> owner must make the request, removes a uid from the coaches list
# transfer owneership -> owner transfers ownership to a coach
# add a player -> creates player object, adds it to the players subcollection
# remove a player -> removes the player from the subcollection
# create a team -> creates the team and adds it to the subcollection
# Remove a team -> removes the team from the subcollection


@organization_blueprint.route("/", methods=["POST"])
@authorized_roles(["coach"])
def create_new_organization():
    if not request.is_json:
        raise BadRequestError("Request body must be JSON")
    
    request_json: dict = request.get_json()
    name: str = request_json["name"]
    coach_uid : str = g.decoded_token.get("uid")
    if not coach_uid:
        raise BadRequestError("User must be logged in to create an organization")
    
    organization_service = OrganizationService(operating_uid=coach_uid)
    new_organization = organization_service.create_organization(name)

    return build_response({"organization": new_organization.__dict__()}, 201, "Organization created successfully")


@organization_blueprint.route("/<organization_id>", methods=["GET"])
def get_organization_by_id(organization_id: str):
    organization_service = OrganizationService()
    organization: Organization = organization_service.get_organization(organization_id)
    return build_response({"organization": organization.__dict__()}, 200, "Organization retrieved successfully")


@organization_blueprint.route("/<organization_id>", methods=["DELETE"])
@authorized_roles(["coach", "admin"])
def delete_organization_by_id(organization_id: str):
    user_uid = g.decoded_token.get("uid")
    user_role = g.decoded_token.get("role")
    admin = user_role == "admin"
    organization_service = OrganizationService(operating_uid=user_uid, admin=admin)

    organization_service.delete_organization(organization_id)

    return build_response({}, 204, f"Organization {organization_id} deleted successfully")
    
    
@organization_blueprint.route("/<organization_id>/coaches", methods=["GET"])
def get_coaches_from_organization(organization_id: str):
    organization_service = OrganizationService()
    
    coaches : list[User] = organization_service.get_organization_coaches(organization_id)
    coaches_json = [coach.__dict__() for coach in coaches]
    
    
    return build_response({"coaches": coaches_json}, 200, "Coaches retrieved successfully")


@organization_blueprint.route("/<organization_id>/coaches/add", methods=["PUT"])
@authorized_roles(["coach", "admin"])
def add_coach_to_organization(organization_id: str):
    # need the user uid of the user to add as a coach
    req = request.get_json()
    coach_uid = req.get("uid")
    if not coach_uid:
        raise BadRequestError("Must provide a uid to add as a coach")

    user_uid = g.decoded_token.get("uid")
    user_role = g.decoded_token.get("role")
    admin = user_role == "admin"
    organization_service = OrganizationService(operating_uid=user_uid, admin=admin)
    organization_service.add_user_to_organization(organization_id, coach_uid)
    return build_response({}, 200, "Coach added successfully")


@organization_blueprint.route(
    "/<organization_id>/coaches/remove", methods=["PUT"]
)
@authorized_roles(["coach", "admin"])
def remove_coach_from_organization(organization_id: str):
    coach_uid = request.get_json().get("uid")
    if not coach_uid:
        raise BadRequestError("Must provide a uid to remove as a coach")
    
    user_uid = g.decoded_token.get("uid")
    user_role = g.decoded_token.get("role")
    admin = user_role == "admin"

    organization_service = OrganizationService(operating_uid=user_uid, admin=admin)
    organization_service.remove_user_from_organization(organization_id, coach_uid)

    return build_response({}, 200, f"Coach {coach_uid} deleted successfully from organization {organization_id}")


@organization_blueprint.route("/<organization_id>/coaches/transfer", methods=["PUT"])
@authorized_roles(["coach", "admin"])
def transfer_ownership_to_coach(organization_id: str):
    coach_uid = request.get_json().get("uid")
    if not coach_uid:
        raise BadRequestError("Must provide a uid to remove as a coach")
    
    user_uid = g.decoded_token.get("uid")
    user_role = g.decoded_token.get("role")
    admin = user_role == "admin"

    organization_service = OrganizationService(operating_uid=user_uid, admin=admin)
    organization_service.transfer_organization_ownership(organization_id, coach_uid)
    
    return build_response({}, 200, f"Ownership of Organization {organization_id} transferred to {coach_uid} successfully")



# Do these later, once players and teams are implemented


# @organization_blueprint.route("/<organization_id>/players", methods=["POST"])
# def add_player_to_organization(organization_id: str):
#     return build_response({}, 200, "Player added successfully")


# @organization_blueprint.route(
#     "/<organization_id>/players/<player_id>", methods=["DELETE"]
# )
# def delete_player_from_organization(organization_id: str, player_id: str):
#     return build_response({}, 200, "Player deleted successfully")


# @organization_blueprint.route("/<organization_id>/teams", methods=["POST"])
# def add_team_to_organization(organization_id: str):
#     return build_response({}, 200, "Team added successfully")


# @organization_blueprint.route("/<organization_id>/teams/<team_id>", methods=["DELETE"])
# def delete_team_from_organization(organization_id: str, team_id: str):
#     return build_response({}, 200, "Team deleted successfully")
