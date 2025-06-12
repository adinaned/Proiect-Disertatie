from flask import Blueprint
from controllers.voting_session_controller import *

voting_session_routes = Blueprint("voting_session_routes", __name__)


@voting_session_routes.route('/voting_sessions', methods=['POST'])
def create_new_voting_session_endpoint():
    return create()


@voting_session_routes.route("/voting_sessions/<string:voting_session_id>/ring", methods=["GET"])
def get_ring_endpoint(voting_session_id):
    return get_ring(voting_session_id)


@voting_session_routes.route('/voting_sessions', methods=['GET'])
def get_voting_sessions_endpoint():
    return get_all()


@voting_session_routes.route('/voting_sessions/<string:voting_session_id>', methods=['GET'])
def get_voting_session_by_id_endpoint(voting_session_id):
    return get_by_id(voting_session_id)


@voting_session_routes.route('/voting_sessions/organization/<string:organization_id>', methods=['GET'])
def get_all_voting_sessions_by_organization_id_endpoint(organization_id):
    return get_all_by_organization_id(organization_id)


@voting_session_routes.route('/voting_sessions/organization/<string:organization_id>/role/<string:role_id>', methods=['GET'])
def get_all_voting_sessions_by_organization_id_and_role_id_endpoint(organization_id, role_id):
    return get_all_by_organization_id_and_role_id(organization_id, role_id)


@voting_session_routes.route('/voting_sessions/<string:voting_session_id>', methods=['PATCH'])
def update_voting_session_by_id_endpoint(voting_session_id):
    return update(voting_session_id)


@voting_session_routes.route('/voting_sessions/<string:voting_session_id>', methods=['DELETE'])
def delete_voting_session_endpoint(voting_session_id):
    return delete(voting_session_id)
