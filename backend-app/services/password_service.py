from models import Password, db
from schemas.password_schema import PasswordResponse
from datetime import date

def create_password(data):
    if not isinstance(data, dict):
        raise ValueError("Payload must be a JSON object")

    if "id" in data:
        raise ValueError("You cannot manually set the ID")

    user_id = data.get("user_id")
    password_data = data.get("password")

    if not user_id or not isinstance(user_id, int):
        raise ValueError("The 'user_id' field is required and must be an integer")
    if not password_data or not isinstance(password_data, str):
        raise ValueError("The 'password' field is required and must be a non-empty string")
    if len(password_data) > 128:
        raise ValueError("The 'password' field must not exceed 128 characters")

    password = Password(
        user_id=user_id,
        password=password_data.strip(),
        updated_at=date.today()
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

    if "password" in data:
        password_data = data["password"]
        if not isinstance(password_data, str) or not password_data.strip():
            raise ValueError("The 'password' field must be a non-empty string")
        if len(password_data) > 128:
            raise ValueError("The 'password' field must not exceed 128 characters")
        password.password = password_data.strip()

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
