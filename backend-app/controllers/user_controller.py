from flask import jsonify, request
from services import (create_user, get_all_users, get_user_by_id, update_user, delete_user)


def create():
    try:
        data = request.get_json()
        new_user = create_user(data)
        return jsonify(new_user), 201
    except ValueError as ve:
        return jsonify({"message": str(ve)}), 400
    except Exception as e:
        return jsonify({"message": str(e)}), 500


def get_by_id(user_id):
    user = get_user_by_id(user_id)
    if user:
        return jsonify(user), 200
    return jsonify({"message": "User not found"}), 404


def get_all():
    users = get_all_users()
    if not users:
        return jsonify([]), 200
    return jsonify(users), 200


def update(user_id):
    try:
        data = request.get_json()
        updated_user = update_user(user_id, data)
        return jsonify(updated_user), 200
    except ValueError as ve:
        return jsonify({"message": str(ve)}), 400
    except Exception as e:
        return jsonify({"message": str(e)}), 500


def delete(user_id):
    try:
        result = delete_user(user_id)
        if result.get("message") == "User not found":
            return jsonify(result), 404
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 500
