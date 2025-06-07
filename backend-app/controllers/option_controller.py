from flask import jsonify, request
from services import (create_option, get_all_options, get_option_by_id, get_all_options_by_session_id, update_option,
                      delete_option, delete_options_by_session_id)


def create(session_id):
    try:
        data = request.get_json()
        new_option = create_option(data, session_id)
        return jsonify(new_option), 201
    except ValueError as ve:
        return jsonify({"message": str(ve)}), 400
    except Exception as e:
        return jsonify({"message": str(e)}), 500


def get_by_id(option_id):
    option = get_option_by_id(option_id)
    if option:
        return jsonify(option), 200
    return jsonify({"message": "Option not found"}), 404


def get_by_session_id(session_id):
    option = get_all_options_by_session_id(session_id)
    if option:
        return jsonify(option), 200
    return jsonify({"message": "Option not found"}), 404


def get_all():
    options = get_all_options()
    if not options:
        return jsonify([]), 200
    return jsonify(options), 200


def update(option_id):
    try:
        data = request.get_json()
        updated_option = update_option(option_id, data)
        return jsonify(updated_option), 200
    except ValueError as ve:
        return jsonify({"message": str(ve)}), 400
    except Exception as e:
        return jsonify({"message": str(e)}), 500


def delete(option_id):
    try:
        result = delete_option(option_id)
        if result.get("message") == "Option not found":
            return jsonify(result), 404
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 500


def delete_by_session_id(session_id):
    try:
        result = delete_options_by_session_id(session_id)
        if isinstance(result, dict) and result.get("message") == "Options not found":
            return jsonify(result), 404
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 500
