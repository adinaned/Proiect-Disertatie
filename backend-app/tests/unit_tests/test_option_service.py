import unittest
from models import Option, db
from services.option_service import (
    create_option,
    get_option_by_id,
    get_all_options,
    update_option,
    delete_option
)
from configs.database import Config
from flask import Flask

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)


class TestOptionService(unittest.TestCase):

    def setUp(self):
        self.app = app
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.session = db.session

        Option.metadata.create_all(db.engine)

    def tearDown(self):
        self.session.query(Option).delete()
        self.session.commit()

        Option.metadata.drop_all(db.engine)

        self.app_context.pop()

    def test_create_option(self):
        data = {
            "name": "Option 1",
            "session_id": 1
        }
        option_data = create_option(data)

        option = self.session.query(Option).filter_by(id=option_data["id"]).first()
        self.assertIsNotNone(option)
        self.assertEqual(option.name, "Option 1")
        self.assertEqual(option.session_id, 1)

    def test_create_option_invalid_name(self):
        data = {
            "name": "",
            "session_id": 1
        }
        with self.assertRaises(ValueError) as context:
            create_option(data)
        self.assertEqual(str(context.exception), "The 'name' field is required and must be a non-empty string")

    def test_get_option_by_id(self):
        option = Option(name="Option 1", session_id=1)
        self.session.add(option)
        self.session.commit()

        option_data = get_option_by_id(option.id)
        self.assertIsNotNone(option_data)
        self.assertEqual(option_data["name"], "Option 1")

    def test_get_option_by_id_not_found(self):
        option_data = get_option_by_id(999)
        self.assertIsNone(option_data)

    def test_get_all_options(self):
        option1 = Option(name="Option 1", session_id=1)
        option2 = Option(name="Option 2", session_id=1)
        self.session.add_all([option1, option2])
        self.session.commit()

        options = get_all_options()
        self.assertEqual(len(options), 2)

    def test_update_option(self):
        option = Option(name="Old Option", session_id=1)
        self.session.add(option)
        self.session.commit()

        data = {"name": "Updated Option"}
        updated_option = update_option(option.id, data)

        self.assertEqual(updated_option["name"], "Updated Option")

    def test_update_option_invalid_name(self):
        option = Option(name="Old Option", session_id=1)
        self.session.add(option)
        self.session.commit()

        data = {"name": ""}
        with self.assertRaises(ValueError) as context:
            update_option(option.id, data)
        self.assertEqual(str(context.exception), "The 'name' field must be a non-empty string")

    def test_delete_option(self):
        option = Option(name="Option to Delete", session_id=1)
        self.session.add(option)
        self.session.commit()

        response = delete_option(option.id)
        self.assertEqual(response["message"], "Option deleted successfully")

        deleted_option = self.session.query(Option).filter_by(id=option.id).first()
        self.assertIsNone(deleted_option)

    def test_delete_option_not_found(self):
        response = delete_option(999)
        self.assertEqual(response["message"], "Option not found")


if __name__ == "__main__":
    unittest.main()