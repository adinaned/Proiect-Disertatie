import re
from datetime import date

from models import Email, User, db
from schemas.email_schema import EmailResponse

EMAIL_REGEX = re.compile(r"[^@]+@[^@]+\.[^@]+")


def create_email(data):
    if not isinstance(data, dict):
        return {"message": "Payload must be a JSON object."}

    if "id" in data or "is_verified" in data or "created_at" in data:
        return {"message": "You cannot manually set protected fields: id, is_verified, or created_at."}

    email_address = data.get("email_address")
    user_id = data.get("user_id")

    if not user_id or not isinstance(user_id, str) or not user_id.strip():
        return {"message": "The 'user_id' field is required and must be a non-empty string (UUID)."}

    if not email_address or not isinstance(email_address, str):
        return {"message": "The 'email_address' field is required and must be a non-empty string."}

    email_address = email_address.strip()

    if len(email_address) < 5 or len(email_address) > 320:
        return {"message": "The 'email_address' must be between 5 and 320 characters."}

    if not EMAIL_REGEX.match(email_address):
        return {"message": "Invalid email format."}

    user = db.session.get(User, user_id)
    if not user:
        return {"message": f"User with ID {user_id} does not exist."}

    existing_email = Email.query.filter_by(email_address=email_address).first()
    if existing_email:
        return {"message": "Email address is already in use."}

    email = Email(
        email_address=email_address,
        user_id=user_id,
        is_verified=False,
        created_at=date.today()
    )

    return email


def get_email_by_user_id(user_id):
    user = db.session.get(User, user_id)
    if not user:
        return {"message": f"User with ID {user_id} does not exist."}

    email = Email.query.filter_by(user_id=user_id).first()
    if not email:
        return {"message": "Email not found for the given user."}

    return {
        "message": "Email retrieved successfully.",
        "data": EmailResponse.model_validate(email).model_dump()
    }


def get_email_by_email_address(email_address):
    email = Email.query.filter_by(email_address=email_address).first()
    if not email:
        return {"message": f"Email address '{email_address}' does not exist."}

    return {
        "message": "Email retrieved successfully.",
        "data": EmailResponse.model_validate(email).model_dump()
    }
