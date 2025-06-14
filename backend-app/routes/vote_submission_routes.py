from flask import Blueprint
from controllers.vote_submission_controller import *

vote_submission_routes = Blueprint("vote_submission_routes", __name__)


@vote_submission_routes.route('/vote_submission_submissions', methods=['POST'])
def create_new_vote_submission_endpoint():
    return create()


@vote_submission_routes.route('/vote_submission_submissions/voting_session/<string:voting_session_id>', methods=['GET'])
def get_vote_submission_submissions_endpoint(voting_session_id):
    return get_all_by_session_id(voting_session_id)


@vote_submission_routes.route('/vote_submission_submissions/<string:vote_submission_id>', methods=['GET'])
def get_vote_submission_by_id_endpoint(vote_submission_id):
    return get_by_id(vote_submission_id)
