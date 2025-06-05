from flask import Blueprint
from controllers.option_controller import *

option_routes = Blueprint("option_routes", __name__)


@option_routes.route('/options/<int:session_id>', methods=['POST'])
def create_new_option_endpoint(session_id):
    return create(session_id)


@option_routes.route('/options', methods=['GET'])
def get_options_endpoint():
    return get_all()


@option_routes.route('/options/<int:option_id>', methods=['GET'])
def get_option_by_id_endpoint(option_id):
    return get_by_id(option_id)


@option_routes.route('/options/session/<int:session_id>', methods=['GET'])
def get_option_by_session_id_endpoint(session_id):
    return get_by_session_id(session_id)


@option_routes.route('/options/<int:option_id>', methods=['PUT'])
def update_option_by_id_endpoint(option_id):
    return update(option_id)


@option_routes.route('/options/<int:option_id>', methods=['DELETE'])
def delete_option_endpoint(option_id):
    return delete(option_id)
