import unittest
from datetime import datetime
from models import Vote, Option, VotingSession, db
from services.vote_service import (
    create_vote,
    get_vote_by_token,
    get_all_votes
)
from configs.database import Config
from flask import Flask

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)


class TestVoteService(unittest.TestCase):

    def setUp(self):
        self.app = app
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.session = db.session

        Vote.metadata.create_all(db.engine)
        Option.metadata.create_all(db.engine)
        VotingSession.metadata.create_all(db.engine)

        # Add test dependencies
        self.test_session = VotingSession(name="Test Session")
        self.test_option = Option(name="Test Option")
        self.session.add_all([self.test_session, self.test_option])
        self.session.commit()

    def tearDown(self):
        self.session.query(Vote).delete()
        self.session.query(Option).delete()
        self.session.query(VotingSession).delete()
        self.session.commit()

        Vote.metadata.drop_all(db.engine)
        Option.metadata.drop_all(db.engine)
        VotingSession.metadata.drop_all(db.engine)

        self.app_context.pop()

    def test_create_vote(self):
        data = {
            "voting_session_id": self.test_session.id,
            "option_id": self.test_option.id
        }
        vote_data = create_vote(data)

        vote = self.session.query(Vote).filter_by(id=vote_data["id"]).first()
        self.assertIsNotNone(vote)
        self.assertEqual(vote.voting_session_id, self.test_session.id)
        self.assertEqual(vote.option_id, self.test_option.id)

    def test_create_vote_invalid_session(self):
        data = {
            "voting_session_id": 999,
            "option_id": self.test_option.id
        }
        with self.assertRaises(ValueError) as context:
            create_vote(data)
        self.assertEqual(str(context.exception), "Voting session not found")

    def test_get_vote_by_token(self):
        vote = Vote(
            voting_session_id=self.test_session.id,
            option_id=self.test_option.id,
            token="test-token",
            submission_timestamp=datetime.now()
        )
        self.session.add(vote)
        self.session.commit()

        vote_data = get_vote_by_token("test-token")
        self.assertIsNotNone(vote_data)
        self.assertEqual(vote_data["token"], "test-token")

    def test_get_vote_by_token_not_found(self):
        vote_data = get_vote_by_token("non-existent-token")
        self.assertIsNone(vote_data)

    def test_get_all_votes(self):
        vote1 = Vote(
            voting_session_id=self.test_session.id,
            option_id=self.test_option.id,
            token="token1",
            submission_timestamp=datetime.now()
        )
        vote2 = Vote(
            voting_session_id=self.test_session.id,
            option_id=self.test_option.id,
            token="token2",
            submission_timestamp=datetime.now()
        )
        self.session.add_all([vote1, vote2])
        self.session.commit()

        votes = get_all_votes()
        self.assertEqual(len(votes), 2)


if __name__ == "__main__":
    unittest.main()
