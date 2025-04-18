import unittest
import logging
from src.tests.db_test import create_tables, drop_tables, get_db
from src.models import Country
from sqlalchemy.inspection import inspect

logging.basicConfig(level=logging.DEBUG, format='%(message)s')
logger = logging.getLogger(__name__)


def to_dict(obj):
    if obj is None:
        return None
    return {column.key: getattr(obj, column.key) for column in inspect(obj).mapper.column_attrs}


class TestDatabaseOperations(unittest.TestCase):
    def __init__(self, methodName: str = "runTest"):
        super().__init__(methodName)
        self.transaction = None

    @classmethod
    def setUpClass(cls):
        logger.info("\n=== Setting up the test class ===")
        create_tables()

    @classmethod
    def tearDownClass(cls):
        logger.info("\n\n=== Tearing down the test class ===")
        drop_tables()

    def setUp(self):
        logger.info("\n--- Starting a new test ---")
        drop_tables()
        create_tables()
        self.db = next(get_db())
        logger.debug("Connected to the database session successfully.")

    def tearDown(self):
        logger.debug("Closing the database connection...\n")
        self.db.close()

    def test_create_country_endpoint(self):
        logger.info("\n>>> Test: Creating a country")
        country_data = {"name": "Brazil"}

        country = Country(**country_data)
        self.db.add(country)
        self.db.commit()
        self.db.refresh(country)

        logger.debug("Created country: %s", to_dict(country))
        self.assertIsNotNone(country.id)
        self.assertEqual(country.name, "Brazil")

    def test_get_countries_endpoint(self):
        logger.info("\n>>> Test: Getting all countries")
        loop = 0
        while loop != 2:
            country_data = {"name": f"Spain{loop+1}"}
            country = Country(**country_data)
            self.db.add(country)
            self.db.commit()
            self.db.refresh(country)
            loop += 1

        countries = self.db.query(Country).filter(Country.name == "Spain").all()
        logger.debug("Countries fetched: %s", [to_dict(c) for c in countries])

        self.assertTrue(any(c.name == "Spain" for c in countries))

    def test_get_country_by_id_endpoint(self):
        logger.info("\n>>> Test: Getting country by id")
        country_data = {"name": "TestCountry2"}
        country = Country(**country_data)
        self.db.add(country)
        self.db.commit()
        self.db.refresh(country)

        countries = self.db.query(Country).filter(Country.name == "TestCountry2").all()
        logger.debug("Countries fetched: %s", [to_dict(c) for c in countries])

        self.assertTrue(any(c.name == "TestCountry2" for c in countries))

    def test_put_country_endpoint(self):
        logger.info("\n>>> Test: Updating a country")
        country_data = {"name": "OldCountry"}
        country = Country(**country_data)
        self.db.add(country)
        self.db.commit()
        self.db.refresh(country)

        logger.debug("Country before update: %s", to_dict(country))

        # Update country name
        country.name = "UpdatedCountry"
        self.db.commit()
        self.db.refresh(country)

        logger.debug("Updated country: %s", to_dict(country))
        self.assertEqual(country.name, "UpdatedCountry")

    def test_delete_country_endpoint(self):
        logger.info("\n>>> Test: Deleting a country")
        country_data = {"name": "DeletedCountry"}
        country = Country(**country_data)
        self.db.add(country)
        self.db.commit()
        self.db.refresh(country)

        logger.debug("Country created for deletion: %s", to_dict(country))

        self.db.delete(country)
        self.db.commit()

        logger.debug("Deleted country with ID: %d", country.id)

        deleted_country = self.db.query(Country).filter(Country.id == country.id).first()
        logger.debug("Fetched deleted country: %s", to_dict(deleted_country))

        self.assertIsNone(deleted_country)


if __name__ == "__main__":
    unittest.main()
