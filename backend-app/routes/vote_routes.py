from flask import Blueprint
from controllers.vote_controller import *

vote_routes = Blueprint("vote_routes", __name__)


@vote_routes.route('/votes', methods=['POST'])
def create_new_vote_endpoint():
    return create()


@vote_routes.route('/votes', methods=['GET'])
def get_votes_endpoint():
    return get_all()


@vote_routes.route('/votes/<int:vote_token>', methods=['GET'])
def get_vote_by_token_endpoint(vote_token):
    return get_vote_by_token(vote_token)
