from flask import Blueprint
from controllers.organisation_controller import *

organisation_routes = Blueprint("organisation_routes", __name__)


@organisation_routes.route('/organisations', methods=['POST'])
def create_new_organisation_endpoint():
    return create()


@organisation_routes.route('/organisations', methods=['GET'])
def get_organisations_endpoint():
    return get_all()


@organisation_routes.route('/organisations/<int:organisation_id>', methods=['GET'])
def get_organisation_by_id_endpoint(organisation_id):
    return get_by_id(organisation_id)


@organisation_routes.route('/organisations/<int:organisation_id>', methods=['PUT'])
def update_organisation_by_id_endpoint(organisation_id):
    return update(organisation_id)


@organisation_routes.route('/organisations/<int:organisation_id>', methods=['DELETE'])
def delete_organisation_endpoint(organisation_id):
    return delete(organisation_id)
