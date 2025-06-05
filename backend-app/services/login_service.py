import jwt

from models import Email, Password, User
from werkzeug.security import check_password_hash
from datetime import datetime, timedelta, timezone
from flask import current_app


def login(email, password):
    email_record = Email.query.filter_by(email_address=email).first()
    if not email_record:
        return ValueError("Invalid email or password"), 401

    password_record = Password.query.filter_by(user_id=email_record.user_id).first()
    if not password_record or not password_record.password == password:
        # if not password_record or not check_password_hash(password_record.password, plain_password):
        return ValueError("Invalid email or password"), 401

    payload = {
        'user_id': email_record.user_id,
        'exp': datetime.now(timezone.utc) + timedelta(hours=2)
    }

    token = jwt.encode(payload, current_app.config['SECRET_KEY'], algorithm='HS256')
    user = User.query.get(email_record.user_id)

    return {
        'token': token,
        'user': {
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': email_record.email_address
        }
    }