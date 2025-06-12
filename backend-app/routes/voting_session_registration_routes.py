from flask import Blueprint
from controllers.voting_session_registration_controller import *

voting_session_registration_routes = Blueprint("voting_session_registration_routes", __name__)


@voting_session_registration_routes.route(
    '/voting_session_registrations/voting_session/<string:voting_session_id>/user/<string:user_id>', methods=['GET'])
def get_voting_session_registrations_by_session_id_and_user_id_endpoint(voting_session_id, user_id):
    return get_by_voting_session_id_and_user_id(voting_session_id, user_id)


@voting_session_registration_routes.route(
    '/voting_session_registrations/voting_session/<string:voting_session_id>', methods=['GET'])
def get_voting_session_registrations_by_session_id_endpoint(voting_session_id):
    return get_by_voting_session_id(voting_session_id)
