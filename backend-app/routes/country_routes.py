from flask import Blueprint
from controllers.country_controller import *

country_routes = Blueprint("country_routes", __name__)


@country_routes.route('/countries', methods=['POST'])
def create_new_country_endpoint():
    return create()


@country_routes.route('/countries', methods=['GET'])
def get_countries_endpoint():
    return get_all()


@country_routes.route('/countries/<int:country_id>', methods=['GET'])
def get_country_by_id_endpoint(country_id):
    return get_by_id(country_id)


@country_routes.route('/countries/<int:country_id>', methods=['PUT'])
def update_country_by_id_endpoint(country_id):
    return update(country_id)


@country_routes.route('/countries/<int:country_id>', methods=['DELETE'])
def delete_country_endpoint(country_id):
    return delete(country_id)
