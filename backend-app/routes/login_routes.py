from flask import Blueprint, request, jsonify
from controllers.login_controller import login_user, get_current_user
from services import jwt_required

login_routes = Blueprint("login_routes", __name__)


@login_routes.route('/login', methods=['POST'])
def login_endpoint():
    return login_user()


@login_routes.route('/me', methods=['GET'])
@jwt_required
def me_endpoint():
    return get_current_user()
