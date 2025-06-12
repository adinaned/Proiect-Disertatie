from flask import Blueprint
from controllers.public_key_controller import *

public_key_routes = Blueprint("public_key_routes", __name__)


@public_key_routes.route('/public_keys', methods=['POST'])
def create_public_key_endpoint():
    return create()


@public_key_routes.route('/public_keys/<string:voting_session_id>', methods=['GET'])
def get_key_ring_by_session_id_endpoint(voting_session_id):
    return get_by_session_id(voting_session_id)
