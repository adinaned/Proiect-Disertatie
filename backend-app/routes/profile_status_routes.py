from flask import Blueprint
from controllers.profile_status_controller import *

profile_status_routes = Blueprint("profile_status_routes", __name__)


@profile_status_routes.route('/profile_statuses/<string:user_id>', methods=['GET'])
def get_profile_status_by_user_id_endpoint(user_id):
    return get_by_user_id(user_id)


@profile_status_routes.route('/profile_statuses/<string:user_id>', methods=['PATCH'])
def update_profile_status_by_id_endpoint(user_id):
    return update_by_user_id(user_id)
