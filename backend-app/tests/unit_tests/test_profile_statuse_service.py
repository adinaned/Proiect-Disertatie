import unittest
from datetime import date
from models import ProfileStatus, ProfileStatusEnum, db
from services.profile_status_service import (
    create_profile_status,
    get_profile_status_by_id,
    get_all_profile_statuses,
    update_profile_status,
    delete_profile_status
)
from configs.database import Config
from flask import Flask

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)


class TestProfileStatusService(unittest.TestCase):

    def setUp(self):
        self.app = app
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.session = db.session

        ProfileStatus.metadata.create_all(db.engine)

    def tearDown(self):
        self.session.query(ProfileStatus).delete()
        self.session.commit()

        ProfileStatus.metadata.drop_all(db.engine)

        self.app_context.pop()

    def test_create_profile_status(self):
        data = {
            "name": ProfileStatusEnum.ACTIVE.value,
            "updated_at": date.today()
        }
        profile_status_data = create_profile_status(data)

        profile_status = self.session.query(ProfileStatus).filter_by(id=profile_status_data["id"]).first()
        self.assertIsNotNone(profile_status)
        self.assertEqual(profile_status.name, ProfileStatusEnum.ACTIVE)
        self.assertEqual(profile_status.updated_at, date.today())

    def test_create_profile_status_invalid_name(self):
        data = {
            "name": "invalid_status",
            "updated_at": date.today()
        }
        with self.assertRaises(ValueError) as context:
            create_profile_status(data)
        self.assertIn("must be one of", str(context.exception))

    def test_get_profile_status_by_id(self):
        profile_status = ProfileStatus(
            name=ProfileStatusEnum.OPEN,
            updated_at=date.today()
        )
        self.session.add(profile_status)
        self.session.commit()

        profile_status_data = get_profile_status_by_id(profile_status.id)
        self.assertIsNotNone(profile_status_data)
        self.assertEqual(profile_status_data["name"], ProfileStatusEnum.OPEN.value)

    def test_get_profile_status_by_id_not_found(self):
        profile_status_data = get_profile_status_by_id(999)
        self.assertIsNone(profile_status_data)

    def test_get_all_profile_statuses(self):
        status1 = ProfileStatus(name=ProfileStatusEnum.ACTIVE, updated_at=date.today())
        status2 = ProfileStatus(name=ProfileStatusEnum.SUSPENDED, updated_at=date.today())
        self.session.add_all([status1, status2])
        self.session.commit()

        profile_statuses = get_all_profile_statuses()
        self.assertEqual(len(profile_statuses), 2)

    def test_update_profile_status(self):
        profile_status = ProfileStatus(
            name=ProfileStatusEnum.OPEN,
            updated_at=date.today()
        )
        self.session.add(profile_status)
        self.session.commit()

        data = {"name": ProfileStatusEnum.CLOSED.value}
        updated_profile_status = update_profile_status(profile_status.id, data)

        self.assertEqual(updated_profile_status["name"], ProfileStatusEnum.CLOSED.value)

    def test_update_profile_status_invalid_name(self):
        profile_status = ProfileStatus(
            name=ProfileStatusEnum.OPEN,
            updated_at=date.today()
        )
        self.session.add(profile_status)
        self.session.commit()

        data = {"name": "invalid_status"}
        with self.assertRaises(ValueError) as context:
            update_profile_status(profile_status.id, data)
        self.assertIn("must be one of", str(context.exception))

    def test_delete_profile_status(self):
        profile_status = ProfileStatus(
            name=ProfileStatusEnum.SUSPENDED,
            updated_at=date.today()
        )
        self.session.add(profile_status)
        self.session.commit()

        response = delete_profile_status(profile_status.id)
        self.assertEqual(response["message"], "ProfileStatus deleted successfully")

        deleted_profile_status = self.session.query(ProfileStatus).filter_by(id=profile_status.id).first()
        self.assertIsNone(deleted_profile_status)

    def test_delete_profile_status_not_found(self):
        response = delete_profile_status(999)
        self.assertEqual(response["message"], "ProfileStatus not found")


if __name__ == "__main__":
    unittest.main()
