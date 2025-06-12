from flask import Blueprint
from controllers.password_controller import *

password_routes = Blueprint("password_routes", __name__)


@password_routes.route('/passwords/<string:user_id>', methods=['GET'])
def get_password_by_user_id_endpoint(user_id):
    return get_by_user_id(user_id)


@password_routes.route('/passwords/<string:user_id>', methods=['PATCH'])
def update_password_by_id_endpoint(user_id):
    return update(user_id)
