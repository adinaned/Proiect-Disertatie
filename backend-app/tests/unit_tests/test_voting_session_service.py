import unittest
from datetime import datetime, timedelta
from models import VotingSession, Role, Organization, db
from services.voting_session_service import (
    create_voting_session,
    get_voting_session_by_id,
    get_all_voting_sessions,
    update_voting_session,
    delete_voting_session
)
from configs.database import Config
from flask import Flask

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)


class TestVotingSessionService(unittest.TestCase):

    def setUp(self):
        self.app = app
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.session = db.session

        VotingSession.metadata.create_all(db.engine)
        Role.metadata.create_all(db.engine)
        Organization.metadata.create_all(db.engine)

        # Add test dependencies
        self.test_role = Role(name="Test Role", organization_id=1)
        self.test_organization = Organization(name="Test Organization")
        self.session.add_all([self.test_role, self.test_organization])
        self.session.commit()

    def tearDown(self):
        self.session.query(VotingSession).delete()
        self.session.query(Role).delete()
        self.session.query(Organization).delete()
        self.session.commit()

        VotingSession.metadata.drop_all(db.engine)
        Role.metadata.drop_all(db.engine)
        Organization.metadata.drop_all(db.engine)

        self.app_context.pop()

    def test_create_voting_session(self):
        data = {
            "title": "Test Voting Session",
            "start_time": datetime.utcnow(),
            "end_time": datetime.utcnow() + timedelta(days=1),
            "role_id": self.test_role.id,
            "organization_id": self.test_organization.id
        }
        voting_session_data = create_voting_session(data)

        voting_session = self.session.query(VotingSession).filter_by(id=voting_session_data["id"]).first()
        self.assertIsNotNone(voting_session)
        self.assertEqual(voting_session.title, "Test Voting Session")

    def test_create_voting_session_invalid_title(self):
        data = {"title": "Invalid title"}
        with self.assertRaises(ValueError) as context:
            create_voting_session(data)
        self.assertEqual(str(context.exception), "The 'title' field is required and must be a non-empty string")

    def test_get_voting_session_by_id(self):
        voting_session = VotingSession(
            title="Test Voting Session",
            question="What is your opinion?",
            start_time=datetime.utcnow(),
            end_time=datetime.utcnow() + timedelta(days=1),
            role_id=self.test_role.id,
            organization_id=self.test_organization.id
        )
        self.session.add(voting_session)
        self.session.commit()

        voting_session_data = get_voting_session_by_id(voting_session.id)
        self.assertIsNotNone(voting_session_data)
        self.assertEqual(voting_session_data["title"], "Test Voting Session")

    def test_get_voting_session_by_id_not_found(self):
        voting_session_data = get_voting_session_by_id(999)
        self.assertIsNone(voting_session_data)

    def test_get_all_voting_sessions(self):
        voting_session1 = VotingSession(
            title="Session 1",
            question="What is your opinion on Session 1?",
            start_time=datetime.utcnow(),
            end_time=datetime.utcnow() + timedelta(days=1),
            role_id=self.test_role.id,
            organization_id=self.test_organization.id
        )
        voting_session2 = VotingSession(
            title="Session 2",
            question="What is your opinion on Session 2?",
            start_time=datetime.utcnow(),
            end_time=datetime.utcnow() + timedelta(days=1),
            role_id=self.test_role.id,
            organization_id=self.test_organization.id
        )
        self.session.add_all([voting_session1, voting_session2])
        self.session.commit()

        voting_sessions = get_all_voting_sessions()
        self.assertEqual(len(voting_sessions), 2)

    def test_update_voting_session(self):
        voting_session = VotingSession(
            title="Old Title",
            question="What is your opinion?",
            start_time=datetime.utcnow(),
            end_time=datetime.utcnow() + timedelta(days=1),
            role_id=self.test_role.id,
            organization_id=self.test_organization.id
        )
        self.session.add(voting_session)
        self.session.commit()

        data = {"title": "Updated Title"}
        updated_session = update_voting_session(voting_session.id, data)

        self.assertEqual(updated_session["title"], "Updated Title")

    def test_update_voting_session_invalid_title(self):
        voting_session = VotingSession(
            title="Old Title",
            question="What is your opinion?",
            start_time=datetime.utcnow(),
            end_time=datetime.utcnow() + timedelta(days=1),
            role_id=self.test_role.id,
            organization_id=self.test_organization.id
        )
        self.session.add(voting_session)
        self.session.commit()

        data = {"title": ""}
        with self.assertRaises(ValueError) as context:
            update_voting_session(voting_session.id, data)
        self.assertEqual(str(context.exception), "The 'title' field must be a non-empty string")

    def test_delete_voting_session(self):
        voting_session = VotingSession(
            title="Session to Delete",
            question="What is your opinion?",
            start_time=datetime.utcnow(),
            end_time=datetime.utcnow() + timedelta(days=1),
            role_id=self.test_role.id,
            organization_id=self.test_organization.id
        )
        self.session.add(voting_session)
        self.session.commit()

        response = delete_voting_session(voting_session.id)
        self.assertEqual(response["message"], "Voting session deleted successfully")

        deleted_session = self.session.query(VotingSession).filter_by(id=voting_session.id).first()
        self.assertIsNone(deleted_session)

    def test_delete_voting_session_not_found(self):
        response = delete_voting_session(999)
        self.assertEqual(response["message"], "Voting session not found")


if __name__ == "__main__":
    unittest.main()
