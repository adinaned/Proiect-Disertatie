import unittest
from models import Organization, db
from services.organization_service import (
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

        Organization.metadata.create_all(db.engine)

    def tearDown(self):
        self.session.query(Organization).delete()
        self.session.commit()

        Organization.metadata.drop_all(db.engine)

        self.app_context.pop()

    def test_create_organisation(self):
        data = {"name": "Test Organization"}
        organisation_data = create_organisation(data)

        organization = self.session.query(Organization).filter_by(id=organisation_data["id"]).first()
        self.assertIsNotNone(organization)
        self.assertEqual(organization.name, "Test Organization")

    def test_create_organisation_invalid_name(self):
        data = {"name": ""}
        with self.assertRaises(ValueError) as context:
            create_organisation(data)
        self.assertEqual(str(context.exception), "The 'name' field is required and must be a non-empty string")

    def test_get_organisation_by_id(self):
        organization = Organization(name="Test Organization")
        self.session.add(organization)
        self.session.commit()

        organisation_data = get_organisation_by_id(organization.id)
        self.assertIsNotNone(organisation_data)
        self.assertEqual(organisation_data["name"], "Test Organization")

    def test_get_organisation_by_id_not_found(self):
        organisation_data = get_organisation_by_id(999)
        self.assertIsNone(organisation_data)

    def test_get_all_organisations(self):
        organisation1 = Organization(name="Organization 1")
        organisation2 = Organization(name="Organization 2")
        self.session.add_all([organisation1, organisation2])
        self.session.commit()

        organisations = get_all_organisations()
        self.assertEqual(len(organisations), 2)

    def test_update_organisation(self):
        organization = Organization(name="Old Organization")
        self.session.add(organization)
        self.session.commit()

        data = {"name": "Updated Organization"}
        updated_organisation = update_organisation(organization.id, data)

        self.assertEqual(updated_organisation["name"], "Updated Organization")

    def test_update_organisation_invalid_name(self):
        organization = Organization(name="Old Organization")
        self.session.add(organization)
        self.session.commit()

        data = {"name": ""}
        with self.assertRaises(ValueError) as context:
            update_organisation(organization.id, data)
        self.assertEqual(str(context.exception), "The 'name' field must be a non-empty string")

    def test_delete_organisation(self):
        organization = Organization(name="Organization to Delete")
        self.session.add(organization)
        self.session.commit()

        response = delete_organisation(organization.id)
        self.assertEqual(response["message"], "Organization deleted successfully")

        deleted_organisation = self.session.query(Organization).filter_by(id=organization.id).first()
        self.assertIsNone(deleted_organisation)

    def test_delete_organisation_not_found(self):
        response = delete_organisation(999)
        self.assertEqual(response["message"], "Organization not found")


if __name__ == "__main__":
    unittest.main()