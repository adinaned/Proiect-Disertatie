from models import Password, db
from schemas.password_schema import PasswordResponse


def create_password(data):
    if not isinstance(data, dict):
        raise ValueError("Payload must be a JSON object")

    if "id" in data:
        raise ValueError("You cannot manually set the ID")

    user_id = data.get("user_id")
    hashed_password = data.get("hashed_password")
    updated_at = data.get("updated_at")

    if not user_id or not isinstance(user_id, int):
        raise ValueError("The 'user_id' field is required and must be an integer")
    if not hashed_password or not isinstance(hashed_password, str):
        raise ValueError("The 'hashed_password' field is required and must be a non-empty string")
    if len(hashed_password) > 128:
        raise ValueError("The 'hashed_password' field must not exceed 128 characters")

    password = Password(
        user_id=user_id,
        hashed_password=hashed_password.strip(),
        updated_at=updated_at
    )

    db.session.add(password)

    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        raise e

    return PasswordResponse.model_validate(password).model_dump()


def get_password_by_user_id(user_id):
    from models import User
    if not isinstance(user_id, int):
        raise ValueError("The 'user_id' must be an integer")

    user = db.session.get(User, user_id)
    if not user:
        raise ValueError(f"User with id {user_id} does not exist")

    password = Password.query.filter_by(user_id=user_id).first()
    if not password:
        raise ValueError("Password not provided")

    return PasswordResponse.model_validate(password).model_dump()


def update_password(password_id, data):
    if not isinstance(data, dict):
        raise ValueError("Payload must be a non-empty dictionary")

    if "id" in data:
        raise ValueError("You cannot modify the ID")

    password = db.session.get(Password, password_id)
    if not password:
        raise ValueError("Password not found")

    if "user_id" in data:
        user_id = data["user_id"]
        if not isinstance(user_id, int):
            raise ValueError("The 'user_id' field must be an integer")
        password.user_id = user_id

    if "hashed_password" in data:
        hashed_password = data["hashed_password"]
        if not isinstance(hashed_password, str) or not hashed_password.strip():
            raise ValueError("The 'hashed_password' field must be a non-empty string")
        if len(hashed_password) > 128:
            raise ValueError("The 'hashed_password' field must not exceed 128 characters")
        password.hashed_password = hashed_password.strip()

    if "updated_at" in data:
        password.updated_at = data["updated_at"]

    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        raise e

    return PasswordResponse.model_validate(password).model_dump()


def delete_password(password_id):
    password = db.session.get(Password, password_id)
    if not password:
        return {"message": "Password not found"}

    db.session.delete(password)

    try:
        db.session.commit()
        return {"message": "Password deleted successfully"}
    except Exception as e:
        db.session.rollback()
        raise e
