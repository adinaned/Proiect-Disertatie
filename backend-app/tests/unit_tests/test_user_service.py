import unittest
from datetime import date
from models import User, Role, Organization, ProfileStatus, Country, db
from services.user_service import (
    create_user,
    get_user_by_id,
    get_all_users,
    update_user,
    delete_user
)
from configs.database import Config
from flask import Flask

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)


class TestUserService(unittest.TestCase):

    def setUp(self):
        self.app = app
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.session = db.session

        # Create tables
        User.metadata.create_all(db.engine)
        Organization.metadata.create_all(db.engine)
        Role.metadata.create_all(db.engine)
        ProfileStatus.metadata.create_all(db.engine)
        Country.metadata.create_all(db.engine)

        # Add test dependencies
        self.test_organisation = Organization(name="Test Organization")
        self.test_role = Role(name="Test Role", organisation_id=1)
        self.test_profile_status = ProfileStatus(name=ProfileStatusEnum.ACTIVE)
        self.test_country = Country(name="Test Country")

        self.session.add_all([self.test_organisation, self.test_role, self.test_profile_status, self.test_country])
        self.session.commit()

    def tearDown(self):
        self.session.query(User).delete()
        self.session.query(Organization).delete()
        self.session.query(Role).delete()
        self.session.query(ProfileStatus).delete()
        self.session.query(Country).delete()
        self.session.commit()

        # Drop tables
        User.metadata.drop_all(db.engine)
        Organization.metadata.drop_all(db.engine)
        Role.metadata.drop_all(db.engine)
        ProfileStatus.metadata.drop_all(db.engine)
        Country.metadata.drop_all(db.engine)

        self.app_context.pop()

    def test_create_user(self):
        data = {
            "first_name": "John",
            "last_name": "Doe",
            "date_of_birth": date(1990, 1, 1),
            "country_id": self.test_country.id,
            "city": "Test City",
            "address": "123 Test Street",
            "national_id": 123456,
            "role_id": self.test_role.id,
            "organisation_id": self.test_organisation.id,
            "profile_status_id": self.test_profile_status.id,
            "created_at": date.today()
        }
        user_data = create_user(data)

        user = self.session.query(User).filter_by(id=user_data["id"]).first()
        self.assertIsNotNone(user)
        self.assertEqual(user.first_name, "John")
        self.assertEqual(user.last_name, "Doe")

    def test_create_user_invalid_first_name(self):
        data = {"first_name": "", "last_name": "Doe"}
        with self.assertRaises(ValueError) as context:
            create_user(data)
        self.assertEqual(str(context.exception), "The 'first_name' field is required and must be a non-empty string")

    def test_get_user_by_id(self):
        user = User(
            first_name="John",
            last_name="Doe",
            date_of_birth=date(1990, 1, 1),
            role_id=self.test_role.id,
            organisation_id=self.test_organisation.id,
            profile_status_id=self.test_profile_status.id
        )
        self.session.add(user)
        self.session.commit()

        user_data = get_user_by_id(user.id)
        self.assertIsNotNone(user_data)
        self.assertEqual(user_data["first_name"], "John")

    def test_get_user_by_id_not_found(self):
        user_data = get_user_by_id(999)
        self.assertIsNone(user_data)

    def test_get_all_users(self):
        user1 = User(first_name="John", last_name="Doe", role_id=self.test_role.id)
        user2 = User(first_name="Jane", last_name="Smith", role_id=self.test_role.id)
        self.session.add_all([user1, user2])
        self.session.commit()

        users = get_all_users()
        self.assertEqual(len(users), 2)

    def test_update_user(self):
        user = User(first_name="John", last_name="Doe", role_id=self.test_role.id)
        self.session.add(user)
        self.session.commit()

        data = {"first_name": "Updated John"}
        updated_user = update_user(user.id, data)

        self.assertEqual(updated_user["first_name"], "Updated John")

    def test_update_user_invalid_first_name(self):
        user = User(first_name="John", last_name="Doe", role_id=self.test_role.id)
        self.session.add(user)
        self.session.commit()

        data = {"first_name": ""}
        with self.assertRaises(ValueError) as context:
            update_user(user.id, data)
        self.assertEqual(str(context.exception), "The 'first_name' field must be a non-empty string")

    def test_delete_user(self):
        user = User(first_name="John", last_name="Doe", role_id=self.test_role.id)
        self.session.add(user)
        self.session.commit()

        response = delete_user(user.id)
        self.assertEqual(response["message"], "User deleted successfully")

        deleted_user = self.session.query(User).filter_by(id=user.id).first()
        self.assertIsNone(deleted_user)

    def test_delete_user_not_found(self):
        response = delete_user(999)
        self.assertEqual(response["message"], "User not found")


if __name__ == "__main__":
    unittest.main()
