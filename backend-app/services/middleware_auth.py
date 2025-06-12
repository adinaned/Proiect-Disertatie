from functools import wraps
from flask import request, jsonify, current_app
import jwt


def jwt_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.cookies.get("token")
        if not token:
            return jsonify({"message": "Authentication token is missing."}), 401

        try:
            payload = jwt.decode(token, current_app.config["SECRET_KEY"], algorithms=["HS256"])
            request.user_id = payload["user_id"]
        except jwt.ExpiredSignatureError:
            return jsonify({"message": "Token has expired."}), 401
        except jwt.InvalidTokenError:
            return jsonify({"message": "Invalid token."}), 401

        return f(*args, **kwargs)

    return decorated
