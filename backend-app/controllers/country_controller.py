from flask import jsonify, request
from services import (
    create_country,
    get_all_countries,
    get_country_by_id,
    get_country_by_name
)


def create():
    try:
        data = request.get_json()
        new_country = create_country(data)
        return jsonify(new_country), 201
    except ValueError as ve:
        return jsonify({"message": str(ve)}), 400
    except Exception as e:
        return jsonify({"message": str(e)}), 500


def get_by_id_or_name(country):
    try:
        if str(country).isdigit():
            country_data = get_country_by_id(int(country))
        else:
            country_data = get_country_by_name(country)

        if not country_data:
            return jsonify({"message": "Country not found"}), 404

        return jsonify({
            "message": "Country retrieved successfully.",
            "data": country_data
        }), 200

    except ValueError as ve:
        return jsonify({"message": str(ve)}), 400
    except Exception as e:
        return jsonify({"message": "Internal server error", "details": str(e)}), 500


def get_all():
    try:
        countries = get_all_countries()
        if not countries:
            return jsonify({
                "message": "No countries stored.",
                "data": []
            }), 200
        return jsonify({
            "message": "Countries retrieved successfully.",
            "data": countries
        }), 200
    except ValueError as ve:
        return jsonify({"message": str(ve)}), 400
    except Exception as e:
        return jsonify({"message": str(e)}), 500
