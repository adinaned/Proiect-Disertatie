from flask import jsonify, request
from services import (create_voting_session, get_all_voting_sessions, get_voting_session_by_id, update_voting_session, delete_voting_session)


def create():
    try:
        data = request.get_json()
        new_voting_session = create_voting_session(data)
        return jsonify(new_voting_session), 201
    except ValueError as ve:
        return jsonify({"message": str(ve)}), 400
    except Exception as e:
        return jsonify({"message": str(e)}), 500


def get_by_id(voting_session_id):
    voting_session = get_voting_session_by_id(voting_session_id)
    if voting_session:
        return jsonify(voting_session), 200
    return jsonify({"message": "VotingSession not found"}), 404


def get_all():
    voting_sessions = get_all_voting_sessions()
    if not voting_sessions:
        return jsonify([]), 200
    return jsonify(voting_sessions), 200


def update(voting_session_id):
    try:
        data = request.get_json()
        updated_voting_session = update_voting_session(voting_session_id, data)
        return jsonify(updated_voting_session), 200
    except ValueError as ve:
        return jsonify({"message": str(ve)}), 400
    except Exception as e:
        return jsonify({"message": str(e)}), 500


def delete(voting_session_id):
    try:
        result = delete_voting_session(voting_session_id)
        if result.get("message") == "VotingSession not found":
            return jsonify(result), 404
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 500
