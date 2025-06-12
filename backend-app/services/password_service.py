from models import Password, db, User
from schemas.password_schema import PasswordResponse
from datetime import datetime, timezone
from pprint import pprint


def create_password(data):
    if not isinstance(data, dict):
        raise ValueError("Payload must be a JSON object.")

    if "id" in data:
        raise ValueError("You cannot manually set the ID.")

    user_id = data.get("user_id")
    password_data = data.get("password")

    if not user_id:
        raise ValueError("The 'user_id' field is required.")

    if not password_data or not isinstance(password_data, str) or not password_data.strip():
        raise ValueError("The 'password' field is required and must be a non-empty string.")

    if len(password_data) > 128:
        raise ValueError("The 'password' field must not exceed 128 characters.")

    user = db.session.get(User, user_id)
    if not user:
        raise ValueError(f"User with ID {user_id} does not exist.")

    password = Password(
        user_id=user_id,
        password=password_data.strip(),
        updated_at=datetime.now(timezone.utc)
    )
    return password



def get_password_by_user_id(user_id):
    user = db.session.get(User, user_id)
    if not user:
        return {"message": f"User with ID {user_id} does not exist."}

    password = Password.query.filter_by(user_id=user_id).first()
    if not password:
        return {"message": "Password not found for the given user."}

    return {
        "message": "Password retrieved successfully.",
        "data": PasswordResponse.model_validate(password).model_dump()
    }


def update_password(user_id, old_password, new_password):
    user = db.session.get(User, user_id)
    if not user:
        raise ValueError("User not found.")

    password_record = Password.query.filter_by(user_id=user_id).first()
    if not password_record:
        raise ValueError("Password record not found for the user.")

    # if not check_password_hash(password_record.hashed_password, old_password):
    if password_record.password != old_password:
        raise ValueError("Old password is incorrect.")

    print(new_password)
    password_record.password = new_password
    password_record.updated_at = datetime.now(timezone.utc)

    db.session.add(password_record)

    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        raise Exception(f"Failed to update password: {str(e)}")

    return {
        "message": "Password updated successfully.",
        "data": PasswordResponse.model_validate(password_record).model_dump()
    }
