import unittest
from models import Organization, db
from services.organization_service import (
    create_organization,
    get_organization_by_id,
    get_all_organizations,
    update_organization,
    delete_organization
)
from configs.database import Config
from flask import Flask

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)


class TestOrganizationService(unittest.TestCase):

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

    def test_create_organization(self):
        data = {"name": "Test Organization"}
        organization_data = create_organization(data)

        organization = self.session.query(Organization).filter_by(id=organization_data["id"]).first()
        self.assertIsNotNone(organization)
        self.assertEqual(organization.name, "Test Organization")

    def test_create_organization_invalid_name(self):
        data = {"name": ""}
        with self.assertRaises(ValueError) as context:
            create_organization(data)
        self.assertEqual(str(context.exception), "The 'name' field is required and must be a non-empty string")

    def test_get_organization_by_id(self):
        organization = Organization(name="Test Organization")
        self.session.add(organization)
        self.session.commit()

        organization_data = get_organization_by_id(organization.id)
        self.assertIsNotNone(organization_data)
        self.assertEqual(organization_data["name"], "Test Organization")

    def test_get_organization_by_id_not_found(self):
        organization_data = get_organization_by_id(999)
        self.assertIsNone(organization_data)

    def test_get_all_organizations(self):
        organization1 = Organization(name="Organization 1")
        organization2 = Organization(name="Organization 2")
        self.session.add_all([organization1, organization2])
        self.session.commit()

        organizations = get_all_organizations()
        self.assertEqual(len(organizations), 2)

    def test_update_organization(self):
        organization = Organization(name="Old Organization")
        self.session.add(organization)
        self.session.commit()

        data = {"name": "Updated Organization"}
        updated_organization = update_organization(organization.id, data)

        self.assertEqual(updated_organization["name"], "Updated Organization")

    def test_update_organization_invalid_name(self):
        organization = Organization(name="Old Organization")
        self.session.add(organization)
        self.session.commit()

        data = {"name": ""}
        with self.assertRaises(ValueError) as context:
            update_organization(organization.id, data)
        self.assertEqual(str(context.exception), "The 'name' field must be a non-empty string")

    def test_delete_organization(self):
        organization = Organization(name="Organization to Delete")
        self.session.add(organization)
        self.session.commit()

        response = delete_organization(organization.id)
        self.assertEqual(response["message"], "Organization deleted successfully")

        deleted_organization = self.session.query(Organization).filter_by(id=organization.id).first()
        self.assertIsNone(deleted_organization)

    def test_delete_organization_not_found(self):
        response = delete_organization(999)
        self.assertEqual(response["message"], "Organization not found")


if __name__ == "__main__":
    unittest.main()