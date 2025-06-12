from flask import jsonify, request
import uuid
import logging

from services import (
    create_organization,
    get_all_organizations,
    get_organization_by_id,
    get_organization_by_name,
    update_organization,
    delete_organization
)

REQUIRED_ORG_FIELDS = {"name"}
FORBIDDEN_ORG_FIELDS = {"id"}

logger = logging.getLogger(__name__)

def validate_create_organization_payload(data):
    if not isinstance(data, dict):
        raise ValueError("Payload must be a JSON object.")

    if FORBIDDEN_ORG_FIELDS & data.keys():
        raise ValueError("You cannot manually set the 'id' field.")

    missing = REQUIRED_ORG_FIELDS - data.keys()
    if missing:
        raise ValueError(f"Missing required field(s): {', '.join(missing)}")

    name = data["name"]
    if not isinstance(name, str) or not name.strip():
        raise ValueError("The 'name' must be a non-empty string.")
    if len(name) > 100:
        raise ValueError("The 'name' field must not exceed 100 characters.")

    return data


def validate_update_organization_payload(data):
    if not isinstance(data, dict):
        raise ValueError("Payload must be a JSON object.")

    if FORBIDDEN_ORG_FIELDS & data.keys():
        raise ValueError("You are not allowed to modify the 'id' field.")

    if "name" in data:
        name = data["name"]
        if not isinstance(name, str) or not name.strip():
            raise ValueError("The 'name' must be a non-empty string.")
        if len(name) > 100:
            raise ValueError("The 'name' field must not exceed 100 characters.")

    return data


def create():
    try:
        data = request.get_json()
        validated_data = validate_create_organization_payload(data)
        new_organization = create_organization(validated_data)
        return jsonify(new_organization), 201
    except ValueError as ve:
        return jsonify({"message": str(ve)}), 400
    except Exception as e:
        return jsonify({"message": str(e)}), 500


def get_by_name_or_id(organization_filter):
    try:
        try:
            uuid_val = uuid.UUID(str(organization_filter))
            organization = get_organization_by_id(uuid_val)
            lookup_type = "ID"
        except ValueError:
            organization = get_organization_by_name(organization_filter)
            lookup_type = "name"

        if not organization:
            logger.info(f"Organization not found with {lookup_type}: {organization_filter}")
            return jsonify({
                "message": f"Organization not found with {lookup_type.lower()}: {organization_filter}",
                "data": None
            }), 404

        logger.info(f"Organization retrieved successfully using {lookup_type}: {organization_filter}")
        return jsonify({
            "message": f"Organization retrieved successfully using {lookup_type}.",
            "data": organization
        }), 200

    except Exception as e:
        logger.error(f"Error retrieving organization by {organization_filter}: {str(e)}")
        return jsonify({
            "message": "An error occurred while retrieving the organization.",
            "error": str(e)
        }), 500


def get_all():
    try:
        organizations = get_all_organizations()
        if not organizations:
            return jsonify({
                "message": "No organizations stored.",
                "data": []
            }), 200
        return jsonify({
            "message": "Organizations retrieved successfully.",
            "data": organizations
        }), 200
    except ValueError as ve:
        return jsonify({"message": str(ve)}), 400
    except Exception as e:
        return jsonify({"message": str(e)}), 500


def update(organization_id):
    try:
        data = request.get_json()
        validated_data = validate_update_organization_payload(data)
        updated_organization = update_organization(organization_id, validated_data)
        return jsonify({
            "message": "Organization updated successfully.",
            "data": updated_organization
        }), 200
    except ValueError as ve:
        return jsonify({"message": str(ve)}), 400
    except Exception as e:
        return jsonify({"message": str(e)}), 500


def delete(organization_id):
    try:
        result = delete_organization(organization_id)
        if result.get("message") == "Organization not found":
            return jsonify(result), 404
        return jsonify({
            "message": "Organization deleted successfully.",
            "data": result.get("data", {})
        }), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 500
