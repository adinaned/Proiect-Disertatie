from flask import jsonify, request
from services import (create_vote_submission, get_all_vote_submissions, get_vote_submission_by_id)


def create():
    try:
        data = request.get_json()
        new_vote_submission = create_vote_submission(data)
        return jsonify(new_vote_submission), 201
    except ValueError as ve:
        return jsonify({"message": str(ve)}), 400
    except Exception as e:
        return jsonify({"message": str(e)}), 500


def get_by_id(vote_submission_id):
    vote_submission = get_vote_submission_by_id(vote_submission_id)
    if vote_submission:
        return jsonify(vote_submission), 200
    return jsonify({"message": "VoteSubmission not found"}), 404


def get_all():
    vote_submissions = get_all_vote_submissions()
    if not vote_submissions:
        return jsonify([]), 200
    return jsonify(vote_submissions), 200
