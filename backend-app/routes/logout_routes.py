from flask import Blueprint
from controllers.logout_controller import *

logout_routes = Blueprint("logout_routes", __name__)


@logout_routes.route('/logout', methods=['POST'])
def logout_endpoint():
    return logout_user()
