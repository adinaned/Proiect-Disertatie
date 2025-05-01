from flask import Blueprint
from controllers.profile_status_controller import *

profile_status_routes = Blueprint("profile_status_routes", __name__)


@profile_status_routes.route('/profile_statuses', methods=['POST'])
def create_new_profile_status_endpoint():
    return create()


@profile_status_routes.route('/profile_statuses', methods=['GET'])
def get_profile_statuses_endpoint():
    return get_all()


@profile_status_routes.route('/profile_statuses/<int:profile_status_id>', methods=['GET'])
def get_profile_status_by_id_endpoint(profile_status_id):
    return get_by_id(profile_status_id)


@profile_status_routes.route('/profile_statuses/<int:profile_status_id>', methods=['PUT'])
def update_profile_status_by_id_endpoint(profile_status_id):
    return update(profile_status_id)


@profile_status_routes.route('/profile_statuses/<int:profile_status_id>', methods=['DELETE'])
def delete_profile_status_endpoint(profile_status_id):
    return delete(profile_status_id)
