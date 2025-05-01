from flask import jsonify, request
from services import (create_role, get_all_roles, get_role_by_id, update_role, delete_role)


def create():
    try:
        data = request.get_json()
        new_role = create_role(data)
        return jsonify(new_role), 201
    except ValueError as ve:
        return jsonify({"message": str(ve)}), 400
    except Exception as e:
        return jsonify({"message": str(e)}), 500


def get_by_id(role_id):
    role = get_role_by_id(role_id)
    if role:
        return jsonify(role), 200
    return jsonify({"message": "Role not found"}), 404


def get_all():
    roles = get_all_roles()
    if not roles:
        return jsonify([]), 200
    return jsonify(roles), 200


def update(role_id):
    try:
        data = request.get_json()
        updated_role = update_role(role_id, data)
        return jsonify(updated_role), 200
    except ValueError as ve:
        return jsonify({"message": str(ve)}), 400
    except Exception as e:
        return jsonify({"message": str(e)}), 500


def delete(role_id):
    try:
        result = delete_role(role_id)
        if result.get("message") == "Role not found":
            return jsonify(result), 404
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 500
