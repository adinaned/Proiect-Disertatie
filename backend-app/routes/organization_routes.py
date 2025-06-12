from flask import Blueprint
from controllers.organization_controller import *

organization_routes = Blueprint("organization_routes", __name__)


@organization_routes.route('/organizations', methods=['POST'])
def create_new_organization_endpoint():
    return create()


@organization_routes.route('/organizations', methods=['GET'])
def get_organizations_endpoint():
    return get_all()


@organization_routes.route('/organizations/<string:organization_filter>', methods=['GET'])
def get_organization_by_name_or_id_endpoint(organization_filter):
    return get_by_name_or_id(organization_filter)


@organization_routes.route('/organizations/<string:organization_id>', methods=['PATCH'])
def update_organization_by_id_endpoint(organization_id):
    return update(organization_id)


@organization_routes.route('/organizations/<string:organization_id>', methods=['DELETE'])
def delete_organization_endpoint(organization_id):
    return delete(organization_id)
