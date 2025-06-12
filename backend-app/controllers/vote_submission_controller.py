from flask import jsonify, request
from services import (
    create_vote_submission,
    get_all_vote_submissions_by_session_id,
    get_vote_submission_by_id
)
import uuid


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
            raise ValueError("You cannot manually set the ID.")

        required_fields = {"user_id", "voting_session_id", "selected_option_ids"}
        missing = required_fields - data.keys()
        if missing:
            raise ValueError(f"Missing required field(s): {', '.join(missing)}")

        if not isinstance(data["user_id"], int) or data["user_id"] <= 0:
            raise ValueError("The 'user_id' must be a positive integer.")

        if not is_valid_uuid(data["voting_session_id"]):
            raise ValueError("The 'voting_session_id' must be a valid UUID.")

        if not isinstance(data["selected_option_ids"], list) or not data["selected_option_ids"]:
            raise ValueError("The 'selected_option_ids' must be a non-empty list.")

        for option_id in data["selected_option_ids"]:
            if not isinstance(option_id, int):
                raise ValueError("Each option ID must be an integer.")

        result = create_vote_submission(data)
        return jsonify({
            "message": "Vote submission created successfully.",
            "data": result
        }), 201

    except ValueError as ve:
        return jsonify({"message": str(ve)}), 400
    except Exception as e:
        return jsonify({"message": str(e)}), 500


def get_by_id(vote_submission_id):
    try:
        if not is_valid_uuid(vote_submission_id):
            return jsonify({"message": "Invalid vote submission ID format."}), 400

        result = get_vote_submission_by_id(vote_submission_id)
        if result:
            return jsonify(result), 200

        return jsonify({"message": "Vote submission not found."}), 404
    except Exception as e:
        return jsonify({"message": str(e)}), 500


def get_all_by_session_id(voting_session_id):
    try:
        if not is_valid_uuid(voting_session_id):
            return jsonify({"message": "Invalid voting session ID format."}), 400
        result = get_all_vote_submissions_by_session_id(voting_session_id)
        if result.get("message") == "Not allowed to view submission before the voting session has ended.":
            return jsonify({"message": result.get("message")}), 403
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 500
