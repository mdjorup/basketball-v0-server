from flask import Blueprint

from app.routes.responses import build_response

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
def create_new_organization():
    return build_response({}, 200, "Organization created successfully")


@organization_blueprint.route("/<organization_id>", methods=["DELETE"])
def delete_organization_by_id(organization_id: str):
    return build_response({}, 200, "Organization deleted successfully")


@organization_blueprint.route("/<organization_id>/coaches", methods=["GET"])
def get_coaches_from_organization(organization_id: str):
    return build_response({}, 200, "Coaches retrieved successfully")


@organization_blueprint.route("/<organization_id>/coaches/<coach_uid>", methods=["GET"])
def get_coach_from_organization(organization_id: str, coach_uid: str):
    return build_response({}, 200, "Coach retrieved successfully")


@organization_blueprint.route("/<organization_id>/coaches", methods=["POST"])
def add_coach_to_organization(organization_id: str):
    return build_response({}, 200, "Coach added successfully")


@organization_blueprint.route(
    "/<organization_id>/coaches/<coach_uid>", methods=["DELETE"]
)
def delete_coach_from_organization(organization_id: str, coach_uid: str):
    return build_response({}, 200, "Coach deleted successfully")


@organization_blueprint.route("/<organization_id>/coaches/transfer", methods=["POST"])
def transfer_ownership_to_coach(organization_id: str):
    return build_response({}, 200, "Ownership transferred successfully")


@organization_blueprint.route("/<organization_id>/players", methods=["POST"])
def add_player_to_organization(organization_id: str):
    return build_response({}, 200, "Player added successfully")


@organization_blueprint.route(
    "/<organization_id>/players/<player_id>", methods=["DELETE"]
)
def delete_player_from_organization(organization_id: str, player_id: str):
    return build_response({}, 200, "Player deleted successfully")


@organization_blueprint.route("/<organization_id>/teams", methods=["POST"])
def add_team_to_organization(organization_id: str):
    return build_response({}, 200, "Team added successfully")


@organization_blueprint.route("/<organization_id>/teams/<team_id>", methods=["DELETE"])
def delete_team_from_organization(organization_id: str, team_id: str):
    return build_response({}, 200, "Team deleted successfully")
