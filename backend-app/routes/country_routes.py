from flask import Blueprint
from controllers.country_controller import *

country_routes = Blueprint("country_routes", __name__)


@country_routes.route('/countries', methods=['POST'])
def create_new_country_endpoint():
    return create()


@country_routes.route('/countries', methods=['GET'])
def get_countries_endpoint():
    return get_all()


@country_routes.route('/countries/<country>', methods=['GET'])
def get_country_by_id_or_name_endpoint(country):
    return get_by_id_or_name(country)
