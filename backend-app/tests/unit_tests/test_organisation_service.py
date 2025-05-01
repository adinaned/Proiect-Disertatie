import unittest
from models import Organisation, db
from services.organisation_service import (
    create_organisation,
    get_organisation_by_id,
    get_all_organisations,
    update_organisation,
    delete_organisation
)
from configs.database import Config
from flask import Flask

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)


class TestOrganisationService(unittest.TestCase):

    def setUp(self):
        self.app = app
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.session = db.session

        Organisation.metadata.create_all(db.engine)

    def tearDown(self):
        self.session.query(Organisation).delete()
        self.session.commit()

        Organisation.metadata.drop_all(db.engine)

        self.app_context.pop()

    def test_create_organisation(self):
        data = {"name": "Test Organisation"}
        organisation_data = create_organisation(data)

        organisation = self.session.query(Organisation).filter_by(id=organisation_data["id"]).first()
        self.assertIsNotNone(organisation)
        self.assertEqual(organisation.name, "Test Organisation")

    def test_create_organisation_invalid_name(self):
        data = {"name": ""}
        with self.assertRaises(ValueError) as context:
            create_organisation(data)
        self.assertEqual(str(context.exception), "The 'name' field is required and must be a non-empty string")

    def test_get_organisation_by_id(self):
        organisation = Organisation(name="Test Organisation")
        self.session.add(organisation)
        self.session.commit()

        organisation_data = get_organisation_by_id(organisation.id)
        self.assertIsNotNone(organisation_data)
        self.assertEqual(organisation_data["name"], "Test Organisation")

    def test_get_organisation_by_id_not_found(self):
        organisation_data = get_organisation_by_id(999)
        self.assertIsNone(organisation_data)

    def test_get_all_organisations(self):
        organisation1 = Organisation(name="Organisation 1")
        organisation2 = Organisation(name="Organisation 2")
        self.session.add_all([organisation1, organisation2])
        self.session.commit()

        organisations = get_all_organisations()
        self.assertEqual(len(organisations), 2)

    def test_update_organisation(self):
        organisation = Organisation(name="Old Organisation")
        self.session.add(organisation)
        self.session.commit()

        data = {"name": "Updated Organisation"}
        updated_organisation = update_organisation(organisation.id, data)

        self.assertEqual(updated_organisation["name"], "Updated Organisation")

    def test_update_organisation_invalid_name(self):
        organisation = Organisation(name="Old Organisation")
        self.session.add(organisation)
        self.session.commit()

        data = {"name": ""}
        with self.assertRaises(ValueError) as context:
            update_organisation(organisation.id, data)
        self.assertEqual(str(context.exception), "The 'name' field must be a non-empty string")

    def test_delete_organisation(self):
        organisation = Organisation(name="Organisation to Delete")
        self.session.add(organisation)
        self.session.commit()

        response = delete_organisation(organisation.id)
        self.assertEqual(response["message"], "Organisation deleted successfully")

        deleted_organisation = self.session.query(Organisation).filter_by(id=organisation.id).first()
        self.assertIsNone(deleted_organisation)

    def test_delete_organisation_not_found(self):
        response = delete_organisation(999)
        self.assertEqual(response["message"], "Organisation not found")


if __name__ == "__main__":
    unittest.main()