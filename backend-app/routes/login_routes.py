from flask import Blueprint
from controllers.login_controller import *

login_routes = Blueprint("login_routes", __name__)


@login_routes.route('/login', methods=['POST'])
def get_login_endpoint():
    return login_user()