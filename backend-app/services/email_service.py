import re
from datetime import date

from flask import jsonify

from models import Email, User, db
from schemas.email_schema import EmailResponse

EMAIL_REGEX = re.compile(r"[^@]+@[^@]+\.[^@]+")


def create_email(data):
    if not isinstance(data, dict):
        raise ValueError("Payload must be a JSON object")

    if "id" in data or "is_verified" in data or "created_at" in data:
        raise ValueError("You cannot manually set protected fields: id, is_verified, or created_at")

    email_address = data.get("email_address")
    user_id = data.get("user_id")

    existing_email = Email.query.filter_by(email_address=email_address).first()
    if existing_email:
        return jsonify({'error': 'Email already in use'}), 409

    if not email_address or not isinstance(email_address, str):
        raise ValueError("The 'email_address' field is required and must be a non-empty string")
    if len(email_address) > 320 or len(email_address) < 5:
        raise ValueError("The 'email_address' must be between 5 and 320 characters")
    if not EMAIL_REGEX.match(email_address):
        raise ValueError("Invalid email format")

    user = db.session.get(User, user_id)
    if not user:
        raise ValueError("User not found")

    email = Email(
        email_address=email_address.strip(),
        user_id=user_id,
        is_verified=False,
        created_at=date.today()
    )

    db.session.add(email)

    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        raise e

    return EmailResponse.model_validate(email).model_dump()


def get_email_by_id(email_id):
    email = db.session.get(Email, email_id)
    if not email:
        return None

    return EmailResponse.model_validate(email).model_dump()

def get_email_by_name(email_address):
    email = Email.query.filter_by(email_address=email_address).first()
    if not email:
        return None

    return EmailResponse.model_validate(email).model_dump()


def get_all_emails():
    emails = Email.query.all()
    if not emails:
        return []

    return [EmailResponse.model_validate(email).model_dump() for email in emails]


def update_email(email_id, data):
    if not isinstance(data, dict):
        raise ValueError("Payload must be a non-empty dictionary")

    if any(field in data for field in ["id", "is_verified", "created_at"]):
        raise ValueError("You cannot modify protected fields: id, is_verified, created_at")

    email = db.session.get(Email, email_id)
    if not email:
        raise ValueError("Email not found")

    if "email_address" in data:
        new_email = data["email_address"]
        if not isinstance(new_email, str) or not new_email.strip():
            raise ValueError("The 'email_address' field must be a non-empty string")
        if len(new_email) > 320 or len(new_email) < 5:
            raise ValueError("The 'email_address' must be between 5 and 320 characters")
        if not EMAIL_REGEX.match(new_email):
            raise ValueError("Invalid email format")
        email.email_address = new_email.strip()

    if "user_id" in data:
        new_user = db.session.get(User, data["user_id"])
        if not new_user:
            raise ValueError("User not found")
        email.user_id = data["user_id"]

    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        raise e

    return EmailResponse.model_validate(email).model_dump()


def delete_email(email_id):
    email = db.session.get(Email, email_id)
    if not email:
        return {"message": "Email not found"}

    db.session.delete(email)

    try:
        db.session.commit()
        return {"message": "Email deleted successfully"}
    except Exception as e:
        db.session.rollback()
        raise e
