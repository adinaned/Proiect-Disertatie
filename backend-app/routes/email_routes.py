from flask import Blueprint
from controllers.email_controller import *

email_routes = Blueprint("email_routes", __name__)


@email_routes.route('/emails', methods=['POST'])
def create_new_email_endpoint():
    return create()


@email_routes.route('/emails/<string:email_address>', methods=['GET'])
def get_email_by_name_endpoint(email_address):
    return get_by_name(email_address)

@email_routes.route('/emails/user/<int:user_id>', methods=['GET'])
def get_email_by_user_id_endpoint(user_id):
    return get_by_user_id(user_id)


@email_routes.route('/emails/<int:email_id>', methods=['PUT'])
def update_email_by_id_endpoint(email_id):
    return update(email_id)


@email_routes.route('/emails/<int:email_id>', methods=['DELETE'])
def delete_email_endpoint(email_id):
    return delete(email_id)
