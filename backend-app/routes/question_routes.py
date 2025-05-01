from flask import Blueprint
from controllers.question_controller import *

question_routes = Blueprint("question_routes", __name__)


@question_routes.route('/questions', methods=['POST'])
def create_new_question_endpoint():
    return create()


@question_routes.route('/questions', methods=['GET'])
def get_questions_endpoint():
    return get_all()


@question_routes.route('/questions/<int:question_id>', methods=['GET'])
def get_question_by_id_endpoint(question_id):
    return get_by_id(question_id)


@question_routes.route('/questions/<int:question_id>', methods=['PUT'])
def update_question_by_id_endpoint(question_id):
    return update(question_id)


@question_routes.route('/questions/<int:question_id>', methods=['DELETE'])
def delete_question_endpoint(question_id):
    return delete(question_id)
