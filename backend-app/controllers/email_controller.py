from flask import jsonify, request
from services import (create_email, get_email_by_id, get_email_by_name, update_email, delete_email)


def create():
    try:
        data = request.get_json()
        new_email = create_email(data)
        return jsonify(new_email), 201
    except ValueError as ve:
        return jsonify({"message": str(ve)}), 400
    except Exception as e:
        return jsonify({"message": str(e)}), 500


def get_by_id(email_id):
    email = get_email_by_id(email_id)
    if email:
        return jsonify(email), 200
    return jsonify({"message": "Email not found"}), 404


def get_by_name(email_address):
    email = get_email_by_name(email_address)
    if email:
        return jsonify(email), 200
    return jsonify({"message": "Email not found"}), 404


def update(email_id):
    try:
        data = request.get_json()
        updated_email = update_email(email_id, data)
        return jsonify(updated_email), 200
    except ValueError as ve:
        return jsonify({"message": str(ve)}), 400
    except Exception as e:
        return jsonify({"message": str(e)}), 500


def delete(email_id):
    try:
        result = delete_email(email_id)
        if result.get("message") == "Email not found":
            return jsonify(result), 404
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 500
