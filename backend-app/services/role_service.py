from models import Role, db
from schemas.role_schema import RoleResponse


def create_role(data):
    if not isinstance(data, dict):
        raise ValueError("Payload must be a JSON object")

    if "id" in data:
        raise ValueError("You cannot manually set the ID")

    name = data.get("name")
    organization_id = data.get("organization_id")

    if not name or not isinstance(name, str):
        raise ValueError("The 'name' field is required and must be a non-empty string")
    if len(name) > 100:
        raise ValueError("The 'name' field must not exceed 100 characters")
    if not organization_id or not isinstance(organization_id, int):
        raise ValueError("The 'organization_id' field is required and must be an integer")

    role = Role(name=name.strip(), organization_id=organization_id)

    db.session.add(role)

    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        raise e

    return RoleResponse.model_validate(role).model_dump()


def get_role_by_id(role_id):
    role = db.session.get(Role, role_id)
    if not role:
        return None

    return RoleResponse.model_validate(role).model_dump()


def get_all_roles():
    roles = Role.query.all()
    if not roles:
        return []

    return [RoleResponse.model_validate(role).model_dump() for role in roles]


def update_role(role_id, data):
    if not isinstance(data, dict):
        raise ValueError("Payload must be a non-empty dictionary")

    if "id" in data:
        raise ValueError("You cannot modify the ID")

    role = db.session.get(Role, role_id)
    if not role:
        raise ValueError("Role not found")

    if "name" in data:
        name = data["name"]
        if not isinstance(name, str) or not name.strip():
            raise ValueError("The 'name' field must be a non-empty string")
        if len(name) > 100:
            raise ValueError("The 'name' field must not exceed 100 characters")
        role.name = name.strip()

    if "organization_id" in data:
        organization_id = data["organization_id"]
        if not isinstance(organization_id, int):
            raise ValueError("The 'organization_id' field must be an integer")
        role.organization_id = organization_id

    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        raise e

    return RoleResponse.model_validate(role).model_dump()


def delete_role(role_id):
    role = db.session.get(Role, role_id)
    if not role:
        return {"message": "Role not found"}

    db.session.delete(role)

    try:
        db.session.commit()
        return {"message": "Role deleted successfully"}
    except Exception as e:
        db.session.rollback()
        raise e