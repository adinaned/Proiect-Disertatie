from flask import jsonify, request
from services import (
    create_option,
    get_option_by_id,
    get_all_options_by_session_id,
    update_option,
    delete_option,
    delete_all_options_by_session_id
)

REQUIRED_OPTION_FIELDS = {"name", "voting_session_id"}
FORBIDDEN_CREATE_FIELDS = {"id"}
FORBIDDEN_UPDATE_FIELDS = {"voting_session_id"}


def validate_create_option_payload(data):
    if not isinstance(data, dict):
        raise ValueError("Payload must be a JSON object.")

    if FORBIDDEN_CREATE_FIELDS & data.keys():
        raise ValueError("You cannot manually set the 'id' field.")

    missing = REQUIRED_OPTION_FIELDS - data.keys()
    if missing:
        raise ValueError(f"Missing required field(s): {', '.join(missing)}")

    name = data["name"]
    if not isinstance(name, str) or not name.strip():
        raise ValueError("The 'name' must be a non-empty string.")
    if len(name) > 100:
        raise ValueError("The 'name' field must not exceed 100 characters.")

    voting_session_id = data["voting_session_id"]
    if not isinstance(voting_session_id, str) or not voting_session_id.strip():
        raise ValueError("The 'voting_session_id' must be a non-empty string.")

    return data


def validate_update_option_payload(data):
    if not isinstance(data, dict):
        raise ValueError("Payload must be a JSON object.")

    if FORBIDDEN_UPDATE_FIELDS & data.keys():
        raise ValueError("You are not allowed to modify the 'voting_session_id'.")

    if "name" in data:
        name = data["name"]
        if not isinstance(name, str) or not name.strip():
            raise ValueError("The 'name' must be a non-empty string.")
        if len(name) > 100:
            raise ValueError("The 'name' field must not exceed 100 characters.")

    return data


def create(voting_session_id):
    try:
        data = request.get_json()
        data["voting_session_id"] = voting_session_id
        validated_data = validate_create_option_payload(data)
        new_option = create_option(validated_data, voting_session_id)
        return jsonify(new_option), 201
    except ValueError as ve:
        return jsonify({"message": str(ve)}), 400
    except Exception as e:
        return jsonify({"message": str(e)}), 500


def get_by_id(option_id):
    option = get_option_by_id(option_id)
    if option:
        return jsonify(option), 200
    return jsonify({"message": "Option not found"}), 404


def get_by_session_id(voting_session_id):
    option = get_all_options_by_session_id(voting_session_id)
    if option:
        return jsonify(option), 200
    return jsonify({"message": "Option not found"}), 404


def update(option_id):
    try:
        data = request.get_json()
        validated_data = validate_update_option_payload(data)
        updated_option = update_option(option_id, validated_data)
        return jsonify(updated_option), 200
    except ValueError as ve:
        return jsonify({"message": str(ve)}), 400
    except Exception as e:
        return jsonify({"message": str(e)}), 500


def delete(option_id):
    try:
        result = delete_option(option_id)
        if result.get("message") == "Option not found":
            return jsonify(result), 404
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 500


def delete_by_session_id(voting_session_id):
    try:
        result = delete_all_options_by_session_id(voting_session_id)
        if isinstance(result, dict) and result.get("message") == "Options not found":
            return jsonify(result), 404
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 500
