from models import Question, db
from schemas.question_schema import QuestionResponse


def create_question(data):
    if not isinstance(data, dict):
        raise ValueError("Payload must be a JSON object")

    if "id" in data:
        raise ValueError("You cannot manually set the ID")

    name = data.get("name")
    voting_session_id = data.get("voting_session_id")

    if not name or not isinstance(name, str):
        raise ValueError("The 'name' field is required and must be a non-empty string")
    if len(name) > 256:
        raise ValueError("The 'name' field must not exceed 256 characters")
    if not voting_session_id or not isinstance(voting_session_id, int):
        raise ValueError("The 'voting_session_id' field is required and must be an integer")

    question = Question(
        name=name.strip(),
        voting_session_id=voting_session_id
    )

    db.session.add(question)

    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        raise e

    return QuestionResponse.model_validate(question).model_dump()


def get_question_by_id(question_id):
    question = db.session.get(Question, question_id)
    if not question:
        return None

    return QuestionResponse.model_validate(question).model_dump()


def get_all_questions():
    questions = Question.query.all()
    if not questions:
        return []

    return [QuestionResponse.model_validate(question).model_dump() for question in questions]


def update_question(question_id, data):
    if not isinstance(data, dict):
        raise ValueError("Payload must be a non-empty dictionary")

    if "id" in data:
        raise ValueError("You cannot modify the ID")

    question = db.session.get(Question, question_id)
    if not question:
        raise ValueError("Question not found")

    if "name" in data:
        name = data["name"]
        if not isinstance(name, str) or not name.strip():
            raise ValueError("The 'name' field must be a non-empty string")
        if len(name) > 256:
            raise ValueError("The 'name' field must not exceed 256 characters")
        question.name = name.strip()

    if "voting_session_id" in data:
        voting_session_id = data["voting_session_id"]
        if not isinstance(voting_session_id, int):
            raise ValueError("The 'voting_session_id' field must be an integer")
        question.voting_session_id = voting_session_id

    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        raise e

    return QuestionResponse.model_validate(question).model_dump()


def delete_question(question_id):
    question = db.session.get(Question, question_id)
    if not question:
        return {"message": "Question not found"}

    db.session.delete(question)

    try:
        db.session.commit()
        return {"message": "Question deleted successfully"}
    except Exception as e:
        db.session.rollback()
        raise e
