from flask import jsonify
from services import (
    get_email_by_user_id,
    get_email_by_email_address
)


def get_by_user_id(user_id):
    email = get_email_by_user_id(user_id)
    if email:
        return jsonify(email), 200
    return jsonify({"message": "Email not found"}), 404


def get_by_email_address(email_address):
    response = get_email_by_email_address(email_address)
    if "data" in response:
        return jsonify(response), 200
    return jsonify(response), 404
