import unittest
from datetime import date
from models import Email, User, db
from services.email_service import (create_email, get_email_by_id, get_all_emails, update_email, delete_email)
from configs.database import Config
from flask import Flask

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)


class TestEmailService(unittest.TestCase):

    def setUp(self):
        self.app = app
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.session = db.session

        Email.metadata.create_all(db.engine)
        User.metadata.create_all(db.engine)

        self.test_user = User(name="Test User", email="testuser@example.com")
        self.session.add(self.test_user)
        self.session.commit()

    def tearDown(self):
        self.session.query(Email).delete()
        self.session.query(User).delete()
        self.session.commit()

        Email.metadata.drop_all(db.engine)
        User.metadata.drop_all(db.engine)

        self.app_context.pop()

    def test_create_email(self):
        data = {
            "email_address": "test@example.com",
            "user_id": self.test_user.id
        }
        email_data = create_email(data)

        email = self.session.query(Email).filter_by(id=email_data["id"]).first()
        self.assertIsNotNone(email)
        self.assertEqual(email.email_address, "test@example.com")
        self.assertEqual(email.user_id, self.test_user.id)

    def test_create_email_invalid_format(self):
        data = {
            "email_address": "invalid-email",
            "user_id": self.test_user.id
        }
        with self.assertRaises(ValueError) as context:
            create_email(data)
        self.assertEqual(str(context.exception), "Invalid email format")

    def test_get_email_by_id(self):
        email = Email(
            email_address="test@example.com",
            user_id=self.test_user.id,
            is_verified=False,
            created_at=date.today()
        )
        self.session.add(email)
        self.session.commit()

        email_data = get_email_by_id(email.id)
        self.assertIsNotNone(email_data)
        self.assertEqual(email_data["email_address"], "test@example.com")

    def test_get_email_by_id_not_found(self):
        email_data = get_email_by_id(999)
        self.assertIsNone(email_data)

    def test_get_all_emails(self):
        email1 = Email(
            email_address="test1@example.com",
            user_id=self.test_user.id,
            is_verified=False,
            created_at=date.today()
        )
        email2 = Email(
            email_address="test2@example.com",
            user_id=self.test_user.id,
            is_verified=False,
            created_at=date.today()
        )
        self.session.add_all([email1, email2])
        self.session.commit()

        emails = get_all_emails()
        self.assertEqual(len(emails), 2)

    def test_update_email(self):
        email = Email(
            email_address="old@example.com",
            user_id=self.test_user.id,
            is_verified=False,
            created_at=date.today()
        )
        self.session.add(email)
        self.session.commit()

        data = {"email_address": "new@example.com"}
        updated_email = update_email(email.id, data)

        self.assertEqual(updated_email["email_address"], "new@example.com")

    def test_update_email_invalid_format(self):
        email = Email(
            email_address="old@example.com",
            user_id=self.test_user.id,
            is_verified=False,
            created_at=date.today()
        )
        self.session.add(email)
        self.session.commit()

        data = {"email_address": "invalid-email"}
        with self.assertRaises(ValueError) as context:
            update_email(email.id, data)
        self.assertEqual(str(context.exception), "Invalid email format")

    def test_delete_email(self):
        email = Email(
            email_address="test@example.com",
            user_id=self.test_user.id,
            is_verified=False,
            created_at=date.today()
        )
        self.session.add(email)
        self.session.commit()

        response = delete_email(email.id)
        self.assertEqual(response["message"], "Email deleted successfully")

        deleted_email = self.session.query(Email).filter_by(id=email.id).first()
        self.assertIsNone(deleted_email)

    def test_delete_email_not_found(self):
        response = delete_email(999)
        self.assertEqual(response["message"], "Email not found")


if __name__ == "__main__":
    unittest.main()
