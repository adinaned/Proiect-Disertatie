from flask import jsonify, request
from services import (
    login,
    get_current_user_service
)


def login_user():
    try:
        data = request.get_json()
        if not isinstance(data, dict):
            return jsonify({"message": "Payload must be a JSON object."}), 400

        email = data.get("email_address")
        password = data.get("password")

        if not email or not isinstance(email, str):
            return jsonify({"message": "The 'email_address' field is required."}), 400
        if not password or not isinstance(password, str):
            return jsonify({"message": "The 'password' field is required."}), 400

        result = login(email, password)

        if hasattr(result, "status_code"):
            return result

        return jsonify(result), 401 if "Invalid" in result["message"] else 400
    except Exception as e:
        return jsonify({"message": str(e)}), 500


def get_current_user():
    return get_current_user_service()
