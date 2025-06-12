from datetime import datetime, timezone
import uuid
import traceback

from models import User, db, Country, Role, Organization
from schemas.user_schema import UserResponse


def create_user(data):
    from services import create_email, create_password, create_profile_status

    organization_id = data["organization_id"]
    country_id = data["country_id"]
    national_id = data["national_id"]

    if not db.session.get(Organization, organization_id):
        raise ValueError(f"Organization with ID '{organization_id}' does not exist.")
    if not db.session.get(Country, country_id):
        raise ValueError(f"Country with ID '{country_id}' does not exist.")
    if User.query.filter_by(national_id=national_id).first():
        raise ValueError(f"A user with national_id {national_id} already exists.")

    try:
        date_of_birth = datetime.fromisoformat(data["date_of_birth"])
    except Exception:
        raise ValueError("Invalid datetime format for 'date_of_birth'. Use ISO 8601 (e.g. 'YYYY-MM-DDTHH:MM:SS').")

    try:
        created_at = datetime.now(timezone.utc)
    except Exception:
        raise ValueError("Invalid datetime format for 'created_at'. Use ISO 8601 (e.g. 'YYYY-MM-DDTHH:MM:SS').")

    user = User(
        first_name=data["first_name"].strip(),
        last_name=data["last_name"].strip(),
        date_of_birth=date_of_birth,
        country_id=country_id,
        city=data["city"].strip(),
        address=data["address"].strip(),
        national_id=national_id,
        organization_id=organization_id.strip(),
        created_at=created_at
    )

    db.session.add(user)

    try:
        db.session.flush()

        profile_status = create_profile_status({
            "user_id": user.id,
            "name": "PENDING",
            "updated_at": created_at
        })
        db.session.add(profile_status)

        email = create_email({
            "user_id": user.id,
            "email_address": data["email_address"]
        })

        if isinstance(email, dict) and "message" in email:
            raise ValueError(email["message"])

        db.session.add(email)

        password = create_password({
            "user_id": user.id,
            "password": data["password"]
        })
        db.session.add(password)

        db.session.commit()
    except Exception as e:
        traceback.print_exc()
        db.session.rollback()
        raise ValueError(f"Failed to create user: {str(e)}")

    return UserResponse.model_validate(user).model_dump()


def get_user_by_id(user_id):
    user = db.session.get(User, user_id)
    if not user:
        return None

    return UserResponse.model_validate(user).model_dump()


def get_all_users_by_organization_id(organization_id):
    users = User.query.filter_by(organization_id=organization_id).all()
    return [UserResponse.model_validate(user).model_dump() for user in users]


def update_user(user_id, data):
    if not isinstance(data, dict):
        raise ValueError("Payload must be a non-empty dictionary")

    if "id" in data:
        raise ValueError("You cannot modify the ID")
    if "date_of_birth" in data:
        raise ValueError("You cannot modify the 'date_of_birth' field")

    user = db.session.get(User, user_id)
    if not user:
        raise ValueError("User not found")

    if "first_name" in data:
        val = data["first_name"]
        if not isinstance(val, str) or not val.strip():
            raise ValueError("The 'first_name' must be a non-empty string")
        user.first_name = val.strip()

    if "last_name" in data:
        val = data["last_name"]
        if not isinstance(val, str) or not val.strip():
            raise ValueError("The 'last_name' must be a non-empty string")
        user.last_name = val.strip()

    if "city" in data:
        val = data["city"]
        if not isinstance(val, str):
            raise ValueError("The 'city' must be a string")
        user.city = val.strip()

    if "country_id" in data:
        country_id = data["country_id"]
        try:
            uuid.UUID(country_id)
        except ValueError:
            raise ValueError("The 'country_id' must be a valid UUID")
        if not db.session.get(Country, country_id):
            raise ValueError(f"Country with ID '{country_id}' does not exist.")
        user.country_id = country_id

    if "address" in data:
        val = data["address"]
        if not isinstance(val, str):
            raise ValueError("The 'address' must be a string")
        user.address = val.strip()

    if "organization_id" in data:
        org_id = data["organization_id"]
        try:
            uuid.UUID(org_id)
        except ValueError:
            raise ValueError("The 'organization_id' must be a valid UUID")
        if not db.session.get(Organization, org_id):
            raise ValueError(f"Organization with ID '{org_id}' does not exist.")
        user.organization_id = org_id

    if "role_id" in data:
        role_id = data["role_id"]
        try:
            uuid.UUID(role_id)
        except ValueError:
            raise ValueError("The 'role_id' must be a valid UUID")
        if not db.session.get(Role, role_id):
            raise ValueError(f"Role with ID '{role_id}' does not exist.")
        user.role_id = role_id

    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        raise ValueError(f"Failed to update user: {str(e)}")

    return UserResponse.model_validate(user).model_dump()


def delete_user(user_id):
    user = db.session.get(User, user_id)
    if not user:
        return {"message": "User not found"}

    db.session.delete(user)

    try:
        db.session.commit()
        return {"message": "User deleted successfully", "data": {"id": user_id}}
    except Exception as e:
        db.session.rollback()
        raise ValueError(f"Failed to delete user: {str(e)}")
