from flask import Blueprint
from controllers.option_controller import *

option_routes = Blueprint("option_routes", __name__)


@option_routes.route('/options/<string:voting_session_id>', methods=['POST'])
def create_new_option_endpoint(voting_session_id):
    return create(voting_session_id)


@option_routes.route('/options/<string:option_id>', methods=['GET'])
def get_option_by_id_endpoint(option_id):
    return get_by_id(option_id)


@option_routes.route('/options/voting_session/<string:voting_session_id>', methods=['GET'])
def get_option_by_session_id_endpoint(voting_session_id):
    return get_by_session_id(voting_session_id)


@option_routes.route('/options/<string:option_id>', methods=['PATCH'])
def update_option_by_id_endpoint(option_id):
    return update(option_id)


@option_routes.route('/options/<string:option_id>', methods=['DELETE'])
def delete_option_endpoint(option_id):
    return delete(option_id)


@option_routes.route('/options/voting_session/<string:voting_session_id>', methods=['DELETE'])
def delete_options_by_session_id_endpoint(voting_session_id):
    return delete_by_session_id(voting_session_id)
