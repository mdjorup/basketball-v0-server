from dataclasses import asdict

from flask import Blueprint, g, request

from app.exceptions import BadRequestError
from app.middlewares import authorized_roles
from app.models.organization_model import Organization
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


# @organization_blueprint.route("/", methods=["POST"])
# @authorized_roles(["coach"])
# def create_new_organization():
#     if not request.is_json:
#         raise BadRequestError("Request body must be JSON")
    
#     request_json: dict = request.get_json()
#     name: str = request_json["name"]
#     coach_uid : str = g.decoded_token.get("uid")
#     if not coach_uid:
#         raise BadRequestError("User must be logged in to create an organization")
    
#     organization_service = OrganizationService()
#     new_organization = organization_service.create_organization(name, coach_uid)

#     return build_response({"organization": asdict(new_organization)}, 201, "Organization created successfully")


# @organization_blueprint.route("/<organization_id>", methods=["DELETE"])
# @authorized_roles(["coach", "admin"])
# def delete_organization_by_id(organization_id: str):
#     user_uid = g.decoded_token.get("uid")
#     user_role = g.decoded_token.get("role")
#     organization_service = OrganizationService()
#     organization = organization_service.get_organization_metadata(organization_id)
#     if not organization:
#         raise BadRequestError("Organization does not exist")
#     elif user_role != "admin" and not user_uid in organization.coaches:
#         raise PermissionError("User does not have permission to delete this organization")
#     organization_service.delete_organization(organization.organization_id)
#     return build_response({}, 204, "Organization deleted successfully")


# @organization_blueprint.route("/<organization_id>/coaches", methods=["GET"])
# def get_coaches_from_organization(organization_id: str):
#     organization_service = OrganizationService()
#     organization = organization_service.get_organization_metadata(organization_id)
#     if not organization:
#         raise BadRequestError("Organization does not exist")
    
    
    
#     return build_response({}, 200, "Coaches retrieved successfully")


# @organization_blueprint.route("/<organization_id>/coaches/<coach_uid>", methods=["GET"])
# def get_coach_from_organization(organization_id: str, coach_uid: str):
#     return build_response({}, 200, "Coach retrieved successfully")


# @organization_blueprint.route("/<organization_id>/coaches", methods=["POST"])
# def add_coach_to_organization(organization_id: str):
#     return build_response({}, 200, "Coach added successfully")


# @organization_blueprint.route(
#     "/<organization_id>/coaches/<coach_uid>", methods=["DELETE"]
# )
# def delete_coach_from_organization(organization_id: str, coach_uid: str):
#     return build_response({}, 200, "Coach deleted successfully")


# @organization_blueprint.route("/<organization_id>/coaches/transfer", methods=["POST"])
# def transfer_ownership_to_coach(organization_id: str):
#     return build_response({}, 200, "Ownership transferred successfully")


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
