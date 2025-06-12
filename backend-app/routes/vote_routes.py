from flask import Blueprint
from controllers.vote_controller import *

vote_routes = Blueprint("vote_routes", __name__)


@vote_routes.route('/votes', methods=['POST'])
def create_new_vote_endpoint():
    return create()


@vote_routes.route('/votes/voting_session/{string:voting_session_id}', methods=['GET'])
def get_votes_by_voting_session_id_endpoint(voting_session_id):
    return get_all_by_voting_session_id(voting_session_id)


@vote_routes.route('/votes/<string:vote_token>', methods=['GET'])
def get_vote_by_token_endpoint(vote_token):
    return get_vote_by_token(vote_token)
