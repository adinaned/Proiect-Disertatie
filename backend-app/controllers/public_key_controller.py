from flask import jsonify, request
from services import create_public_key, get_public_key_by_session_id


def create():
    data = request.get_json()

    required_fields = ['voting_session_id', 'user_id', 'public_key_x', 'public_key_y']
    missing_fields = [field for field in required_fields if field not in data]

    if missing_fields:
        return jsonify({'error': f"Missing required fields: {', '.join(missing_fields)}"}), 400

    try:
        result = create_public_key(data)
        return jsonify({
            "message": "Public key successfully created.",
            "data": result
        }), 201
    # except PublicKeyAlreadyExists as e:
    #     return jsonify({'message': str(e)}), 409
    except Exception as e:
        print("Unexpected error:", str(e))
        return jsonify({'error': 'Internal server error', 'details': str(e)}), 500


def get_by_session_id(voting_session_id):
    try:
        result = get_public_key_by_session_id(voting_session_id)
        if result is None:
            return jsonify({'message': 'Public key not found'}), 404
        return jsonify(result), 200
    except Exception as e:
        return jsonify({'message': f'Internal server error: {str(e)}'}), 500
