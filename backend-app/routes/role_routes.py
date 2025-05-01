from flask import Blueprint
from controllers.role_controller import *

role_routes = Blueprint("role_routes", __name__)


@role_routes.route('/roles', methods=['POST'])
def create_new_role_endpoint():
    return create()


@role_routes.route('/roles', methods=['GET'])
def get_roles_endpoint():
    return get_all()


@role_routes.route('/roles/<int:role_id>', methods=['GET'])
def get_role_by_id_endpoint(role_id):
    return get_by_id(role_id)


@role_routes.route('/roles/<int:role_id>', methods=['PUT'])
def update_role_by_id_endpoint(role_id):
    return update(role_id)


@role_routes.route('/roles/<int:role_id>', methods=['DELETE'])
def delete_role_endpoint(role_id):
    return delete(role_id)
