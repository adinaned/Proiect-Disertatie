from flask import jsonify, request
from services import (create_question, get_all_questions, get_question_by_id, update_question, delete_question)


def create():
    try:
        data = request.get_json()
        new_question = create_question(data)
        return jsonify(new_question), 201
    except ValueError as ve:
        return jsonify({"message": str(ve)}), 400
    except Exception as e:
        return jsonify({"message": str(e)}), 500


def get_by_id(question_id):
    question = get_question_by_id(question_id)
    if question:
        return jsonify(question), 200
    return jsonify({"message": "Question not found"}), 404


def get_all():
    questions = get_all_questions()
    if not questions:
        return jsonify([]), 200
    return jsonify(questions), 200


def update(question_id):
    try:
        data = request.get_json()
        updated_question = update_question(question_id, data)
        return jsonify(updated_question), 200
    except ValueError as ve:
        return jsonify({"message": str(ve)}), 400
    except Exception as e:
        return jsonify({"message": str(e)}), 500


def delete(question_id):
    try:
        result = delete_question(question_id)
        if result.get("message") == "Question not found":
            return jsonify(result), 404
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 500
