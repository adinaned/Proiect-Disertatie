from flask import jsonify, request
from services import (create_profile_status, get_all_profile_statuses, get_profile_status_by_id, update_profile_status, delete_profile_status)


def create():
    try:
        data = request.get_json()
        new_profile_status = create_profile_status(data)
        return jsonify(new_profile_status), 201
    except ValueError as ve:
        return jsonify({"message": str(ve)}), 400
    except Exception as e:
        return jsonify({"message": str(e)}), 500


def get_by_id(profile_status_id):
    profile_status = get_profile_status_by_id(profile_status_id)
    if profile_status:
        return jsonify(profile_status), 200
    return jsonify({"message": "ProfileStatus not found"}), 404


def get_all():
    profile_statuses = get_all_profile_statuses()
    if not profile_statuses:
        return jsonify([]), 200
    return jsonify(profile_statuses), 200


def update(profile_status_id):
    try:
        data = request.get_json()
        updated_profile_status = update_profile_status(profile_status_id, data)
        return jsonify(updated_profile_status), 200
    except ValueError as ve:
        return jsonify({"message": str(ve)}), 400
    except Exception as e:
        return jsonify({"message": str(e)}), 500


def delete(profile_status_id):
    try:
        result = delete_profile_status(profile_status_id)
        if result.get("message") == "ProfileStatus not found":
            return jsonify(result), 404
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 500
