import unittest
import logging
from src.tests.db_test import create_tables, drop_tables, get_db
from sqlalchemy.inspection import inspect


logging.basicConfig(level=logging.DEBUG, format='%(message)s')
logger = logging.getLogger(__name__)


def to_dict(obj):
    if obj is None:
        return None
    return {column.key: getattr(obj, column.key) for column in inspect(obj).mapper.column_attrs}


class BaseDatabaseTest(unittest.TestCase):
    def __init__(self, methodName: str = "runTest", model=None):
        if model is None:
            raise ValueError("Model must be provided for the test")
        super().__init__(methodName)
        self.model = model
        self.transaction = None

    @classmethod
    def setUpClass(cls):
        logger.info("\n=== Setting up the test class ===\n")
        create_tables()

    @classmethod
    def tearDownClass(cls):
        logger.info("\n\n=== Tearing down the test class ===")
        drop_tables()

    def setUp(self):
        logger.info("-------------- Starting a new test --------------")
        drop_tables()
        create_tables()
        self.db = next(get_db())

    def tearDown(self):
        logger.debug("Closing the database connection...\n")
        self.db.close()

    def test_create(self):
        logger.info(f">>> Test: Creating a {self.model.__name__}\n")
        data = {"name": "Test"}
        item = self.model(**data)
        self.db.add(item)
        self.db.commit()
        self.db.refresh(item)

        logger.debug(f"Created {self.model.__name__}: %s", to_dict(item))
        self.assertIsNotNone(item.id)
        self.assertEqual(item.name, "Test")

    def test_get_all(self):
        logger.info(f">>> Test: Getting all {self.model.__name__}s\n")
        data = [{"name": "Test1"}, {"name": "Test2"}]
        for entry in data:
            item = self.model(**entry)
            self.db.add(item)
        self.db.commit()

        items = self.db.query(self.model).all()
        logger.debug(f"All {self.model.__name__}s: %s", [to_dict(i) for i in items])

        self.assertGreaterEqual(len(items), 2)

    def test_get_by_id(self):
        logger.info(f">>> Test: Getting {self.model.__name__} by id\n")
        data = {"name": "Test"}
        item = self.model(**data)
        self.db.add(item)
        self.db.commit()
        self.db.refresh(item)

        fetched_item = self.db.query(self.model).filter(self.model.id == item.id).first()
        logger.debug(f"{self.model.__name__} fetched by ID: %s", to_dict(fetched_item))

        self.assertIsNotNone(fetched_item)
        self.assertEqual(fetched_item.name, "Test")

    def test_update(self):
        logger.info(f">>> Test: Updating a {self.model.__name__}\n")
        data = {"name": "OldName"}
        item = self.model(**data)
        self.db.add(item)
        self.db.commit()
        self.db.refresh(item)

        item.name = "UpdatedName"
        self.db.commit()
        self.db.refresh(item)

        logger.debug(f"Updated {self.model.__name__}: %s", to_dict(item))
        self.assertEqual(item.name, "UpdatedName")

    def test_delete(self):
        logger.info(f">>> Test: Deleting a {self.model.__name__}\n")
        data = {"name": "ToDelete"}
        item = self.model(**data)
        self.db.add(item)
        self.db.commit()
        self.db.refresh(item)

        self.db.delete(item)
        self.db.commit()

        deleted_item = self.db.query(self.model).filter(self.model.id == item.id).first()
        logger.debug(f"Deleted {self.model.__name__}: %s", to_dict(deleted_item))

        self.assertIsNone(deleted_item)


