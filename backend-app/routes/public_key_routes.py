from flask import Blueprint
from controllers.public_key_controller import *

public_key_routes = Blueprint("public_key_routes", __name__)


@public_key_routes.route('/public-keys', methods=['POST'])
def create_public_key_endpoint():
    return create()


@public_key_routes.route('/public-keys/<int:session_id>/<int:user_id>', methods=['GET'])
def get_key_ring_by_session_id_by_user_id_endpoint(session_id, user_id):
    return get_by_session_id_and_user_id(session_id, user_id)
