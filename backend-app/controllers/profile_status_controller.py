from flask import jsonify, request
from services import (
    get_profile_status_by_user_id,
    update_profile_status_by_user_id,
)


def get_by_user_id(user_id):
    result = get_profile_status_by_user_id(user_id)

    if "data" in result:
        return jsonify(result), 200
    if f"User with ID {user_id} does not exist." in result.get("message", ""):
        return jsonify(result), 404
    if "Failed to find profile status for the specified user." in result.get("message", ""):
        return jsonify(result), 404

    return jsonify(result), 400


def update_by_user_id(user_id):
    try:
        data = request.get_json()

        if not isinstance(data, dict):
            return jsonify({"message": "Payload must be a JSON object."}), 400

        name = data.get("name")
        if not name or not isinstance(name, str) or not name.strip():
            return jsonify({"message": "The 'name' field is required and must be a non-empty string."}), 400

        result = update_profile_status_by_user_id(user_id, data)

        if "data" in result:
            return jsonify(result), 200
        if "does not exist" in result.get("message", ""):
            return jsonify(result), 404
        if "not found" in result.get("message", ""):
            return jsonify(result), 404

        return jsonify(result), 400
    except ValueError as ve:
        return jsonify({"message": str(ve)}), 400
    except Exception as e:
        return jsonify({"message": str(e)}), 500
