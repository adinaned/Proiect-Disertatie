from flask import Blueprint
from controllers.user_controller import *

user_routes = Blueprint("user_routes", __name__)


@user_routes.route('/users', methods=['POST'])
def create_new_user_endpoint():
    return create()


@user_routes.route('/users', methods=['GET'])
def get_users_endpoint():
    return get_all()


@user_routes.route('/users/<int:user_id>', methods=['GET'])
def get_user_by_id_endpoint(user_id):
    return get_by_id(user_id)


@user_routes.route('/users/<int:user_id>', methods=['PUT'])
def update_user_by_id_endpoint(user_id):
    return update(user_id)


@user_routes.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user_endpoint(user_id):
    return delete(user_id)
