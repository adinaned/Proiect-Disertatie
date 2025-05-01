import unittest
from models import Country, db
from configs.database import Config
from flask import Flask
from services import (
    create_country, get_country_by_id, get_all_countries,
    update_country, delete_country)
import logging

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)

logging.basicConfig(level=logging.DEBUG, format='%(message)s')
logger = logging.getLogger(__name__)


class TestCountryService(unittest.TestCase):

    def setUp(self):
        logger.info("\n\n------------ Starting a new test ------------")
        self.app = app
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.session = db.session

        # Create tables for each test
        Country.metadata.create_all(db.engine)
        logger.info("Created all tables in the database.")

    def tearDown(self):
        self.session.query(Country).delete()
        self.session.commit()
        logger.info("Deleted all countries from the database.")

        Country.metadata.drop_all(db.engine)
        logger.info("Dropped all tables from the database.")

        self.app_context.pop()

    @classmethod
    def tearDownClass(cls):
        logger.info("\n\n------------ Tearing down the test class ------------")

    @classmethod
    def setUpClass(cls):
        logger.info("\n------------ Setting up the test class ------------\n")

    def test_create_country(self):
        logger.info("\n>>> Test: Creating a country")
        data = {"name": "This is a valid country with more than 10 characters"}
        logger.debug(f"Data to create country: {data}")
        country_data = create_country(data)

        country = self.session.query(Country).filter_by(id=country_data["id"]).first()
        self.assertIsNotNone(country)
        self.assertEqual(country.name, "This is a valid country with more than 10 characters")
        logger.info(f"Created country with ID {country.id} and name '{country.name}'.")

    def test_create_country_empty_name(self):
        logger.info("\n>>> Test: Creating a country with empty name")
        data = {"name": ""}
        logger.debug(f"Data to create country: {data}")
        with self.assertRaises(ValueError):
            create_country(data)
        logger.error("Attempted to create a country with an empty name, raised ValueError.")

    def test_create_country_short_name(self):
        logger.info("\n>>> Test: Creating a country with an invalid name length")
        data = {"name": "a"}
        logger.debug(f"Data to create country: {data}")
        with self.assertRaises(ValueError):
            create_country(data)
        logger.error("Attempted to create a country with a name shorter than 2 characters, raised ValueError.")

    def test_get_country(self):
        logger.info("\n>>> Test: Getting country by id")
        country = Country(name="Test country")
        self.session.add(country)
        self.session.commit()
        logger.debug(f"Added country with ID {country.id} and name '{country.name}' to the database.")

        country_data = get_country_by_id(country.id)
        self.assertIsNotNone(country_data)
        self.assertEqual(country_data["name"], "Test country")
        logger.info(f"Retrieved country with ID {country.id} and name '{country_data['name']}'.")

    def test_get_country_not_found(self):
        logger.info("\n>>> Test: Getting a country that does not exist")
        country_data = get_country_by_id(9999)
        self.assertIsNone(country_data)
        logger.info("Tried to retrieve a non-existent country (ID 9999), got None.")

    def test_get_all_countries(self):
        logger.info("\n>>> Test: Getting all countries")
        country1 = Country(name="First country")
        country2 = Country(name="Second country")
        self.session.add(country1)
        self.session.add(country2)
        self.session.commit()
        logger.debug(f"Added countries with names '{country1.name}' and '{country2.name}'.")

        countries_data = get_all_countries()
        self.assertEqual(len(countries_data), 2)
        logger.info(f"Retrieved {len(countries_data)} countries from the database.")

    def test_update_country(self):
        logger.info("\n>>> Test: Updating a country")
        country = Country(name="Initial name")
        self.session.add(country)
        self.session.commit()
        logger.debug(f"Added country with ID {country.id} and name '{country.name}' to the database.")

        data = {"name": "Updated name", "sentiment": "positive"}
        logger.debug(f"Data to update country: {data}")
        updated_country = update_country(country.id, data)

        self.assertEqual(updated_country["name"], "Updated name")
        logger.info(f"Updated country with ID {updated_country['id']} to new name '{updated_country['name']}'.")

    def test_update_country_not_found(self):
        logger.info("\n>>> Test: Updating a country that does not exist")
        data = {"name": "Updated name"}
        logger.debug(f"Data to update non-existent country: {data}")
        with self.assertRaises(ValueError):
            update_country(9999, data)
        logger.error("Attempted to update a non-existent country (ID 9999), raised ValueError.")

    def test_delete_country(self):
        logger.info("\n>>> Test: Deleting a country")
        country = Country(name="Country to delete")
        self.session.add(country)
        self.session.commit()
        logger.debug(f"Added country with ID {country.id} and name '{country.name}' to the database.")

        response = delete_country(country.id)
        self.assertEqual(response["message"], "Country deleted successfully")

        deleted_country = self.session.query(Country).filter_by(id=country.id).first()
        self.assertIsNone(deleted_country)
        logger.info(f"Deleted country with ID {country.id} and name '{country.name}'.")

    def test_delete_country_not_found(self):
        logger.info("\n>>> Test: Deleting a country that does not exist")
        response = delete_country(9999)
        self.assertEqual(response["message"], "Country not found")
        logger.info("Tried to delete a non-existent country (ID 9999), got 'Country not found' response.")


if __name__ == '__main__':
    unittest.main()
