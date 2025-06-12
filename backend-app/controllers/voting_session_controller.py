from flask import jsonify, request
import uuid

from services import (
    create_voting_session,
    get_all_voting_sessions_by_organization_id,
    get_all_voting_sessions_by_organization_id_and_role_id,
    get_voting_session_by_id,
    get_ring_by_voting_session,
    update_voting_session,
    delete_voting_session
)

REQUIRED_FIELDS = {"title", "question", "start_datetime", "end_datetime", "role_id", "organization_id"}


def validate_create_payload(data):
    if not isinstance(data, dict):
        raise ValueError("Payload must be a JSON object.")

    if "id" in data:
        raise ValueError("You cannot manually set the ID.")

    missing = REQUIRED_FIELDS - data.keys()
    if missing:
        raise ValueError(f"Missing required field(s): {', '.join(missing)}")

    title = data["title"]
    if not isinstance(title, str) or not title.strip():
        raise ValueError("The 'title' must be a non-empty string.")
    if len(title) > 50:
        raise ValueError("The 'title' field must not exceed 50 characters.")

    question = data["question"]
    if not isinstance(question, str) or not question.strip():
        raise ValueError("The 'question' must be a non-empty string.")
    if len(question) > 255:
        raise ValueError("The 'question' field must not exceed 255 characters.")

    for field in ["role_id", "organization_id"]:
        if not isinstance(data[field], str) or not data[field].strip():
            raise ValueError(f"The '{field}' must be a non-empty string.")

    return data


def create():
    try:
        data = request.get_json()
        validated_data = validate_create_payload(data)
        new_voting_session = create_voting_session(validated_data)
        return jsonify({
            "message": "Voting session created successfully.",
            "data": new_voting_session
        }), 201
    except ValueError as ve:
        return jsonify({"message": str(ve)}), 400
    except Exception as e:
        return jsonify({"message": str(e)}), 500


def is_valid_uuid(val):
    try:
        uuid.UUID(str(val))
        return True
    except ValueError:
        return False


def get_by_id(voting_session_id):
    try:
        if not is_valid_uuid(voting_session_id):
            return jsonify({"message": "Invalid voting session ID format."}), 400

        voting_session = get_voting_session_by_id(voting_session_id)
        if voting_session:
            return jsonify({
                "message": "Voting session retrieved successfully.",
                "data": voting_session
            }), 200

        return jsonify({"message": "Voting session not found."}), 404
    except Exception as e:
        return jsonify({"message": str(e)}), 500


def get_all_by_organization_id(organization_id):
    try:
        voting_sessions = get_all_voting_sessions_by_organization_id(organization_id)
        if not voting_sessions:
            return jsonify({
                "message": "No voting sessions found.",
                "data": []
            }), 200

        return jsonify({
            "message": "Voting sessions retrieved successfully.",
            "data": voting_sessions
        }), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 500


def get_all_by_organization_id_and_role_id(organization_id, role_id):
    try:
        voting_sessions = get_all_voting_sessions_by_organization_id_and_role_id(organization_id, role_id)
        if not voting_sessions:
            return jsonify({
                "message": "No voting sessions found.",
                "data": []
            }), 200

        return jsonify({
            "message": "Voting sessions retrieved successfully.",
            "data": voting_sessions
        }), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 500


def get_ring(voting_session_id):
    try:
        if not is_valid_uuid(voting_session_id):
            return jsonify({"message": "Invalid voting session ID format."}), 400

        voting_session = get_voting_session_by_id(voting_session_id)
        if not voting_session:
            return jsonify({"message": "Voting session not found."}), 404

        return jsonify({"data": get_ring_by_voting_session(voting_session)}), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 500


def validate_update_payload(data):
    if not isinstance(data, dict):
        raise ValueError("Payload must be a JSON object.")

    forbidden_fields = {"id", "organization_id", "role_id"}
    present_forbidden = forbidden_fields & data.keys()
    if present_forbidden:
        raise ValueError(f"You are not allowed to modify the following field(s): {', '.join(present_forbidden)}")

    if "title" in data:
        title = data["title"]
        if not isinstance(title, str) or not title.strip():
            raise ValueError("The 'title' must be a non-empty string.")
        if len(title) > 50:
            raise ValueError("The 'title' field must not exceed 50 characters.")

    if "question" in data:
        question = data["question"]
        if not isinstance(question, str) or not question.strip():
            raise ValueError("The 'question' must be a non-empty string.")
        if len(question) > 255:
            raise ValueError("The 'question' field must not exceed 255 characters.")

    return data


def update(voting_session_id):
    try:
        data = request.get_json()
        validated_data = validate_update_payload(data)
        updated_voting_session = update_voting_session(voting_session_id, validated_data)
        return jsonify({
            "message": "Voting session updated successfully.",
            "data": updated_voting_session
        }), 200
    except ValueError as ve:
        return jsonify({"message": str(ve)}), 400
    except Exception as e:
        return jsonify({"message": str(e)}), 500


def delete(voting_session_id):
    try:
        if not is_valid_uuid(voting_session_id):
            return jsonify({"message": "Invalid voting session ID format."}), 400

        result = delete_voting_session(voting_session_id)
        if result.get("message") == "Voting session not found":
            return jsonify(result), 404

        return jsonify(result), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 500
