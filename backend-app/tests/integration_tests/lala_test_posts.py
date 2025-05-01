import unittest
from routes.app_routes import create_app
from models import db, Country

app = create_app()


class CountryDatabaseIntegrationTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()

        with self.app.app_context():
            db.create_all()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_create_country_in_db(self):
        response = self.client.post('/countries', json={"name": "This is a test country"})
        self.assertEqual(response.status_code, 201)
        data = response.get_json()
        self.assertIn('id', data)
        self.assertEqual(data['name'], 'This is a test country')

        with self.app.app_context():
            country = db.session.get(Country, data['id'])
            self.assertIsNotNone(country)
            self.assertEqual(country.name, 'This is a test country')

    def test_get_country_by_id_from_db(self):
        response = self.client.post('/countries', json={"name": "Test country for DB GET"})
        country_id = response.get_json()['id']

        response = self.client.get(f'/countries/{country_id}')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data['id'], country_id)
        self.assertEqual(data['name'], "Test country for DB GET")

        with self.app.app_context():
            country = db.session.get(Country, country_id)
            self.assertEqual(country.name, "Test country for DB GET")

    def test_update_country_in_db(self):
        response = self.client.post('/countries', json={"name": "Old name"})
        country_id = response.get_json()['id']

        response = self.client.put(f'/countries/{country_id}', json={"name": "Updated name"})
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data['name'], "Updated name")

        with self.app.app_context():
            country = db.session.get(Country, country_id)
            self.assertEqual(country.name, "Updated name")

    def test_delete_country_from_db(self):
        response = self.client.post('/countries', json={"name": "Test country for DELETE"})
        country_id = response.get_json()['id']

        response = self.client.delete(f'/countries/{country_id}')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data['message'], "Country deleted successfully")

        with self.app.app_context():
            country = db.session.get(Country, country_id)
            self.assertIsNone(country)


if __name__ == '__main__':
    unittest.main()
