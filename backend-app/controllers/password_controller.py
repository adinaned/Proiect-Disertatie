from flask import jsonify, request
from services import (
    get_password_by_user_id,
    update_password
)


def get_by_user_id(user_id):
    try:
        password = get_password_by_user_id(user_id)
        return jsonify(password), 200
    except ValueError as ve:
        return jsonify({"message": str(ve)}), 400
    except Exception as e:
        return jsonify({"message": str(e)}), 500


def update(user_id):
    data = request.get_json()

    if not isinstance(data, dict) or not data:
        return jsonify({"message": "Payload must be a non-empty dictionary."}), 400

    if "id" in data:
        return jsonify({"message": "You cannot modify the ID."}), 400

    old_password = data.get("old_password")
    new_password = data.get("new_password")

    if not old_password or not new_password:
        return jsonify({"message": "Both old and new passwords are required."}), 400

    try:
        result = update_password(user_id, old_password, new_password)
        return jsonify(result), 200
    except ValueError as e:
        return jsonify({"message": str(e)}), 400
    except Exception as e:
        return jsonify({"message": "Internal server error", "details": str(e)}), 500
