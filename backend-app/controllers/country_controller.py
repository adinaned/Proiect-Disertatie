from flask import jsonify, request
from services import (create_country, get_all_countries, get_country_by_id, update_country, delete_country)


def create():
    try:
        data = request.get_json()
        new_country = create_country(data)
        return jsonify(new_country), 201
    except ValueError as ve:
        return jsonify({"message": str(ve)}), 400
    except Exception as e:
        return jsonify({"message": str(e)}), 500


def get_by_id(country_id):
    country = get_country_by_id(country_id)
    if country:
        return jsonify(country), 200
    return jsonify({"message": "Country not found"}), 404


def get_all():
    countries = get_all_countries()
    if not countries:
        return jsonify([]), 200
    return jsonify(countries), 200


def update(country_id):
    try:
        data = request.get_json()
        updated_country = update_country(country_id, data)
        return jsonify(updated_country), 200
    except ValueError as ve:
        return jsonify({"message": str(ve)}), 400
    except Exception as e:
        return jsonify({"message": str(e)}), 500


def delete(country_id):
    try:
        result = delete_country(country_id)
        if result.get("message") == "Country not found":
            return jsonify(result), 404
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 500
