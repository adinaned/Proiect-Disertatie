import unittest
from models import Question, db
from services.question_service import (
    create_question,
    get_question_by_id,
    get_all_questions,
    update_question,
    delete_question
)
from configs.database import Config
from flask import Flask

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)


class TestQuestionService(unittest.TestCase):

    def setUp(self):
        self.app = app
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.session = db.session

        Question.metadata.create_all(db.engine)

    def tearDown(self):
        self.session.query(Question).delete()
        self.session.commit()

        Question.metadata.drop_all(db.engine)

        self.app_context.pop()

    def test_create_question(self):
        data = {
            "name": "Test Question",
            "voting_session_id": 1
        }
        question_data = create_question(data)

        question = self.session.query(Question).filter_by(id=question_data["id"]).first()
        self.assertIsNotNone(question)
        self.assertEqual(question.name, "Test Question")
        self.assertEqual(question.voting_session_id, 1)

    def test_create_question_invalid_name(self):
        data = {
            "name": "",
            "voting_session_id": 1
        }
        with self.assertRaises(ValueError) as context:
            create_question(data)
        self.assertEqual(str(context.exception), "The 'name' field is required and must be a non-empty string")

    def test_get_question_by_id(self):
        question = Question(name="Test Question", voting_session_id=1)
        self.session.add(question)
        self.session.commit()

        question_data = get_question_by_id(question.id)
        self.assertIsNotNone(question_data)
        self.assertEqual(question_data["name"], "Test Question")

    def test_get_question_by_id_not_found(self):
        question_data = get_question_by_id(999)
        self.assertIsNone(question_data)

    def test_get_all_questions(self):
        question1 = Question(name="Question 1", voting_session_id=1)
        question2 = Question(name="Question 2", voting_session_id=1)
        self.session.add_all([question1, question2])
        self.session.commit()

        questions = get_all_questions()
        self.assertEqual(len(questions), 2)

    def test_update_question(self):
        question = Question(name="Old Question", voting_session_id=1)
        self.session.add(question)
        self.session.commit()

        data = {"name": "Updated Question"}
        updated_question = update_question(question.id, data)

        self.assertEqual(updated_question["name"], "Updated Question")

    def test_update_question_invalid_name(self):
        question = Question(name="Old Question", voting_session_id=1)
        self.session.add(question)
        self.session.commit()

        data = {"name": ""}
        with self.assertRaises(ValueError) as context:
            update_question(question.id, data)
        self.assertEqual(str(context.exception), "The 'name' field must be a non-empty string")

    def test_delete_question(self):
        question = Question(name="Question to Delete", voting_session_id=1)
        self.session.add(question)
        self.session.commit()

        response = delete_question(question.id)
        self.assertEqual(response["message"], "Question deleted successfully")

        deleted_question = self.session.query(Question).filter_by(id=question.id).first()
        self.assertIsNone(deleted_question)

    def test_delete_question_not_found(self):
        response = delete_question(999)
        self.assertEqual(response["message"], "Question not found")


if __name__ == "__main__":
    unittest.main()
