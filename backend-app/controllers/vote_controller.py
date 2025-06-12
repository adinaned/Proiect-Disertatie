from flask import jsonify, request
from services import (
    create_vote,
    get_all_votes_by_voting_session_id,
    get_vote_by_token
)
import traceback


def create():
    try:
        data = request.get_json()

        if not isinstance(data, dict):
            return jsonify({"message": "Payload must be a JSON object"}), 400

        forbidden_fields = {"id", "token", "submission_timestamp"}
        if any(field in data for field in forbidden_fields):
            return jsonify({"message": "Fields 'id', 'token', or 'submission_timestamp' cannot be manually set"}), 400

        required_fields = {"voting_session_id", "option_id", "key_image", "signature"}
        missing_fields = required_fields - data.keys()
        if missing_fields:
            return jsonify({"message": f"Missing required field(s): {', '.join(missing_fields)}"}), 400

        if not isinstance(data["voting_session_id"], str):
            return jsonify({"message": "'voting_session_id' must be a string (UUID)"}), 400

        if not isinstance(data["option_id"], str):
            return jsonify({"message": "'option_id' must be a string (UUID)"}), 400

        if not isinstance(data["key_image"], (str, dict)):
            return jsonify({"message": "'key_image' must be a string or JSON object"}), 400

        if not isinstance(data["signature"], (dict, str)):
            return jsonify({"message": "'signature' must be a string or JSON object"}), 400

        new_vote = create_vote(data)
        return jsonify(new_vote), 201

    except ValueError as ve:
        traceback.print_exc()
        error_message = str(ve)
        if "Voting session has already ended" in error_message:
            return jsonify({"message": error_message}), 403
        if "has already submitted a vote" in error_message:
            return jsonify({"message": error_message}), 400
        return jsonify({"message": error_message}), 400

    except Exception as e:
        traceback.print_exc()
        return jsonify({"message": str(e)}), 500


def get_by_id(vote_token):
    try:
        vote = get_vote_by_token(vote_token)
        if "message" in vote and "Associated voting session not found." in vote["message"]:
            return jsonify(vote), 403
        if "message" in vote and "Vote not found." in vote["message"]:
            return jsonify(vote), 404
        return jsonify(vote), 200
    except Exception as e:
        traceback.print_exc()
        return jsonify({"message": str(e)}), 500


def get_all_by_voting_session_id(voting_session_id):
    try:
        votes = get_all_votes_by_voting_session_id(voting_session_id)
        if "message" in votes and "Not allowed to view votes before the voting session has ended." in votes[
            "message"].lower():
            return jsonify(votes), 403
        if "message" in votes and "Voting session not found." in votes["message"].lower():
            return jsonify(votes), 404
        return jsonify(votes), 200
    except Exception as e:
        traceback.print_exc()
        return jsonify({"message": str(e)}), 500
