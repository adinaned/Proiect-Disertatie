from flask import jsonify, request
from services import (create_vote, get_all_votes, get_vote_by_token)


def create():
    try:
        data = request.get_json()
        new_vote = create_vote(data)
        return jsonify(new_vote), 201
    except ValueError as ve:
        return jsonify({"message": str(ve)}), 400
    except Exception as e:
        return jsonify({"message": str(e)}), 500


def get_by_id(vote_token):
    vote = get_vote_by_token(vote_token)
    if vote:
        return jsonify(vote), 200
    return jsonify({"message": "Vote not found"}), 404


def get_all():
    votes = get_all_votes()
    if not votes:
        return jsonify([]), 200
    return jsonify(votes), 200
