from flask import Blueprint
from controllers.password_controller import *

password_routes = Blueprint("password_routes", __name__)


@password_routes.route('/passwords', methods=['POST'])
def create_new_password_endpoint():
    return create()


@password_routes.route('/passwords/<int:user_id>', methods=['GET'])
def get_password_by_user_id_endpoint(user_id):
    return get_by_user_id(user_id)


@password_routes.route('/passwords/<int:user_id>', methods=['PUT'])
def update_password_by_id_endpoint(user_id):
    return update(user_id)


@password_routes.route('/passwords/<int:user_id>', methods=['DELETE'])
def delete_password_endpoint(user_id):
    return delete(user_id)
