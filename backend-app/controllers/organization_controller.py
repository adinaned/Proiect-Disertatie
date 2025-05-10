from flask import jsonify, request
from services import (create_organisation, get_all_organisations, get_organisation_by_id, update_organisation, delete_organisation)


def create():
    try:
        data = request.get_json()
        new_organisation = create_organisation(data)
        return jsonify(new_organisation), 201
    except ValueError as ve:
        return jsonify({"message": str(ve)}), 400
    except Exception as e:
        return jsonify({"message": str(e)}), 500


def get_by_id(organisation_id):
    organization = get_organisation_by_id(organisation_id)
    if organization:
        return jsonify(organization), 200
    return jsonify({"message": "Organization not found"}), 404


def get_all():
    organisations = get_all_organisations()
    if not organisations:
        return jsonify([]), 200
    return jsonify(organisations), 200


def update(organisation_id):
    try:
        data = request.get_json()
        updated_organisation = update_organisation(organisation_id, data)
        return jsonify(updated_organisation), 200
    except ValueError as ve:
        return jsonify({"message": str(ve)}), 400
    except Exception as e:
        return jsonify({"message": str(e)}), 500


def delete(organisation_id):
    try:
        result = delete_organisation(organisation_id)
        if result.get("message") == "Organization not found":
            return jsonify(result), 404
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 500
