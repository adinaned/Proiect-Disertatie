from models import User, db
from schemas.user_schema import UserResponse


def create_user(data):
    if not isinstance(data, dict):
        raise ValueError("Payload must be a JSON object")

    if "id" in data:
        raise ValueError("You cannot manually set the ID")

    first_name = data.get("first_name")
    last_name = data.get("last_name")
    date_of_birth = data.get("date_of_birth")
    country_id = data.get("country_id")
    city = data.get("city")
    address = data.get("address")
    national_id = data.get("national_id")
    role_id = data.get("role_id")
    organization_id = data.get("organization_id")
    created_at = data.get("created_at")

    if not first_name or not isinstance(first_name, str):
        raise ValueError("The 'first_name' field is required and must be a non-empty string")
    if not last_name or not isinstance(last_name, str):
        raise ValueError("The 'last_name' field is required and must be a non-empty string")

    user = User(
        first_name=first_name.strip(),
        last_name=last_name.strip(),
        date_of_birth=date_of_birth,
        country_id=country_id,
        city=city.strip() if city else None,
        address=address.strip() if address else None,
        national_id=national_id,
        role_id=role_id,
        organization_id=organization_id,
        created_at=created_at
    )

    db.session.add(user)

    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        raise e

    return UserResponse.model_validate(user).model_dump()


def get_user_by_id(user_id):
    user = db.session.get(User, user_id)
    if not user:
        return None

    return UserResponse.model_validate(user).model_dump()


def get_all_users():
    users = User.query.all()
    if not users:
        return []

    return [UserResponse.model_validate(user).model_dump() for user in users]


def update_user(user_id, data):
    if not isinstance(data, dict):
        raise ValueError("Payload must be a non-empty dictionary")

    if "id" in data:
        raise ValueError("You cannot modify the ID")

    user = db.session.get(User, user_id)
    if not user:
        raise ValueError("User not found")

    if "first_name" in data:
        first_name = data["first_name"]
        if not isinstance(first_name, str) or not first_name.strip():
            raise ValueError("The 'first_name' field must be a non-empty string")
        user.first_name = first_name.strip()

    if "last_name" in data:
        last_name = data["last_name"]
        if not isinstance(last_name, str) or not last_name.strip():
            raise ValueError("The 'last_name' field must be a non-empty string")
        user.last_name = last_name.strip()

    if "city" in data:
        user.city = data["city"].strip() if data["city"] else None

    if "address" in data:
        user.address = data["address"].strip() if data["address"] else None

    if "role_id" in data:
        user.role_id = data["role_id"]

    if "organization_id" in data:
        user.organization_id = data["organization_id"]

    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        raise e

    return UserResponse.model_validate(user).model_dump()


def delete_user(user_id):
    user = db.session.get(User, user_id)
    if not user:
        return {"message": "User not found"}

    db.session.delete(user)

    try:
        db.session.commit()
        return {"message": "User deleted successfully"}
    except Exception as e:
        db.session.rollback()
        raise e
