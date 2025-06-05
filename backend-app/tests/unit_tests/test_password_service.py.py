import unittest
from datetime import date
from models import Password, User, db
from services.password_service import (
    create_password,
    get_password_by_user_id,
    update_password,
    delete_password
)
from configs.database import Config
from flask import Flask

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)


class TestPasswordService(unittest.TestCase):

    def setUp(self):
        self.app = app
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.session = db.session

        Password.metadata.create_all(db.engine)
        User.metadata.create_all(db.engine)

        # Add a test user
        self.test_user = User(name="Test User", email="testuser@example.com")
        self.session.add(self.test_user)
        self.session.commit()

    def tearDown(self):
        self.session.query(Password).delete()
        self.session.query(User).delete()
        self.session.commit()

        Password.metadata.drop_all(db.engine)
        User.metadata.drop_all(db.engine)

        self.app_context.pop()

    def test_create_password(self):
        data = {
            "user_id": self.test_user.id,
            "password": "password_123",
            "updated_at": date.today()
        }
        password_data = create_password(data)

        password = self.session.query(Password).filter_by(id=password_data["id"]).first()
        self.assertIsNotNone(password)
        self.assertEqual(password.password, "password_123")
        self.assertEqual(password.user_id, self.test_user.id)

    def test_create_password_invalid_user_id(self):
        data = {
            "user_id": "invalid",
            "password": "password_123",
            "updated_at": date.today()
        }
        with self.assertRaises(ValueError) as context:
            create_password(data)
        self.assertEqual(str(context.exception), "The 'user_id' field is required and must be an integer")

    def test_get_password_by_user_id(self):
        password = Password(
            user_id=self.test_user.id,
            password="password_123",
            updated_at=date.today()
        )
        self.session.add(password)
        self.session.commit()

        password_data = get_password_by_user_id(self.test_user.id)
        self.assertIsNotNone(password_data)
        self.assertEqual(password_data["password"], "password_123")

    def test_get_password_by_user_id_not_found(self):
        with self.assertRaises(ValueError) as context:
            get_password_by_user_id(999)
        self.assertEqual(str(context.exception), "User with id 999 does not exist")

    def test_update_password(self):
        password = Password(
            user_id=self.test_user.id,
            password="old_password",
            updated_at=date.today()
        )
        self.session.add(password)
        self.session.commit()

        data = {"password": "new_password"}
        updated_password = update_password(password.id, data)

        self.assertEqual(updated_password["password"], "new_password")

    def test_update_password_invalid_password(self):
        password = Password(
            user_id=self.test_user.id,
            password="old_password",
            updated_at=date.today()
        )
        self.session.add(password)
        self.session.commit()

        data = {"password": ""}
        with self.assertRaises(ValueError) as context:
            update_password(password.id, data)
        self.assertEqual(str(context.exception), "The 'password' field must be a non-empty string")

    def test_delete_password(self):
        password = Password(
            user_id=self.test_user.id,
            password="password_to_delete",
            updated_at=date.today()
        )
        self.session.add(password)
        self.session.commit()

        response = delete_password(password.id)
        self.assertEqual(response["message"], "Password deleted successfully")

        deleted_password = self.session.query(Password).filter_by(id=password.id).first()
        self.assertIsNone(deleted_password)

    def test_delete_password_not_found(self):
        response = delete_password(999)
        self.assertEqual(response["message"], "Password not found")


if __name__ == "__main__":
    unittest.main()
