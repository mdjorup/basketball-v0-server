from flask import Blueprint

organization_blueprint = Blueprint("organization", __name__)

# create organization -> need name, owner uid
# delete an organization -> soft delete
# add a coach -> owner must make the request, adds an existing uid to the
# delete a coach -> owner must make the request, removes a uid from the coaches list
# transfer owneership -> owner transfers ownership to a coach
# add a player -> creates player object, adds it to the players subcollection
# remove a player -> removes the player from the subcollection
# create a team -> creates the team and adds it to the subcollection
# Remove a team -> removes the team from the subcollection
