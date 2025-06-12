from flask import jsonify
from services import (
    get_all_registrations_by_voting_session_id,
    get_registration_by_voting_session_id_and_user_id
)


def get_by_voting_session_id_and_user_id(voting_session_id, user_id):
    response, status = get_registration_by_voting_session_id_and_user_id(voting_session_id, user_id)
    return jsonify(response), status


def get_by_voting_session_id(voting_session_id):
    response, status = get_all_registrations_by_voting_session_id(voting_session_id)
    return jsonify(response), status
