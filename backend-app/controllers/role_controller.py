from flask import jsonify, request
from services import (
    create_role,
    get_all_roles,
    get_all_roles_by_organization_id,
    get_role_by_id,
    update_role,
    delete_role
)


def create():
    try:
        data = request.get_json()

        if not isinstance(data, dict):
            return jsonify({"message": "Invalid payload. JSON object required."}), 400

        if "id" in data:
            return jsonify({"message": "You are not allowed to manually set the role ID."}), 400
        if "name" not in data or not isinstance(data.get("name"), str) or not data.get("name").strip():
            return jsonify({"message": "The 'name' field is required and must be a non-empty string."}), 400
        if "organization_id" not in data or not isinstance(data.get("organization_id"), int):
            return jsonify({"message": "The 'organization_id' field is required and must be an integer."}), 400

        new_role = create_role(data)
        return jsonify({
            "message": "Role created successfully.",
            "data": new_role
        }), 201
    except ValueError as ve:
        return jsonify({"message": str(ve)}), 400
    except Exception as e:
        return jsonify({"message": str(e)}), 500


def get_by_id(role_id):
    try:
        role = get_role_by_id(role_id)
        if not role:
            return jsonify({"message": "Role not found"}), 404
        return jsonify({
            "message": "Role retrieved successfully.",
            "data": role
        }), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 500


def get_all():
    try:
        roles = get_all_roles()
        if not roles:
            return jsonify({
                "message": "No roles stored.",
                "data": []
            }), 200
        return jsonify({
            "message": "Roles retrieved successfully.",
            "data": roles
        }), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 500


def get_by_organization_id(organization_id):
    try:
        roles = get_all_roles_by_organization_id(organization_id)
        if not roles:
            return jsonify({
                "message": "No roles stored.",
                "data": []
            }), 200
        return jsonify({
            "message": "Roles retrieved successfully.",
            "data": roles
        }), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 500


def update(role_id):
    try:
        data = request.get_json()

        if not isinstance(data, dict):
            return jsonify({"message": "Invalid payload. JSON object required."}), 400
        if "id" in data:
            return jsonify({"message": "You are not allowed to modify the role ID."}), 400
        if "organization_id" in data:
            return jsonify({"message": "You are not allowed to modify the organization ID."}), 400

        updated_role = update_role(role_id, data)
        return jsonify({
            "message": "Role updated successfully.",
            "data": updated_role
        }), 200
    except ValueError as ve:
        return jsonify({"message": str(ve)}), 400
    except Exception as e:
        return jsonify({"message": str(e)}), 500


def delete(role_id):
    try:
        result = delete_role(role_id)
        if result.get("message") == "Role not found":
            return jsonify(result), 404
        return jsonify({
            "message": result.get("message", "Role deleted successfully."),
            "data": result.get("data", {"id": role_id})
        }), 200
    except ValueError as ve:
        return jsonify({"message": str(ve)}), 400
    except Exception as e:
        return jsonify({"message": str(e)}), 500
