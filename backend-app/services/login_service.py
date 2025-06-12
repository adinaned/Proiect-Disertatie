from datetime import datetime, timedelta, timezone
from flask import current_app, make_response, jsonify, request
from werkzeug.security import check_password_hash
import jwt

from models import Email, Password, User

JWT_ALGORITHM = "HS256"
JWT_EXP_DELTA_SECONDS = 3600


def login(email_address, password):
    jwt_secret_key = current_app.config['SECRET_KEY']

    if not email_address or not isinstance(email_address, str):
        return {"message": "The 'email_address' field is required."}

    if not password or not isinstance(password, str):
        return {"message": "The 'password' field is required."}

    email = Email.query.filter_by(email_address=email_address.strip()).first()
    if not email or not email.user:
        return {"message": "Invalid email or password."}

    user = email.user

    password_record = Password.query.filter_by(user_id=user.id).first()
    if not password_record:
        return {"message": "Password not set for this user."}

    # if not check_password_hash(password_record.password, password):
    if password_record.password != password:
        return {"message": "Invalid email or password."}

    payload = {
        "user_id": user.id,
        "exp": datetime.now(timezone.utc) + timedelta(seconds=JWT_EXP_DELTA_SECONDS)
    }
    token = jwt.encode(payload, jwt_secret_key, algorithm=JWT_ALGORITHM)

    response = make_response(jsonify({
        "message": "Login successful.",
        "data": {
            "user_id": user.id,
        }
    }))
    response.status_code = 200

    response.set_cookie(
        "token",
        token,
        httponly=True,
        secure=False,
        samesite="Lax",
        max_age=JWT_EXP_DELTA_SECONDS
    )
    return response


def get_current_user_service():
    user_id = getattr(request, "user_id", None)

    if not user_id:
        return jsonify({"message": "Unauthorized"}), 401

    user = User.query.get(user_id)
    if not user:
        return jsonify({"message": "User not found."}), 404

    return jsonify({
        "message": "User fetched successfully.",
        "data": {
            "user_id": user.id,
            "first_name": user.first_name
        }
    }), 200