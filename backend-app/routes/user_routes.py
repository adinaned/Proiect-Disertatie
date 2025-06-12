from flask import Blueprint
from controllers.user_controller import *

user_routes = Blueprint("user_routes", __name__)


@user_routes.route('/users', methods=['POST'])
def create_new_user_endpoint():
    return create()


@user_routes.route('/users/<string:user_id>', methods=['GET'])
def get_user_by_id_endpoint(user_id):
    return get_by_id(user_id)


@user_routes.route('/users/organization/<string:organization_id>', methods=['GET'])
def get_user_by_organization_id_endpoint(organization_id):
    return get_all_by_organization_id(organization_id)


@user_routes.route('/users/<string:user_id>', methods=['PATCH'])
def update_user_by_id_endpoint(user_id):
    return update(user_id)


@user_routes.route('/users/<string:user_id>', methods=['DELETE'])
def delete_user_endpoint(user_id):
    return delete(user_id)
