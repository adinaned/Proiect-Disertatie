import unittest
from models import VoteSubmission, VotingSession, User, db
from services.vote_submission_service import (
    create_vote_submission,
    get_vote_submission_by_id,
    get_all_vote_submissions
)
from configs.database import Config
from flask import Flask

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)


class TestVoteSubmissionService(unittest.TestCase):

    def setUp(self):
        self.app = app
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.session = db.session

        VoteSubmission.metadata.create_all(db.engine)
        VotingSession.metadata.create_all(db.engine)
        User.metadata.create_all(db.engine)

        # Add test dependencies
        self.test_user = User(first_name="John", last_name="Doe")
        self.test_session = VotingSession(name="Test Session")
        self.session.add_all([self.test_user, self.test_session])
        self.session.commit()

    def tearDown(self):
        self.session.query(VoteSubmission).delete()
        self.session.query(VotingSession).delete()
        self.session.query(User).delete()
        self.session.commit()

        VoteSubmission.metadata.drop_all(db.engine)
        VotingSession.metadata.drop_all(db.engine)
        User.metadata.drop_all(db.engine)

        self.app_context.pop()

    def test_create_vote_submission(self):
        data = {
            "user_id": self.test_user.id,
            "voting_session_id": self.test_session.id
        }
        vote_submission_data = create_vote_submission(data)

        vote_submission = self.session.query(VoteSubmission).filter_by(id=vote_submission_data["id"]).first()
        self.assertIsNotNone(vote_submission)
        self.assertEqual(vote_submission.user_id, self.test_user.id)
        self.assertEqual(vote_submission.voting_session_id, self.test_session.id)
        self.assertFalse(vote_submission.has_voted)

    def test_create_vote_submission_invalid_user(self):
        data = {
            "user_id": 999,
            "voting_session_id": self.test_session.id
        }
        with self.assertRaises(ValueError) as context:
            create_vote_submission(data)
        self.assertEqual(str(context.exception), "The 'user_id' field is required and must be an integer")

    def test_create_vote_submission_invalid_session(self):
        data = {
            "user_id": self.test_user.id,
            "voting_session_id": 999
        }
        with self.assertRaises(ValueError) as context:
            create_vote_submission(data)
        self.assertEqual(str(context.exception), "Voting session with id 999 does not exist")

    def test_get_vote_submission_by_id(self):
        vote_submission = VoteSubmission(
            user_id=self.test_user.id,
            voting_session_id=self.test_session.id,
            has_voted=False
        )
        self.session.add(vote_submission)
        self.session.commit()

        vote_submission_data = get_vote_submission_by_id(vote_submission.id)
        self.assertIsNotNone(vote_submission_data)
        self.assertEqual(vote_submission_data["user_id"], self.test_user.id)

    def test_get_vote_submission_by_id_not_found(self):
        vote_submission_data = get_vote_submission_by_id(999)
        self.assertIsNone(vote_submission_data)

    def test_get_all_vote_submissions(self):
        vote_submission1 = VoteSubmission(user_id=self.test_user.id, voting_session_id=self.test_session.id, has_voted=False)
        vote_submission2 = VoteSubmission(user_id=self.test_user.id, voting_session_id=self.test_session.id, has_voted=True)
        self.session.add_all([vote_submission1, vote_submission2])
        self.session.commit()

        vote_submissions = get_all_vote_submissions()
        self.assertEqual(len(vote_submissions), 2)


if __name__ == "__main__":
    unittest.main()
