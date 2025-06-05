from flask import jsonify, request
from services import (login)


def login_user():
    try:
        data = request.get_json()
        if not data:
            return jsonify({'message': 'Request body must be JSON'}), 400

        email_input = data.get('email')
        password_input = data.get('password')

        if not email_input or not password_input:
            return jsonify({'message': 'Email and password are required'}), 400

        login_data = login(email_input, password_input)
        return jsonify(login_data), 200

    except ValueError as ve:
        return jsonify({'message': str(ve)}), 401  # 401 = Unauthorized
    except Exception as e:
        return jsonify({'message': f'Internal server error: {e}'}), 500
