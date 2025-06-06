from models import Organization, db
from schemas.organization_schema import OrganizationResponse


def create_organization(data):
    if not isinstance(data, dict):
        raise ValueError("Payload must be a JSON object")

    if "id" in data:
        raise ValueError("You cannot manually set the ID")

    name = data.get("name")
    if not name or not isinstance(name, str):
        raise ValueError("The 'name' field is required and must be a non-empty string")
    if len(name) > 100:
        raise ValueError("The 'name' field must not exceed 100 characters")

    organization = Organization(name=name.strip())

    db.session.add(organization)

    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        raise e

    return OrganizationResponse.model_validate(organization).model_dump()


def get_organization_by_id(organization_id):
    organization = db.session.get(Organization, organization_id)
    if not organization:
        return None

    return OrganizationResponse.model_validate(organization).model_dump()


def get_all_organizations():
    organizations = Organization.query.all()
    if not organizations:
        return []

    return [OrganizationResponse.model_validate(org).model_dump() for org in organizations]


def update_organization(organization_id, data):
    if not isinstance(data, dict):
        raise ValueError("Payload must be a non-empty dictionary")

    if "id" in data:
        raise ValueError("You cannot modify the ID")

    organization = db.session.get(Organization, organization_id)
    if not organization:
        raise ValueError("Organization not found")

    if "name" in data:
        name = data["name"]
        if not isinstance(name, str) or not name.strip():
            raise ValueError("The 'name' field must be a non-empty string")
        if len(name) > 100:
            raise ValueError("The 'name' field must not exceed 100 characters")
        organization.name = name.strip()

    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        raise e

    return OrganizationResponse.model_validate(organization).model_dump()


def delete_organization(organization_id):
    organization = db.session.get(Organization, organization_id)
    if not organization:
        return {"message": "Organization not found"}

    db.session.delete(organization)

    try:
        db.session.commit()
        return {"message": "Organization deleted successfully"}
    except Exception as e:
        db.session.rollback()
        raise e
