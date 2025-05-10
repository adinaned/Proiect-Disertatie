import unittest
from models import Role, Organization, db
from services.role_service import (
    create_role,
    get_role_by_id,
    get_all_roles,
    update_role,
    delete_role
)
from configs.database import Config
from flask import Flask

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)


class TestRoleService(unittest.TestCase):

    def setUp(self):
        self.app = app
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.session = db.session

        Role.metadata.create_all(db.engine)
        Organization.metadata.create_all(db.engine)

        # Add a test organization
        self.test_organisation = Organization(name="Test Organization")
        self.session.add(self.test_organisation)
        self.session.commit()

    def tearDown(self):
        self.session.query(Role).delete()
        self.session.query(Organization).delete()
        self.session.commit()

        Role.metadata.drop_all(db.engine)
        Organization.metadata.drop_all(db.engine)

        self.app_context.pop()

    def test_create_role(self):
        data = {
            "name": "Test Role",
            "organisation_id": self.test_organisation.id
        }
        role_data = create_role(data)

        role = self.session.query(Role).filter_by(id=role_data["id"]).first()
        self.assertIsNotNone(role)
        self.assertEqual(role.name, "Test Role")
        self.assertEqual(role.organisation_id, self.test_organisation.id)

    def test_create_role_invalid_name(self):
        data = {
            "name": "",
            "organisation_id": self.test_organisation.id
        }
        with self.assertRaises(ValueError) as context:
            create_role(data)
        self.assertEqual(str(context.exception), "The 'name' field is required and must be a non-empty string")

    def test_get_role_by_id(self):
        role = Role(name="Test Role", organisation_id=self.test_organisation.id)
        self.session.add(role)
        self.session.commit()

        role_data = get_role_by_id(role.id)
        self.assertIsNotNone(role_data)
        self.assertEqual(role_data["name"], "Test Role")

    def test_get_role_by_id_not_found(self):
        role_data = get_role_by_id(999)
        self.assertIsNone(role_data)

    def test_get_all_roles(self):
        role1 = Role(name="Role 1", organisation_id=self.test_organisation.id)
        role2 = Role(name="Role 2", organisation_id=self.test_organisation.id)
        self.session.add_all([role1, role2])
        self.session.commit()

        roles = get_all_roles()
        self.assertEqual(len(roles), 2)

    def test_update_role(self):
        role = Role(name="Old Role", organisation_id=self.test_organisation.id)
        self.session.add(role)
        self.session.commit()

        data = {"name": "Updated Role"}
        updated_role = update_role(role.id, data)

        self.assertEqual(updated_role["name"], "Updated Role")

    def test_update_role_invalid_name(self):
        role = Role(name="Old Role", organisation_id=self.test_organisation.id)
        self.session.add(role)
        self.session.commit()

        data = {"name": ""}
        with self.assertRaises(ValueError) as context:
            update_role(role.id, data)
        self.assertEqual(str(context.exception), "The 'name' field must be a non-empty string")

    def test_delete_role(self):
        role = Role(name="Role to Delete", organisation_id=self.test_organisation.id)
        self.session.add(role)
        self.session.commit()

        response = delete_role(role.id)
        self.assertEqual(response["message"], "Role deleted successfully")

        deleted_role = self.session.query(Role).filter_by(id=role.id).first()
        self.assertIsNone(deleted_role)

    def test_delete_role_not_found(self):
        response = delete_role(999)
        self.assertEqual(response["message"], "Role not found")


if __name__ == "__main__":
    unittest.main()
