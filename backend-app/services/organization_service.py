from flask import jsonify
import logging

from models import Organization, db, User
from schemas.organization_schema import OrganizationResponse

logger = logging.getLogger(__name__)


def validate_organization_name(name: str):
    if not name or not isinstance(name, str) or not name.strip():
        raise ValueError("The 'name' field is required and cannot be empty")
    if len(name) > 100:
        raise ValueError("The 'name' field must not exceed 100 characters")
    if len(name) < 5:
        raise ValueError("The 'name' field should have at least 5 characters")
    return name


def create_organization(data):
    if not isinstance(data, dict):
        raise ValueError("Payload must be a JSON object")

    if "id" in data:
        raise ValueError("You cannot manually set the ID")

    name = validate_organization_name(data.get("name", "").strip())
    if Organization.query.filter_by(name=name).first():
        raise ValueError("An organization with this name already exists.")

    organization = Organization(name=name)
    db.session.add(organization)

    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error creating organization: {e}")
        raise e

    return OrganizationResponse.model_validate(organization).model_dump()


def get_organization_by_id(organization_id):
    organization = db.session.get(Organization, organization_id)
    if not organization:
        return None
    return OrganizationResponse.model_validate(organization).model_dump()


def get_organization_by_name(organization_name):
    org = db.session.query(Organization).filter_by(name=organization_name).first()
    if not org:
        return None
    return OrganizationResponse.model_validate(org).model_dump()


def get_all_organizations():
    try:
        organizations = Organization.query.all()
        return [OrganizationResponse.model_validate(org).model_dump() for org in organizations]
    except Exception as e:
        logger.error(f"Error retrieving all organizations: {e}")
        raise e


def update_organization(organization_id, data):
    if not isinstance(data, dict):
        raise ValueError("Payload must be a non-empty dictionary")

    if "id" in data:
        raise ValueError("You cannot modify the ID")

    organization = db.session.get(Organization, organization_id)
    if not organization:
        raise ValueError("Organization not found")

    name = validate_organization_name(data.get("name", "").strip())
    if name != organization.name:
        if Organization.query.filter_by(name=name).first():
            raise ValueError("An organization with this name already exists.")

    organization.name = name

    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error updating organization {organization_id}: {e}")
        raise e

    return OrganizationResponse.model_validate(organization).model_dump()


def delete_organization(organization_id):
    organization = db.session.get(Organization, organization_id)
    if not organization:
        return {"message": "Organization not found"}

    if User.query.filter_by(organization_id=organization_id).first():
        raise ValueError("Cannot delete organization: it is assigned to one or more users.")

    num_roles = len(organization.roles)
    db.session.delete(organization)

    try:
        db.session.commit()
        return {
            "message": "Organization deleted successfully.",
            "data": {
                "id": organization_id,
                "roles_deleted": num_roles
            },
            "warning": f"{num_roles} role(s) associated with this organization were also deleted."
            if num_roles > 0 else None
        }
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error deleting organization {organization_id}: {e}")
        raise e
