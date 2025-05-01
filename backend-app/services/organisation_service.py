from models import Organisation, db
from schemas.organisation_schema import OrganisationResponse


def create_organisation(data):
    if not isinstance(data, dict):
        raise ValueError("Payload must be a JSON object")

    if "id" in data:
        raise ValueError("You cannot manually set the ID")

    name = data.get("name")
    if not name or not isinstance(name, str):
        raise ValueError("The 'name' field is required and must be a non-empty string")
    if len(name) > 100:
        raise ValueError("The 'name' field must not exceed 100 characters")

    organisation = Organisation(name=name.strip())

    db.session.add(organisation)

    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        raise e

    return OrganisationResponse.model_validate(organisation).model_dump()


def get_organisation_by_id(organisation_id):
    organisation = db.session.get(Organisation, organisation_id)
    if not organisation:
        return None

    return OrganisationResponse.model_validate(organisation).model_dump()


def get_all_organisations():
    organisations = Organisation.query.all()
    if not organisations:
        return []

    return [OrganisationResponse.model_validate(org).model_dump() for org in organisations]


def update_organisation(organisation_id, data):
    if not isinstance(data, dict):
        raise ValueError("Payload must be a non-empty dictionary")

    if "id" in data:
        raise ValueError("You cannot modify the ID")

    organisation = db.session.get(Organisation, organisation_id)
    if not organisation:
        raise ValueError("Organisation not found")

    if "name" in data:
        name = data["name"]
        if not isinstance(name, str) or not name.strip():
            raise ValueError("The 'name' field must be a non-empty string")
        if len(name) > 100:
            raise ValueError("The 'name' field must not exceed 100 characters")
        organisation.name = name.strip()

    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        raise e

    return OrganisationResponse.model_validate(organisation).model_dump()


def delete_organisation(organisation_id):
    organisation = db.session.get(Organisation, organisation_id)
    if not organisation:
        return {"message": "Organisation not found"}

    db.session.delete(organisation)

    try:
        db.session.commit()
        return {"message": "Organisation deleted successfully"}
    except Exception as e:
        db.session.rollback()
        raise e
