from flask import Blueprint
from controllers.organization_controller import *

organization_routes = Blueprint("organization_routes", __name__)


@organization_routes.route('/organizations', methods=['POST'])
def create_new_organization_endpoint():
    return create()


@organization_routes.route('/organizations', methods=['GET'])
def get_organizations_endpoint():
    return get_all()


@organization_routes.route('/organizations/<int:organization_id>', methods=['GET'])
def get_organization_by_id_endpoint(organization_id):
    return get_by_id(organization_id)


@organization_routes.route('/organizations/<int:organization_id>', methods=['PUT'])
def update_organization_by_id_endpoint(organization_id):
    return update(organization_id)


@organization_routes.route('/organizations/<int:organization_id>', methods=['DELETE'])
def delete_organization_endpoint(organization_id):
    return delete(organization_id)
