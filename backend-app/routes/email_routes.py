from flask import Blueprint
from controllers.email_controller import *

email_routes = Blueprint("email_routes", __name__)


@email_routes.route('/emails/user/<string:user_id>', methods=['GET'])
def get_email_by_user_id_endpoint(user_id):
    return get_by_user_id(user_id)


@email_routes.route('/emails/<string:email_address>', methods=['GET'])
def get_email_by_email_address_endpoint(email_address):
    return get_by_email_address(email_address)
