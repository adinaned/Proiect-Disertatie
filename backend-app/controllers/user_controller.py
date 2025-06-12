from flask import jsonify, request
from services import (
    create_user,
    get_all_users_by_organization_id,
    get_user_by_id,
    update_user,
    delete_user
)
import uuid
from datetime import datetime

REQUIRED_FIELDS = {
    "first_name", "last_name", "date_of_birth", "country_id",
    "city", "address", "national_id", "organization_id"
}


def is_valid_uuid(value):
    try:
        uuid.UUID(str(value))
        return True
    except ValueError:
        return False


def create():
    try:
        data = request.get_json()
        if not isinstance(data, dict):
            raise ValueError("Payload must be a JSON object.")

        if "id" in data:
            raise ValueError("You cannot manually set the 'id' field.")

        missing = REQUIRED_FIELDS - data.keys()
        if missing:
            raise ValueError(f"Missing required field(s): {', '.join(missing)}")

        if not isinstance(data["national_id"], int) or data["national_id"] <= 0:
            raise ValueError("The 'national_id' must be a positive integer.")

        if not is_valid_uuid(data["organization_id"]):
            raise ValueError("The 'organization_id' must be a valid UUID.")

        try:
            datetime.fromisoformat(data["date_of_birth"])
        except Exception:
            raise ValueError("Invalid datetime format. Use ISO 8601 for 'date_of_birth'.")

        new_user = create_user(data)
        return jsonify({
            "message": "User created successfully.",
            "data": new_user
        }), 201
    except ValueError as ve:
        return jsonify({"message": str(ve)}), 400
    except Exception as e:
        return jsonify({"message": str(e)}), 500


def get_by_id(user_id):
    try:
        user = get_user_by_id(user_id)
        if user:
            return jsonify({
                "message": "User retrieved successfully.",
                "data": user
            }), 200
        return jsonify({"message": "User not found."}), 404
    except Exception as e:
        return jsonify({"message": str(e)}), 500


def get_all_by_organization_id(organization_id):
    try:
        users = get_all_users_by_organization_id(organization_id)
        return jsonify({
            "message": "Users retrieved successfully." if users else "No users found.",
            "data": users
        }), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 500


def update(user_id):
    try:
        data = request.get_json()
        if "id" in data:
            return jsonify({"message": "You cannot modify the 'id' field."}), 400
        if "created_at" in data:
            return jsonify({"message": "You cannot modify the 'created_at' field."}), 400
        if "date_of_birth" in data:
            return jsonify({"message": "You cannot modify the 'date_of_birth' field."}), 400
        if "profile_status_id" in data:
            return jsonify({"message": "You cannot modify the 'profile_status_id' field."}), 400
        updated_user = update_user(user_id, data)
        return jsonify({
            "message": "User updated successfully.",
            "data": updated_user
        }), 200
    except ValueError as ve:
        return jsonify({"message": str(ve)}), 400
    except Exception as e:
        return jsonify({"message": str(e)}), 500


def delete(user_id):
    try:
        result = delete_user(user_id)
        if result.get("message") == "User not found":
            return jsonify(result), 404
        return jsonify({
            "message": result["message"],
            "data": result.get("data")
        }), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 500
