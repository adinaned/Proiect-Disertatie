from flask import jsonify, request
from services import (create_organization, get_all_organizations, get_organization_by_id, update_organization, delete_organization)
import traceback

def create():
    try:
        data = request.get_json()
        traceback.print_exc()
        new_organization = create_organization(data)
        return jsonify(new_organization), 201
    except ValueError as ve:
        return jsonify({"message": str(ve)}), 400
    except Exception as e:
        return jsonify({"message": str(e)}), 500


def get_by_id(organization_id):
    organization = get_organization_by_id(organization_id)
    if organization:
        return jsonify(organization), 200
    return jsonify({"message": "Organization not found"}), 404


def get_all():
    organizations = get_all_organizations()
    if not organizations:
        return jsonify([]), 200
    return jsonify(organizations), 200


def update(organization_id):
    try:
        data = request.get_json()
        updated_organization = update_organization(organization_id, data)
        return jsonify(updated_organization), 200
    except ValueError as ve:
        return jsonify({"message": str(ve)}), 400
    except Exception as e:
        return jsonify({"message": str(e)}), 500


def delete(organization_id):
    try:
        result = delete_organization(organization_id)
        if result.get("message") == "Organization not found":
            return jsonify(result), 404
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 500
