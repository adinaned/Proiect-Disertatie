from flask import jsonify, request
from services import (create_password, get_password_by_user_id, update_password, delete_password)


def create():
    try:
        data = request.get_json()
        new_password = create_password(data)
        return jsonify(new_password), 201
    except ValueError as ve:
        return jsonify({"message": str(ve)}), 400
    except Exception as e:
        return jsonify({"message": str(e)}), 500


def get_by_user_id(user_id):
    try:
        password = get_password_by_user_id(user_id)
        return jsonify(password), 200
    except ValueError as ve:
        return jsonify({"message": str(ve)}), 400
    except Exception as e:
        return jsonify({"message": str(e)}), 500


def update(password_id):
    try:
        data = request.get_json()
        updated_password = update_password(password_id, data)
        return jsonify(updated_password), 200
    except ValueError as ve:
        return jsonify({"message": str(ve)}), 400
    except Exception as e:
        return jsonify({"message": str(e)}), 500


def delete(password_id):
    try:
        result = delete_password(password_id)
        if result.get("message") == "Password not found":
            return jsonify(result), 404
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 500
