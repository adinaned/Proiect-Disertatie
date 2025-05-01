from flask import Blueprint
from controllers.option_controller import *

option_routes = Blueprint("option_routes", __name__)


@option_routes.route('/options', methods=['POST'])
def create_new_option_endpoint():
    return create()


@option_routes.route('/options', methods=['GET'])
def get_options_endpoint():
    return get_all()


@option_routes.route('/options/<int:option_id>', methods=['GET'])
def get_option_by_id_endpoint(option_id):
    return get_by_id(option_id)


@option_routes.route('/options/<int:option_id>', methods=['PUT'])
def update_option_by_id_endpoint(option_id):
    return update(option_id)


@option_routes.route('/options/<int:option_id>', methods=['DELETE'])
def delete_option_endpoint(option_id):
    return delete(option_id)
